import sys

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ENDC = '\033[0m'

def print_styled(text, color=Colors.ENDC, bold=False):
    style = color + (Colors.BOLD if bold else '')
    print(f"{style}{text}{Colors.ENDC}")

def print_progress(current, total, repo_name, status=""):
    bar_width = 20
    filled = int(bar_width * current / total) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_width - filled)
    percent = int(100 * current / total) if total > 0 else 0
    # Truncate repo name if too long
    display_repo = repo_name[:30] + "..." if len(repo_name) > 33 else repo_name
    sys.stdout.write(f"\r{Colors.CYAN}[{bar}]{Colors.ENDC} {percent:3d}% │ {display_repo:<35} {status}\033[K")
    sys.stdout.flush()

def print_progress_done(message="Complete"):
    sys.stdout.write(f"\r{Colors.GREEN}[✔]{Colors.ENDC} {message}\033[K\n")
    sys.stdout.flush()

def render_table(stats, since_date, until_date):
    if not stats:
        print_styled("\nNo commits found in the specified range.", Colors.WARNING)
        return

    print("\n")
    max_repo_len = max(len(r) for r in stats.keys())
    col_repo = max(max_repo_len + 2, 17)
    col_commits = 10
    col_changes = 25

    def print_sep(chars):
        print(f"{Colors.BLUE}{chars[0]}{chars[1]*col_repo}{chars[2]}{chars[1]*col_commits}{chars[2]}{chars[1]*col_changes}{chars[3]}{Colors.ENDC}")

    print_sep("┌─┬┐")
    print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}{'Repository':<{col_repo-1}}{Colors.ENDC}{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}{'Commits':<{col_commits-1}}{Colors.ENDC}{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}{'Changes':<{col_changes-1}}{Colors.ENDC}{Colors.BLUE}│{Colors.ENDC}")
    print_sep("├─┼┤")

    total_commits = total_added = total_deleted = 0
    for repo, data in sorted(stats.items(), key=lambda x: x[1]['commits'], reverse=True):
        total_commits += data['commits']
        total_added += data['added']
        total_deleted += data['deleted']
        changes_str = f"{Colors.GREEN}+{data['added']}{Colors.ENDC} / {Colors.RED}-{data['deleted']}{Colors.ENDC}"
        visible_len = len(f"+{data['added']} / -{data['deleted']}")
        padding = col_changes - 1 - visible_len
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.CYAN}{repo:<{col_repo-1}}{Colors.ENDC}{Colors.BLUE}│{Colors.ENDC} {str(data['commits']):<{col_commits-1}}{Colors.BLUE}│{Colors.ENDC} {changes_str}{' '*padding}{Colors.BLUE}│{Colors.ENDC}")

    print_sep("└─┴┘")

    print(f"\n{Colors.BOLD}Summary ({since_date} ~ {until_date}):{Colors.ENDC}")
    print(f"  • Active Projects: {Colors.CYAN}{len(stats)}{Colors.ENDC}")
    print(f"  • Total Commits:   {Colors.CYAN}{total_commits}{Colors.ENDC}")
    print(f"  • Total Growth:    {Colors.GREEN}+{total_added}{Colors.ENDC} lines")
    print(f"  • Total Cleaning:  {Colors.RED}-{total_deleted}{Colors.ENDC} lines")
