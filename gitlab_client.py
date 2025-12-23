"""
GitLab API Client for fetching user activity data.
"""
import requests
from typing import Dict, List, Optional


class GitLabClient:
    """Client for interacting with GitLab API."""
    
    def __init__(self, url: str, token: str, username: str):
        """
        Initialize GitLab client.
        
        Args:
            url: GitLab instance URL
            token: Personal access token
            username: GitLab username
        """
        self.url = url.rstrip('/')
        self.token = token
        self.username = username
        self.headers = {
            'PRIVATE-TOKEN': token
        }
    
    def get_user_id(self) -> Optional[int]:
        """Get the user ID for the configured username."""
        try:
            response = requests.get(
                f"{self.url}/api/v4/users",
                headers=self.headers,
                params={'username': self.username}
            )
            response.raise_for_status()
            users = response.json()
            if users:
                return users[0]['id']
        except Exception as e:
            print(f"Error fetching user ID: {e}")
        return None
    
    def get_recent_commits(self, since: Optional[str] = None) -> List[Dict]:
        """
        Get recent commits by the user.
        
        Args:
            since: ISO 8601 formatted date string to filter commits
            
        Returns:
            List of commit events
        """
        user_id = self.get_user_id()
        if not user_id:
            return []
        
        try:
            # Base parameters for the events API call
            base_params = {'action': 'pushed'}
            if since:
                base_params['after'] = since

            # Fetch all pages of events to avoid missing commits due to pagination
            events: List[Dict] = []
            page = 1
            while True:
                params = dict(base_params)
                params['page'] = page

                response = requests.get(
                    f"{self.url}/api/v4/users/{user_id}/events",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                page_events = response.json()
                if not page_events:
                    break
                events.extend(page_events)

                next_page = response.headers.get('X-Next-Page')
                if not next_page:
                    break
                try:
                    page = int(next_page)
                except (TypeError, ValueError):
                    page += 1
            
            # Filter for push events and extract commit info
            commits = []
            for event in events:
                if event.get('action_name') == 'pushed to':
                    push_data = event.get('push_data', {})
                    commits.append({
                        'commit_count': push_data.get('commit_count', 1),
                        'created_at': event.get('created_at'),
                        'project': event.get('project_id'),
                        'ref': push_data.get('ref')
                    })
            
            return commits
        except Exception as e:
            print(f"Error fetching commits: {e}")
            return []
    
    def get_approved_merge_requests(self, since: Optional[str] = None) -> List[Dict]:
        """
        Get merge requests that were approved.
        
        Args:
            since: ISO 8601 formatted date string to filter MRs
            
        Returns:
            List of approved merge requests
        """
        user_id = self.get_user_id()
        if not user_id:
            return []
        
        try:
            params = {
                'action': 'approved',
                'after': since
            } if since else {'action': 'approved'}
            
            response = requests.get(
                f"{self.url}/api/v4/users/{user_id}/events",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            events = response.json()
            
            # Filter for approval events
            approvals = []
            for event in events:
                if 'approved' in event.get('action_name', '').lower():
                    approvals.append({
                        'target_title': event.get('target_title'),
                        'created_at': event.get('created_at'),
                        'project': event.get('project_id')
                    })
            
            return approvals
        except Exception as e:
            print(f"Error fetching merge requests: {e}")
            return []
    
    def get_language_stats(self) -> Dict[str, int]:
        """
        Get programming language statistics from user's projects.
        
        Returns:
            Dictionary mapping language names to usage counts
        """
        user_id = self.get_user_id()
        if not user_id:
            return {}
        
        try:
            # Get user's projects
            response = requests.get(
                f"{self.url}/api/v4/users/{user_id}/projects",
                headers=self.headers
            )
            response.raise_for_status()
            projects = response.json()
            
            # Aggregate language statistics
            language_stats = {}
            for project in projects[:10]:  # Limit to recent projects
                # Get project languages
                proj_response = requests.get(
                    f"{self.url}/api/v4/projects/{project['id']}/languages",
                    headers=self.headers
                )
                if proj_response.status_code == 200:
                    languages = proj_response.json()
                    for lang, percentage in languages.items():
                        language_stats[lang] = language_stats.get(lang, 0) + percentage
            
            return language_stats
        except Exception as e:
            print(f"Error fetching language stats: {e}")
            return {}
