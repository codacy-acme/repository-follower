#!/usr/bin/env python3
import requests
import json
import argparse

def test_list_repositories(baseurl, provider, organization, token):
    """Test different API endpoints to list repositories."""
    
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    
    # Test the current endpoint (only shows added repos)
    print("=== Testing current endpoint (added repos only) ===")
    url1 = f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories'
    print(f"URL: {url1}")
    
    try:
        response = requests.get(url1, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            repos = [repo['name'] for repo in data.get('data', [])]
            print(f"Found {len(repos)} repositories:")
            for repo in repos[:10]:  # Show first 10
                print(f"  - {repo}")
            if len(repos) > 10:
                print(f"  ... and {len(repos) - 10} more")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Test potential alternative endpoints
    test_endpoints = [
        f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories/available',
        f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories?include=available',
        f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories?source=provider',
        f'{baseurl}/api/v3/organizations/{provider}/{organization}/repositories?status=all',
        f'{baseurl}/api/v3/providers/{provider}/organizations/{organization}/repositories',
        f'{baseurl}/api/v3/{provider}/{organization}/repositories',
    ]
    
    for url in test_endpoints:
        print(f"=== Testing: {url} ===")
        try:
            response = requests.get(url, headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'data' in data:
                    repos = [repo.get('name', 'Unknown') for repo in data.get('data', [])]
                    print(f"Found {len(repos)} repositories")
                    for repo in repos[:5]:  # Show first 5
                        print(f"  - {repo}")
                elif isinstance(data, list):
                    print(f"Found {len(data)} items")
                    for item in data[:5]:  # Show first 5
                        if isinstance(item, dict):
                            name = item.get('name', item.get('repositoryName', 'Unknown'))
                            print(f"  - {name}")
                else:
                    print(f"Response structure: {type(data)}")
            else:
                print(f"Error: {response.text[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
        print()

def main():
    parser = argparse.ArgumentParser(description='Test Codacy API endpoints for listing repositories')
    parser.add_argument('--token', required=True, help='Codacy API token')
    parser.add_argument('--provider', default='gh', help='Git provider (gh, gl, etc.)')
    parser.add_argument('--organization', required=True, help='Organization name')
    parser.add_argument('--baseurl', default='https://app.codacy.com', help='Codacy base URL')
    
    args = parser.parse_args()
    
    print(f"Testing repository listing for {args.provider}/{args.organization}")
    print(f"Base URL: {args.baseurl}")
    print("="*60)
    
    test_list_repositories(args.baseurl, args.provider, args.organization, args.token)

if __name__ == "__main__":
    main()
