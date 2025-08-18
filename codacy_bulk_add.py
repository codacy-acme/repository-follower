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
        current_url = f'{url}?limit=100&filter=NotSynced' + (f'&cursor={quote(cursor)}' if cursor else '')
        logger.debug(f"Making request to: {current_url}")
        
        try:
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Retrieved {len(data.get('data', []))} repositories")
            logger.debug(f"Response: {json.dumps(data, indent=2)}")
            
            repositories.extend([repo['name'] for repo in data['data']])
            
            if 'pagination' in data and 'cursor' in data['pagination']:
                cursor = data['pagination']['cursor']
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

def addRepository(baseurl, provider, organization, repo, token):
    """Add a repository to Codacy."""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'api-token': token,
        'caller': 'codacy-integration-helper'
    }
    data = {
        "provider": provider,
        "repositoryFullPath": f'{organization}/{repo}'
    }
    url = f'{baseurl}/api/v3/repositories'
    
    try:
        logger.debug(f"Adding repository {repo} to Codacy...")
        logger.debug(f"Making request to: {url}")
        logger.debug(f"Request data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        logger.info(f"Successfully added {repo}")
        logger.debug(f"Response: {response.text}")
        return True, f"Successfully added {repo}: {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code == 409:
                logger.warning(f"Repository {repo} already exists")
                return False, f"Repository {repo} already exists: {e.response.status_code}"
            elif e.response.status_code == 401:
                # Check if the error message indicates the repository is already being followed
                try:
                    error_response = e.response.json()
                    if "permission" in error_response.get("message", "").lower():
                        logger.warning(f"Repository {repo} already exists (following state)")
                        return False, f"Repository {repo} already exists: {e.response.status_code}"
                except:
                    pass
                logger.error(f"Failed to add {repo}: {e.response.status_code}, Response: {e.response.text}")
                return False, f"Failed to add {repo}: {e.response.status_code}, Response: {e.response.text}"
            else:
                logger.error(f"Failed to add {repo}: {e.response.status_code}, Response: {e.response.text}")
                return False, f"Failed to add {repo}: {e.response.status_code}, Response: {e.response.text}"
        else:
            logger.error(f"Failed to add {repo}: {str(e)}")
            return False, f"Failed to add {repo}: {str(e)}"

def updateRepositoryIntegrationsSettings(baseurl, provider, organization, repo, token):
    """Update repository integration settings to disable all integrations."""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'api-token': token,
        'caller': 'codacy-integration-helper'
    }
    data = {
        "commitStatus": False,
        "pullRequestComment": False,
        "pullRequestSummary": False,
        "coverageSummary": False,
        "suggestions": False,
        "aiEnhancedComments": False
    }
    url = f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories/{repo}/integrations/providerSettings'
    
    try:
        logger.debug(f"Updating integration settings for {repo}...")
        logger.debug(f"Making request to: {url}")
        logger.debug(f"Request data: {json.dumps(data, indent=2)}")
        
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        
        logger.info(f"Successfully updated integration settings for {repo}")
        logger.debug(f"Response: {response.text}")
        return True, f"Successfully updated integration settings {repo}: {response.status_code}"
        
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Failed to update integration settings {repo}: {e.response.status_code}, Response: {e.response.text}")
            return False, f"Failed to update integration settings {repo}: {e.response.status_code}, Response: {e.response.text}"
        else:
            logger.error(f"Failed to update integration settings {repo}: {str(e)}")
            return False, f"Failed to update integration settings {repo}: {str(e)}"

def processAllRepositories(baseurl, provider, organization, token, reponames=None, dry_run=False):
    """Process all repositories or specific ones if provided."""
    repositories = listRepositories(baseurl, provider, organization, token)
    
    if reponames:
        target_repos = [repo.strip() for repo in reponames.split(',')]
        logger.info(f"Processing specific repositories: {target_repos}")
        invalid_repos = set(target_repos) - set(repositories)
        if invalid_repos:
            logger.warning(f"These repositories were not found: {invalid_repos}")
        repositories = [repo for repo in repositories if repo in target_repos]
    else:
        logger.info("Processing all repositories")
    
    if dry_run:
        logger.info("DRY RUN MODE - No actual changes will be made")
        logger.info(f"Would process {len(repositories)} repositories:")
        for repo in repositories:
            logger.info(f"  - {repo}")
        return len(repositories), 0, 0
    
    success_count = 0
    fail_count = 0
    already_exists_count = 0
    
    for i, repo in enumerate(repositories, 1):
        logger.info(f"Processing repository {i}/{len(repositories)}: {repo}")
        
        # Add repository
        add_success, add_message = addRepository(baseurl, provider, organization, repo, token)
        
        if add_success:
            success_count += 1
            # Update integration settings
            settings_success, settings_message = updateRepositoryIntegrationsSettings(
                baseurl, provider, organization, repo, token
            )
            if not settings_success:
                logger.warning(f"Repository added but failed to update settings: {settings_message}")
        else:
            if "already exists" in add_message.lower():
                already_exists_count += 1
                logger.info(f"Repository {repo} already exists, skipping...")
            else:
                fail_count += 1
                logger.error(add_message)
        
        # Rate limiting - wait between requests
        if i < len(repositories):  # Don't wait after the last repository
            logger.debug("Waiting 2 seconds to avoid rate limiting...")
            time.sleep(2)
    
    return success_count, fail_count, already_exists_count

def main():
    print('\nWelcome to Codacy Bulk Repository Add Tool\n')
    
    parser = argparse.ArgumentParser(description='Codacy Bulk Repository Add Tool')
    parser.add_argument('--token', required=True, help='The API token to be used on the REST API')
    parser.add_argument('--provider', default='gh', help='Git provider (gh for GitHub, gl for GitLab, etc.) - default: gh')
    parser.add_argument('--organization', required=True, help='Organization name')
    parser.add_argument('--baseurl', default='https://app.codacy.com', help='Codacy server address - default: https://app.codacy.com')
    parser.add_argument('--reponames', help='Comma separated list of repositories to add (optional - if not provided, all repos will be processed)')
    parser.add_argument('--dry-run', action='store_true', help='Preview what would be added without making actual changes')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()

    if not args.debug:
        logging.getLogger().setLevel(logging.INFO)

    logger.info(f"Starting bulk add with provider: {args.provider}, organization: {args.organization}")
    logger.debug(f"Base URL: {args.baseurl}")
    logger.debug(f"Dry run mode: {args.dry_run}")
    
    start_time = time.time()
    
    try:
        success_count, fail_count, already_exists_count = processAllRepositories(
            args.baseurl, 
            args.provider, 
            args.organization, 
            args.token, 
            args.reponames,
            args.dry_run
        )
        
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        
        logger.info(f"\n{'='*50}")
        logger.info(f"Script completed in {execution_time} seconds")
        
        if args.dry_run:
            logger.info(f"DRY RUN: Would have processed {success_count} repositories")
        else:
            logger.info(f"Successfully added {success_count} repositories")
            if already_exists_count > 0:
                logger.info(f"Skipped {already_exists_count} repositories (already exist)")
            if fail_count > 0:
                logger.warning(f"Failed to add {fail_count} repositories")
        
        logger.info(f"{'='*50}")
        
        return 0 if fail_count == 0 else 1
        
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
