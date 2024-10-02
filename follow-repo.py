import argparse
import requests
import json
import time
from urllib.parse import quote

def listOrganizationRepositories(baseurl, provider, organization, token):
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    
    url = f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories'
    repositories = []
    cursor = None
    
    while True:
        if cursor:
            response = requests.get(f'{url}?cursor={quote(cursor)}', headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        data = response.json()
        repositories.extend([repo['name'] for repo in data['data']])
        
        if 'pagination' in data and 'next' in data['pagination']:
            cursor = data['pagination']['next']
        else:
            break
    
    return repositories

def followAllRepositories(baseurl, provider, organization, token, reponame):
    repositories = listOrganizationRepositories(baseurl, provider, organization, token)
    allAboard = (reponame == None)
    targetRepos = reponame.split(',') if not allAboard else repositories
    
    for repo in repositories:
        if allAboard or repo in targetRepos:
            followRepository(baseurl, provider, organization, repo, token)

def followRepository(baseurl, provider, organization, repo, token):
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    url = f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories/{repo}/follow'
    response = requests.post(url, headers=headers)
    print(f"{repo}: {response.status_code}")

def main():
    print('\nWelcome to Codacy Integration Helper - Follow All Repositories\n')
    parser = argparse.ArgumentParser(description='Codacy Integration Helper')
    parser.add_argument('--token', dest='token', required=True,
                        help='the api-token to be used on the Codacy REST API')
    parser.add_argument('--reponame', dest='reponame', default=None,
                        help='comma separated list of the repositories to be followed, none means all')
    parser.add_argument('--provider', dest='provider', required=True,
                        help='git provider (gh|ghe|gl|bb)')
    parser.add_argument('--organization', dest='organization', required=True,
                        help='organization name')
    parser.add_argument('--baseurl', dest='baseurl', default='https://app.codacy.com',
                        help='codacy server address (ignore if cloud)')
    args = parser.parse_args()
    
    startdate = time.time()
    followAllRepositories(args.baseurl, args.provider, args.organization, args.token, args.reponame)
    enddate = time.time()
    print(f"\nThe script took {round(enddate-startdate,2)} seconds")

if __name__ == "__main__":
    main()