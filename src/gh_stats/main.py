#!/usr/bin/env python3
import sys
import argparse
import datetime
import subprocess
import shutil
from collections import defaultdict

from .api import get_current_user, get_user_repos, get_org_repos, get_repo_commits, get_commit_stats, get_user_active_branches
from .ui import Colors, print_styled, print_progress, print_progress_done, render_table
from .utils import parse_date_range, parse_relative_date

def main():
    parser = argparse.ArgumentParser(description="GitHub contribution statistics")
    parser.add_argument('--personal', dest='personal', action='store_true', default=True, help='Include personal repos (default)')
    parser.add_argument('--no-personal', dest='personal', action='store_false', help='Exclude personal repos')
    parser.add_argument('--orgs', type=str, default='', help='Comma-separated organization names')
    
    # Date selection (yt-dlp style aliases)
    parser.add_argument('--since', '--date-after', dest='since', type=str, help='Start date (YYYY-MM-DD, YYYYMMDD, or relative like "today-1week")')
    parser.add_argument('--until', '--date-before', dest='until', type=str, help='End date (YYYY-MM-DD, YYYYMMDD, or relative like "today")')
    
    # choices removed to allow flexible formats like '3days', 'today-1week'
    parser.add_argument('--range', type=str, help='Date range preset (e.g., today, week, 3days)')
    parser.add_argument('--personal-limit', type=int, help='Max personal repos to scan (0=unlimited)')
    parser.add_argument('--org-limit', type=int, help='Max repos per org to scan (0=unlimited)')
    parser.add_argument('--all-branches', action='store_true', help='Scan all active branches (found via Events API) instead of just default branch')
    args = parser.parse_args()

    # Remove defaults_map and automatic limit logic
    personal_limit = args.personal_limit
    org_limit = args.org_limit

    # Date Logic
    # 1. Start with 'range' preset if exists
    if args.range:
        try:
            since_date, until_date = parse_date_range(args.range)
        except ValueError:
            since_date = datetime.date.today()
            until_date = datetime.date.today()
    else:
        since_date = datetime.date.today()
        until_date = datetime.date.today()

    # 2. Override with explicit flags
    if args.since:
        try:
            since_date = parse_relative_date(args.since)
        except ValueError:
            pass
    if args.until:
        try:
            until_date = parse_relative_date(args.until)
        except ValueError:
            pass

    orgs = [o.strip() for o in args.orgs.split(',') if o.strip()]

    # Check gh
    if shutil.which('gh') is None:
        print_styled("Error: 'gh' CLI not installed.", Colors.RED, True)
        sys.exit(1)

    print_styled("GitHub Contribution Statistics", Colors.HEADER, True)
    print(f"Range: {since_date} to {until_date}")
    if orgs: print(f"Orgs: {', '.join(orgs)}")
    print(f"Personal: {'Yes' if args.personal else 'No'}")
    print()

    # Auth - Moved BEFORE discovery logic
    print(f"{Colors.CYAN}[...]{Colors.ENDC} Authenticating...", end="", flush=True)
    username = get_current_user()
    if not username:
        print(f"\r{Colors.RED}[✗]{Colors.ENDC} Error: Run 'gh auth login' first.")
        sys.exit(1)
    print(f"\r{Colors.GREEN}[✔]{Colors.ENDC} Authenticated as: {username}")
    
    # Discovery Logic (Hybrid)
    repos_to_scan_set = set() # (full_name, name) tuples
    active_branches_map = {} 
    
    # 1. ALWAYS run Events API (Precision Layer)
    # This guarantees we capture everything active in the last ~90 days
    print(f"{Colors.CYAN}[...]{Colors.ENDC} Analyzing recent activity (Events API)...", end="", flush=True)
    active_branches_map = get_user_active_branches(username) # {repo: branches}
    print(f"\r{Colors.GREEN}[✔]{Colors.ENDC} Found recent activity in {len(active_branches_map)} repos")
    
    for full_name in active_branches_map.keys():
        if '/' in full_name:
             _, name = full_name.split('/', 1)
             repos_to_scan_set.add((full_name, name))
        else:
             repos_to_scan_set.add((full_name, full_name))

    # 2. Check Range for Fallback (Full History Layer)
    days_ago = (datetime.date.today() - since_date).days
    
    if days_ago > 90:
        print(f"\n{Colors.WARNING}[WARN]{Colors.ENDC} Time range > 90 days. Events API covers recent 90 days.")
        print(f"To ensure coverage for older activity (>90 days ago), we can fallback to scanning repo lists.")
        
        choice = input(f"{Colors.BOLD}Scan older repos? [a]ll, [number], or [Enter] to skip: {Colors.ENDC}").strip().lower()
        
        limit = None
        should_fetch = False
        
        if choice == 'a' or choice == 'all':
            limit = None
            should_fetch = True
            print(f" -> Scanning ALL remaining repositories.")
        elif choice.isdigit():
            limit = int(choice)
            should_fetch = True
            print(f" -> Scanning top {limit} remaining repositories.")
        else:
            print(f" -> Skipping fallback scan. Only checking {len(repos_to_scan_set)} active repos.")
        
        if should_fetch:
            # Fetch Personal
            if args.personal:
                print(f"{Colors.CYAN}[...]{Colors.ENDC} Fetching personal repos...", end="", flush=True)
                user_repos = get_user_repos(username, limit)
                for r in user_repos:
                    repos_to_scan_set.add((r['full_name'], r['name']))
                print(f"\r{Colors.GREEN}[✔]{Colors.ENDC} Found {len(user_repos)} personal repos")

            # Fetch Orgs
            for org in orgs:
                print(f"{Colors.CYAN}[...]{Colors.ENDC} Fetching {org} repos...", end="", flush=True)
                org_repos = get_org_repos(org, limit)
                for r in org_repos:
                    repos_to_scan_set.add((r['full_name'], r['name']))
                print(f"\r{Colors.GREEN}[✔]{Colors.ENDC} Found {len(org_repos)} repos in {org}")
                
    else:
        print(f"{Colors.CYAN}[INFO]{Colors.ENDC} Range within 90 days. Events API coverage is sufficient.")

    # Convert set to list for processing
    repos_to_scan = list(repos_to_scan_set)

    if not repos_to_scan:
        print_styled("No repositories to scan.", Colors.WARNING)
        return

    # Scanning
    print(f"\n{Colors.BOLD}Scanning {len(repos_to_scan)} repositories...{Colors.ENDC}\n")
    stats = defaultdict(lambda: {'commits': 0, 'added': 0, 'deleted': 0})
    repos_with_commits = 0
    
    for idx, (repo_full_name, repo_name) in enumerate(repos_to_scan):
        print_progress(idx, len(repos_to_scan), repo_full_name, "checking...")
        
        # Determine strict branches to check if we have data
        target_branches = active_branches_map.get(repo_full_name) # Returns Set or None
        
        commits = get_repo_commits(repo_full_name, username, since_date, until_date, target_branches)
        if commits:
            repos_with_commits += 1
            print_progress(idx, len(repos_to_scan), repo_full_name, f"found {len(commits)} commits")
            for commit in commits:
                stats[repo_full_name]['commits'] += 1
                added, deleted = get_commit_stats(repo_full_name, commit['sha'])
                stats[repo_full_name]['added'] += added
                stats[repo_full_name]['deleted'] += deleted
    
    print_progress(len(repos_to_scan), len(repos_to_scan), "Complete", "")
    print_progress_done(f"Scanned {len(repos_to_scan)} repos, {repos_with_commits} with commits")

    # Output
    render_table(stats, since_date, until_date)

if __name__ == "__main__":
    main()
