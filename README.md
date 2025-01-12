# Codacy Repository Auto-Follow Script

A Python script that automates the process of following repositories in Codacy. It can follow all repositories in an organization or specific ones you select, with comprehensive error handling and logging capabilities.

## Features

- Follow all repositories in an organization or select specific ones
- Automatic pagination handling for large organizations
- Detailed logging with debug mode option
- Success/failure tracking for each repository
- URL encoding for special characters in repository names
- Validates repository names before attempting to follow
- Comprehensive error handling and reporting

## Prerequisites

- Python 3.x
- Required Python packages:
  - requests
  - urllib3

## Installation

1. Clone this repository or download the script
2. Install the required dependencies:
   ```bash
   pip install requests
   ```

## Usage

### Basic Usage

```bash
python codacy_follow.py --token YOUR_API_TOKEN --provider PROVIDER --organization ORG_NAME
```

### Follow Specific Repositories

```bash
python codacy_follow.py --token YOUR_API_TOKEN --provider PROVIDER --organization ORG_NAME --reponames "repo1,repo2,repo3"
```

### Enable Debug Mode

```bash
python codacy_follow.py --token YOUR_API_TOKEN --provider PROVIDER --organization ORG_NAME --debug
```

### Command Line Arguments

- `--token`: (Required) Your Codacy API token
- `--provider`: (Required) Git provider code (e.g., 'gh' for GitHub, 'gl' for GitLab)
- `--organization`: (Required) Your organization name
- `--baseurl`: (Optional) Codacy server address (default: 'https://app.codacy.com')
- `--reponames`: (Optional) Comma-separated list of specific repositories to follow
- `--debug`: (Optional) Enable debug logging

## Output

The script provides:
- Progress updates for each repository
- Success/failure status for each operation
- Summary of total successes and failures
- Execution time
- Detailed logs in debug mode

### Example Output

```
2024-01-12 10:00:01 - INFO - Starting script with provider: gh, organization: myorg
2024-01-12 10:00:02 - INFO - Retrieved 25 repositories
2024-01-12 10:00:03 - INFO - Successfully followed repo1
2024-01-12 10:00:03 - INFO - Successfully followed repo2
2024-01-12 10:00:04 - INFO - Script completed in 3.45 seconds
2024-01-12 10:00:04 - INFO - Successfully followed 2 repositories
```

## Error Handling

The script handles various error scenarios:
- Invalid API tokens
- Network connectivity issues
- Rate limiting
- Invalid repository names
- Malformed API responses
- Permission issues

All errors are logged with appropriate detail level based on the debug setting.

## Exit Codes

- 0: All operations completed successfully
- 1: One or more operations failed

## Best Practices

1. Use environment variables for sensitive information like API tokens
2. Enable debug mode when troubleshooting
3. Test with a small set of repositories first
4. Monitor rate limits when dealing with large organizations

## Security Considerations

- Store API tokens securely
- Use minimal required permissions for API tokens
- Consider using a dedicated service account
- Review logs for sensitive information before sharing

## Troubleshooting

Common issues and solutions:

1. Rate Limiting
   - Reduce concurrent requests
   - Check API quotas
   - Implement retry mechanism

2. Permission Errors
   - Verify API token permissions
   - Check organization access
   - Verify repository visibility

3. Connection Issues
   - Check network connectivity
   - Verify base URL
   - Check proxy settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues with:
- Codacy API: Visit the [Codacy API documentation](https://api.codacy.com/docs)
- This script: Open an issue in the repository

## Changelog

### v1.0.0
- Initial release with merged functionality
- Added support for specific repository selection
- Implemented comprehensive error handling
- Added debug mode
- Added success/failure tracking