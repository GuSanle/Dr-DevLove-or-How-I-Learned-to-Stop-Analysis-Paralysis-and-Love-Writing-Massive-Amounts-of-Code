from collections import defaultdict
from .api import get_repo_commits, get_commit_stats
from .ui import Colors, print_progress, print_progress_done

def scan_repositories(repos_to_scan, active_branches_map, username, since_date, until_date):
    """
    Scan the provided repositories for commits and statistics.
    
    Args:
        repos_to_scan: List of tuples (repo_full_name, repo_name)
        active_branches_map: Dict of {repo_full_name: set(branches)}
        username: GitHub username
        since_date: Start date
        until_date: End date
        
    Returns:
        stats: defaultdict containing commit counts and line changes
        repos_with_commits: Count of repos found to have relevant commits
    """
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
    
    return stats, repos_with_commits
