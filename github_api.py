import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')

# API endpoint
GITHUB_API_URL = "https://api.github.com"

def get_user_repos(username=None):
    """Fetch all repositories for a user (defaults to authenticated user)"""
    if not GITHUB_TOKEN:
        return None
    
    # Use provided username or default to authenticated user
    user = username or GITHUB_USERNAME
    
    if not user:
        return None
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f"{GITHUB_API_URL}/users/{user}/repos"
    
    try:
        response = requests.get(url, headers=headers, params={'per_page': 100})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repos: {e}")
        return None

def get_repo_details(repo_name):
    """Get detailed information about a specific repository"""
    if not GITHUB_TOKEN or not GITHUB_USERNAME:
        return None
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{repo_name}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repo details: {e}")
        return None

def get_repo_commits(repo_name, username):
    """Get commit count for a repository"""
    if not GITHUB_TOKEN:
        return 0
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # First try to get from repo object if available
    url = f"{GITHUB_API_URL}/repos/{username}/{repo_name}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        
        # Get the default branch
        default_branch = repo_data.get('default_branch', 'main')
        
        # Now get commits for that branch
        commits_url = f"{GITHUB_API_URL}/repos/{username}/{repo_name}/commits"
        commits_response = requests.get(
            commits_url, 
            headers=headers,
            params={'sha': default_branch, 'per_page': 1}
        )
        commits_response.raise_for_status()
        
        # Check Link header for total count
        link_header = commits_response.headers.get('Link', '')
        if 'last' in link_header:
            try:
                last_url = [link.split(';')[0].strip('<>') for link in link_header.split(',') if 'last' in link][0]
                page = int(last_url.split('page=')[-1])
                return page
            except:
                return len(commits_response.json())
        
        return len(commits_response.json())
    except Exception as e:
        print(f"Error getting commits for {repo_name}: {e}")
        return 0

def format_github_repos(repos, username):
    """Convert GitHub API response to our project format"""
    if not repos:
        return []
    
    formatted_repos = []
    for repo in repos:
        # Skip forked repos if you want (optional)
        if repo['fork']:
            continue
        
        commits = get_repo_commits(repo['name'], username)
        
        formatted_repos.append({
            'name': repo['name'],
            'description': repo['description'] or '',
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'language': repo['language'] or 'Unknown',
            'commits': commits,
            'url': repo['html_url']
        })
    
    return formatted_repos

def sync_github_repos_to_db(database_module=None, username=None):
    """Fetch repos from GitHub and add them to database"""
    repos = get_user_repos(username)
    
    if not repos:
        return False, "Failed to fetch repos from GitHub"
    
    formatted_repos = format_github_repos(repos, username or GITHUB_USERNAME)
    
    if not formatted_repos:
        return False, "No repositories found"
    
    added_count = 0
    for repo in formatted_repos:
        try:
            database_module.add_project(
                name=repo['name'],
                description=repo['description'],
                stars=repo['stars'],
                forks=repo['forks'],
                language=repo['language'],
                commits=repo['commits'],
                url=repo['url']
            )
            added_count += 1
        except Exception as e:
            print(f"Error adding {repo['name']}: {e}")
    
    return True, f"Added {added_count} repositories"