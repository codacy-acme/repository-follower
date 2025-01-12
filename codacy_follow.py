import argparse
import requests
import json
import time
import logging
from urllib.parse import quote

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def listRepositories(baseurl, provider, organization, token):
    """List all repositories in the organization with pagination support."""
    repositories = []
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    
    url = f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories'
    cursor = None
    
    while True:
        current_url = f'{url}?limit=100' + (f'&cursor={quote(cursor)}' if cursor else '')
        logger.debug(f"Making request to: {current_url}")
        
        try:
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Retrieved {len(data.get('data', []))} repositories")
            logger.debug(f"Response: {json.dumps(data, indent=2)}")
            
            repositories.extend([repo['name'] for repo in data['data']])
            
            if 'pagination' in data and 'next' in data['pagination']:
                cursor = data['pagination']['next']
                logger.debug(f"Next page cursor: {cursor}")
            else:
                break
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request: {str(e)}")
            if response is not None:
                logger.error(f"Response status: {response.status_code}")
                logger.error(f"Response body: {response.text}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response: {str(e)}")
            raise
        except KeyError as e:
            logger.error(f"Unexpected response structure: {str(e)}")
            raise
            
    logger.info(f"Total repositories found: {len(repositories)}")
    return repositories

def followRepository(baseurl, provider, organization, repo, token):
    """Follow a single repository."""
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    url = f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories/{repo}/follow'
    
    logger.debug(f"Following repository: {repo}")
    logger.debug(f"Making request to: {url}")
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        logger.info(f"Successfully followed {repo}")
        logger.debug(f"Response: {response.text}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error following {repo}: {str(e)}")
        if response is not None:
            logger.error(f"Response status: {response.status_code}")
            logger.error(f"Response body: {response.text}")
        return False

def followAllRepositories(baseurl, provider, organization, token, reponames=None):
    """Follow all repositories or specific ones if provided."""
    repositories = listRepositories(baseurl, provider, organization, token)
    
    if reponames:
        target_repos = reponames.split(',')
        logger.info(f"Following specific repositories: {target_repos}")
        invalid_repos = set(target_repos) - set(repositories)
        if invalid_repos:
            logger.warning(f"These repositories were not found: {invalid_repos}")
        repositories = [repo for repo in repositories if repo in target_repos]
    else:
        logger.info("Following all repositories")
    
    success_count = 0
    fail_count = 0
    
    for repo in repositories:
        if followRepository(baseurl, provider, organization, repo, token):
            success_count += 1
        else:
            fail_count += 1
    
    return success_count, fail_count

def main():
    parser = argparse.ArgumentParser(description='Codacy Repository Auto-Follow')
    parser.add_argument('--token', required=True, help='The API token to be used on the REST API')
    parser.add_argument('--provider', required=True, help='Git provider (gh for GitHub, gl for GitLab, etc.)')
    parser.add_argument('--organization', required=True, help='Organization name')
    parser.add_argument('--baseurl', default='https://app.codacy.com', help='Codacy server address (ignore if cloud)')
    parser.add_argument('--reponames', help='Comma separated list of repositories to follow (optional)')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    if not args.debug:
        logging.getLogger().setLevel(logging.INFO)

    logger.info(f"Starting script with provider: {args.provider}, organization: {args.organization}")
    logger.debug(f"Base URL: {args.baseurl}")
    
    start_time = time.time()
    
    try:
        success_count, fail_count = followAllRepositories(
            args.baseurl, 
            args.provider, 
            args.organization, 
            args.token, 
            args.reponames
        )
        
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        
        logger.info(f"\nScript completed in {execution_time} seconds")
        logger.info(f"Successfully followed {success_count} repositories")
        if fail_count > 0:
            logger.warning(f"Failed to follow {fail_count} repositories")
        
        return 0 if fail_count == 0 else 1
        
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())