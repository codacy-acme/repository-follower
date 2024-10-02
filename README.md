# Codacy Integration Helper

## Overview

The Codacy Integration Helper is a Python script designed to automate the process of following repositories in Codacy. It uses the Codacy API to list all repositories in a specified organization and then follows each repository, streamlining the setup process for large organizations or projects with numerous repositories.

## Features

- List all repositories in a Codacy organization
- Follow all repositories or a specified subset
- Support for multiple Git providers (GitHub, GitLab, Bitbucket)
- Pagination handling for organizations with many repositories
- Customizable base URL for self-hosted Codacy instances

## Prerequisites

- Python 3.6 or higher
- `requests` library (can be installed via pip)
- Codacy API token with appropriate permissions

## Installation

1. Clone this repository or download the script file.
2. Install the required Python library:

   ```
   pip install requests
   ```

## Usage

Run the script from the command line with the following syntax:

```
python follow-repo.py --token YOUR_CODACY_TOKEN --provider PROVIDER --organization ORG_NAME [OPTIONS]
```

### Required Arguments

- `--token`: Your Codacy API token
- `--provider`: Git provider (use 'gh' for GitHub, 'gl' for GitLab, 'bb' for Bitbucket)
- `--organization`: Your organization name in Codacy

### Optional Arguments

- `--reponame`: Comma-separated list of specific repositories to follow (if omitted, all repositories will be followed)
- `--baseurl`: Codacy server address (default is 'https://app.codacy.com', change for self-hosted instances)

### Examples

Follow all repositories in a GitHub organization:
```
python follow-repo.py.py --token YOUR_TOKEN --provider gh --organization YOUR_ORG
```

Follow specific repositories in a GitLab organization:
```
python follow-repo.py.py --token YOUR_TOKEN --provider gl --organization YOUR_ORG --reponame repo1,repo2,repo3
```

Use with a self-hosted Codacy instance:
```
python follow-repo.py.py --token YOUR_TOKEN --provider bb --organization YOUR_ORG --baseurl https://codacy.your-domain.com
```

## Notes

- Ensure your Codacy API token has the necessary permissions to list and follow repositories.
- For large organizations, the script may take some time to run as it processes each repository sequentially.
- The script uses pagination to handle organizations with more than the default number of repositories returned by the API.

## Troubleshooting

- If you encounter authentication errors, verify that your API token is correct and has the necessary permissions.
- For issues with specific repositories, check that they exist and that you have the required access rights.
- If the script fails to list repositories after recent permission changes, use the Codacy API's cleanCache endpoint to refresh the repository list.