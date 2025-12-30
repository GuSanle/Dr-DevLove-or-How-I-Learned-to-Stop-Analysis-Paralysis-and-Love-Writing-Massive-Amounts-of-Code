import pytest
from gh_stats.api import get_user_active_branches

@pytest.fixture
def mock_run_cmd(mocker):
    return mocker.patch('gh_stats.api.run_gh_cmd')

def test_get_active_branches_push_event(mock_run_cmd):
    """
    Scenario: User pushed code to existing branches.
    """
    mock_events = [
        {
            'type': 'PushEvent',
            'repo': {'name': 'user/repo1'},
            'payload': {
                'ref': 'refs/heads/main'  # Standard push
            }
        },
        {
            'type': 'PushEvent',
            'repo': {'name': 'user/repo1'},
            'payload': {
                'ref': 'refs/heads/feature-x' # Another branch
            }
        },
        {
            'type': 'PushEvent',
            'repo': {'name': 'org/repo2'},
            'payload': {
                'ref': 'refs/tags/v1.0' # Tag push - should be IGNORED (if logic assumes heads only)
            }
        }
    ]
    
    # Return events on first page, empty on second
    mock_run_cmd.side_effect = [mock_events, []]
    
    active_map = get_user_active_branches('user')
    
    assert 'user/repo1' in active_map
    assert 'main' in active_map['user/repo1']
    assert 'feature-x' in active_map['user/repo1']
    
    # Verify tag push was ignored (based on current implementation seeing 'refs/heads/')
    if 'org/repo2' in active_map:
        assert 'v1.0' not in active_map['org/repo2']

def test_get_active_branches_create_event(mock_run_cmd):
    """
    Scenario: User created a new branch.
    """
    mock_events = [
        {
            'type': 'CreateEvent',
            'repo': {'name': 'user/new-repo'},
            'payload': {
                'ref_type': 'branch',
                'ref': 'init-branch'
            }
        },
        {
            'type': 'CreateEvent',
            'repo': {'name': 'user/another-repo'},
            'payload': {
                'ref_type': 'tag',  # Should be ignored
                'ref': 'v0.1'
            }
        }
    ]
    
    mock_run_cmd.side_effect = [mock_events, []]
    
    active_map = get_user_active_branches('user')
    
    # Check branch creation logic
    assert 'user/new-repo' in active_map
    assert 'init-branch' in active_map['user/new-repo']
    
    # Check tag creation ignored
    assert 'user/another-repo' not in active_map

def test_get_active_branches_pagination(mock_run_cmd):
    """
    Verify that it fetches multiple pages.
    """
    page1 = [{'type': 'PushEvent', 'repo': {'name': 'r1'}, 'payload': {'ref': 'refs/heads/b1'}}]
    page2 = [{'type': 'PushEvent', 'repo': {'name': 'r2'}, 'payload': {'ref': 'refs/heads/b2'}}]
    
    # We need to simulate full pages. The code checks `len(data) < 100` to break.
    # So we must return a list of length 100 to trigger next page.
    full_page = page1 * 100 
    
    mock_run_cmd.side_effect = [full_page, page2, []]
    
    active_map = get_user_active_branches('user')
    
    assert mock_run_cmd.call_count >= 2
    assert 'r1' in active_map
    assert 'r2' in active_map
