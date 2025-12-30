import datetime
from datetime import date, timedelta
from unittest.mock import MagicMock
import pytest
from gh_stats.discovery import discover_repositories

# Mock the dependencies where they are used in discovery.py
@pytest.fixture
def mock_api(mocker):
    return {
        'get_active': mocker.patch('gh_stats.discovery.get_user_active_branches'),
        'get_user_repos': mocker.patch('gh_stats.discovery.get_user_repos'),
        'get_org_repos': mocker.patch('gh_stats.discovery.get_org_repos'),
        'search_commits': mocker.patch('gh_stats.discovery.search_user_commits'),
    }

def test_discover_recent_events_only(mock_api):
    """
    Scenario: Date range is small (e.g. today).
    Should only rely on Events API. Fallback logic skipped.
    """
    mock_api['get_active'].return_value = {
        'user/repo1': {'main'},
        'user/repo2': {'dev'}
    }
    
    repos, branches = discover_repositories(
        username='user',
        since_date=date.today(),
        until_date=date.today(),
        orgs=[],
        personal=True
    )
    
    # Verify outputs
    assert len(repos) == 2
    assert ('user/repo1', 'repo1') in repos
    assert ('user/repo2', 'repo2') in repos
    assert branches == {'user/repo1': {'main'}, 'user/repo2': {'dev'}}
    
    # Verify fallback was NOT called
    mock_api['get_user_repos'].assert_not_called()

def test_discover_filtering_personal_only(mock_api):
    """
    Scenario: Active branches found for user and org.
    User only wants personal repos.
    """
    mock_api['get_active'].return_value = {
        'user/my-repo': {'main'},
        'my-org/corp-repo': {'main'}
    }
    
    repos, _ = discover_repositories(
        username='user',
        since_date=date.today(),
        until_date=date.today(),
        orgs=[],
        personal=True
    )
    
    assert len(repos) == 1
    assert repos[0] == ('user/my-repo', 'my-repo')

def test_discover_filtering_org_only(mock_api):
    """
    Scenario: User wants specific org repos, no personal.
    """
    mock_api['get_active'].return_value = {
        'user/my-repo': {'main'},
        'target-org/repo1': {'main'},
        'other-org/repo2': {'main'}
    }
    
    repos, _ = discover_repositories(
        username='user',
        since_date=date.today(),
        until_date=date.today(),
        orgs=['target-org'],
        personal=False
    )
    
    assert len(repos) == 1
    assert repos[0] == ('target-org/repo1', 'repo1')

def test_discover_fallback_logic(mock_api):
    """
    Scenario: Date range > 90 days. User selects 'all' at prompt.
    Should fetch full repo lists.
    """
    # Setup active branches (recent activity)
    mock_api['get_active'].return_value = {'user/active-repo': {'main'}}
    
    # Setup fallback repos (old history)
    mock_api['get_user_repos'].return_value = [
        {'full_name': 'user/old-repo', 'name': 'old-repo'}
    ]
    
    # Mock prompt to return 'all'
    mock_prompt = MagicMock(return_value='all')
    
    long_ago = date.today() - timedelta(days=100)
    
    repos, _ = discover_repositories(
        username='user',
        since_date=long_ago,
        until_date=date.today(),
        orgs=[],
        personal=True,
        prompt_callback=mock_prompt
    )
    
    # Should include BOTH active and old repos
    assert len(repos) == 2
    repo_names = {r[1] for r in repos}
    assert 'active-repo' in repo_names
    assert 'old-repo' in repo_names
    
    # Verify fallback WAS called
    mock_api['get_user_repos'].assert_called_once()

def test_discover_fallback_skip(mock_api):
    """
    Scenario: Date range > 90 days, but user presses Enter (skip).
    """
    mock_api['get_active'].return_value = {'user/active-repo': {'main'}}
    
    mock_prompt = MagicMock(return_value='') # Empty input = skip in code logic
    
    long_ago = date.today() - timedelta(days=100)
    
    repos, _ = discover_repositories(
        username='user',
        since_date=long_ago,
        until_date=date.today(),
        orgs=[],
        personal=True,
        prompt_callback=mock_prompt
    )
    
    # Should only have active repo
    assert len(repos) == 1
    assert repos[0] == ('user/active-repo', 'active-repo')
    
    # Verify fallback was NOT called
    mock_api['get_user_repos'].assert_not_called()

