from datetime import date
from .api import get_user_active_branches, get_user_repos, get_org_repos
from .ui import Colors

def default_prompt_callback(msg):
    return input(msg)

def discover_repositories(username, since_date, orgs, personal, is_self=True, prompt_callback=default_prompt_callback):
    """
    Discover repositories based on the hybrid logic:
    1. Always check Events API for recent activity (precision layer).
    2. If date range > 90 days, prompt user for interactive fallback (history layer).
    
    Args:
        username: Target GitHub username to analyze
        since_date: Start date for the range
        orgs: List of organization names to include
        personal: Whether to include personal repos
        is_self: True if username is the authenticated user (can see private repos),
                 False if querying another user (public repos only)
        prompt_callback: Callback for user prompts
    
    Returns:
        repos_to_scan: List of tuples (full_name, name)
        active_branches_map: Dict of {repo_full_name: set(branches)}
    """
    
    repos_to_scan_set = set() # (full_name, name) tuples
    active_branches_map = {} 
    
    # When querying other users, orgs filter doesn't apply (we only see their personal public repos)
    if not is_self:
        orgs = []
        if not personal:
            print(f"{Colors.WARNING}[WARN]{Colors.ENDC} --no-personal with --user makes no sense. Enabling personal repos.")
            personal = True
    
    # 1. ALWAYS run Events API (Precision Layer)
    print(f"{Colors.CYAN}[...]{Colors.ENDC} Analyzing recent activity (Events API)...", end="", flush=True)
    active_branches_map = get_user_active_branches(username) # {repo: branches}
    print(f"\r{Colors.GREEN}[✔]{Colors.ENDC} Found recent activity in {len(active_branches_map)} repos")
    
    for full_name in active_branches_map.keys():
        owner, name = full_name.split('/', 1) if '/' in full_name else (username, full_name)
        
        if not is_self:
            # When querying OTHER users: include ALL repos from Events API
            # These are all repos where the target user had public activity
            repos_to_scan_set.add((full_name, name))
        else:
            # When querying SELF: apply filtering logic
            # 1. Personal Repos: Include if --personal is active AND owner is me
            is_personal_match = personal and (owner == username)
            
            # 2. Org Repos: Include if owner is in the allowed orgs list
            is_org_match = owner in orgs
            
            if is_personal_match or is_org_match:
                 repos_to_scan_set.add((full_name, name))

    # 2. Check Range for Fallback (Full History Layer)
    days_ago = (date.today() - since_date).days
    
    if days_ago > 90:
        print(f"\n{Colors.WARNING}[WARN]{Colors.ENDC} Time range > 90 days. Events API covers recent 90 days.")
        print(f"To ensure coverage for older activity (>90 days ago), we can fallback to scanning repo lists.")
        
        choice = prompt_callback(f"{Colors.BOLD}Scan older repos? [a]ll, [number], or [Enter] to skip: {Colors.ENDC}").strip().lower()
        
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
            # Fetch Personal repos
            if personal:
                print(f"{Colors.CYAN}[...]{Colors.ENDC} Fetching personal repos...", end="", flush=True)
                user_repos = get_user_repos(username, limit, is_self=is_self)
                for r in user_repos:
                    repos_to_scan_set.add((r['full_name'], r['name']))
                visibility_hint = "" if is_self else " (public only)"
                print(f"\r{Colors.GREEN}[✔]{Colors.ENDC} Found {len(user_repos)} personal repos{visibility_hint}")

            # Fetch Org repos (only when querying self)
            for org in orgs:
                print(f"{Colors.CYAN}[...]{Colors.ENDC} Fetching {org} repos...", end="", flush=True)
                org_repos = get_org_repos(org, limit)
                for r in org_repos:
                    repos_to_scan_set.add((r['full_name'], r['name']))
                print(f"\r{Colors.GREEN}[✔]{Colors.ENDC} Found {len(org_repos)} repos in {org}")
                
    else:
        print(f"{Colors.CYAN}[INFO]{Colors.ENDC} Range within 90 days. Events API coverage is sufficient.")

    return list(repos_to_scan_set), active_branches_map

