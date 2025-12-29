import json
import subprocess

def run_gh_cmd(args, silent=False):
    try:
        result = subprocess.run(['gh'] + args, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        return None
    except json.JSONDecodeError:
        return None

def get_current_user():
    data = run_gh_cmd(['api', 'user'])
    return data['login'] if data else None

def get_user_repos(username, limit=None):
    repos = []
    page = 1
    while True:
        data = run_gh_cmd(['api', f'users/{username}/repos?per_page=100&page={page}&type=owner&sort=pushed&direction=desc'], silent=True)
        if not data: break
        repos.extend(data)
        if limit and len(repos) >= limit:
            return repos[:limit]
        if len(data) < 100: break
        page += 1
    return repos

def get_org_repos(org, limit=None):
    repos = []
    page = 1
    while True:
        data = run_gh_cmd(['api', f'orgs/{org}/repos?per_page=100&page={page}&sort=pushed&direction=desc'], silent=True)
        if not data: break
        repos.extend(data)
        if limit and len(repos) >= limit:
            return repos[:limit]
        if len(data) < 100: break
        page += 1
    return repos

import datetime

def get_repo_commits(repo_full_name, author, since_date, until_date):
    # Determine local timezone offset
    local_tz = datetime.datetime.now().astimezone().tzinfo
    
    # Create local datetime objects for start and end of day
    since_dt = datetime.datetime.combine(since_date, datetime.time.min, tzinfo=local_tz)
    until_dt = datetime.datetime.combine(until_date, datetime.time.max, tzinfo=local_tz)
    
    # Convert to UTC
    since_utc = since_dt.astimezone(datetime.timezone.utc)
    until_utc = until_dt.astimezone(datetime.timezone.utc)
    
    # Format as API expects (ISO 8601 with Z)
    since_iso = since_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
    until_iso = until_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    commits = []
    page = 1
    while True:
        data = run_gh_cmd([
            'api', 
            f'repos/{repo_full_name}/commits?author={author}&since={since_iso}&until={until_iso}&per_page=100&page={page}'
        ], silent=True)
        if not data: break
        commits.extend(data)
        if len(data) < 100: break
        page += 1
    return commits

def get_commit_stats(repo_full_name, sha):
    data = run_gh_cmd(['api', f'repos/{repo_full_name}/commits/{sha}'], silent=True)
    if data and 'stats' in data:
        return data['stats'].get('additions', 0), data['stats'].get('deletions', 0)
    return 0, 0
