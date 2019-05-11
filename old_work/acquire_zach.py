import os
import json
from typing import Dict, List
import requests

# TODO: make a github personal access token
# TODO: replace YOUR_GITHUB_USERNAME with your github username

# Go here and generate a personal access token
# https://github.com/settings/tokens
# save it in your env.py file
# from env import github_token

# headers = {
#     'Authorization': f'token {github_token}',
#     'User-Agent': 'YOUR_GITHUB_USERNAME'
# }

def github_api_request(url: str) -> requests.Response:
    return requests.get(url)

def get_repo_language(repo: str) -> str:
    url = f'https://api.github.com/repos/{repo}'
    return github_api_request(url).json()['language']
    
def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f'https://api.github.com/repos/{repo}/contents/'
    return github_api_request(url).json()

def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    '''
    Takes in a response from the github api that lists
    the files in a repo and returns the url that can be
    used to download the repo's README file.
    '''
    for file in files:
        if file['name'].lower().startswith('readme'):
            return file['download_url']

def process_repo(repo: str) -> Dict[str, str]:
    '''
    Takes a repo name like "gocodeup/codeup-setup-script" and returns
    a dictionary with the language of the repo and the readme contents.
    '''
    contents = get_repo_contents(repo)
    return {
        'repo': repo,
        'language': get_repo_language(repo),
        'readme_contents': requests.get(get_readme_download_url(contents)).text
    }

# TODO: put a lot of repos here (or generate the list progromatically)
# repos = [
#     'gocodeup/codeup-setup-script',
#     'gocodeup/movies-application',

# ]

def scrape_github_data(repos):
    data = [process_repo(repo) for repo in repos]
    json.dump(data, open('data.json', 'w'))
    
if __name__ == '__main__':
    scrape_github_data()