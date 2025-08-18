# Codacy Repository Tools

A collection of Python scripts for managing repositories in Codacy. This toolkit includes tools for both following repositories and bulk adding repositories to your Codacy organization.

## Tools Included

### 1. Repository Auto-Follow (`codacy_follow.py`)
Automates the process of following repositories in Codacy. It can follow all repositories in an organization or specific ones you select.

### 2. Bulk Repository Add (`codacy_bulk_add.py`)
Bulk adds repositories from your organization to Codacy and configures integration settings. Uses Codacy's organization endpoint to discover repositories automatically - no CSV file required.

## Features

### Repository Auto-Follow (`codacy_follow.py`)
- Follow all repositories in an organization or select specific ones
- Automatic pagination handling for large organizations
- Detailed logging with debug mode option
- Success/failure tracking for each repository
- URL encoding for special characters in repository names
- Validates repository names before attempting to follow
- Comprehensive error handling and reporting

### Bulk Repository Add (`codacy_bulk_add.py`)
- Automatically discovers repositories using Codacy's organization endpoint
- Bulk adds repositories to Codacy with a single command
- Configures integration settings (disables all integrations by default)
- Handles repositories that already exist gracefully
- Dry-run mode to preview changes before execution
- Rate limiting to avoid API throttling
- Comprehensive error handling and detailed logging
- Selective repository processing with `--reponames` option

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

### Repository Auto-Follow (`codacy_follow.py`)

#### Basic Usage
```bash
python codacy_follow.py --token YOUR_API_TOKEN --provider PROVIDER --organization ORG_NAME
```

#### Follow Specific Repositories
```bash
python codacy_follow.py --token YOUR_API_TOKEN --provider PROVIDER --organization ORG_NAME --reponames "repo1,repo2,repo3"
```

#### Enable Debug Mode
```bash
python codacy_follow.py --token YOUR_API_TOKEN --provider PROVIDER --organization ORG_NAME --debug
```

#### Command Line Arguments
- `--token`: (Required) Your Codacy API token
- `--provider`: (Required) Git provider code (e.g., 'gh' for GitHub, 'gl' for GitLab)
- `--organization`: (Required) Your organization name
- `--baseurl`: (Optional) Codacy server address (default: 'https://app.codacy.com')
- `--reponames`: (Optional) Comma-separated list of specific repositories to follow
- `--debug`: (Optional) Enable debug logging

### Bulk Repository Add (`codacy_bulk_add.py`)

#### Basic Usage (with defaults)
```bash
python codacy_bulk_add.py --token YOUR_API_TOKEN --organization ORG_NAME
```

#### Full Usage Example
```bash
python codacy_bulk_add.py --token YOUR_API_TOKEN --provider gh --organization ORG_NAME --baseurl https://app.codacy.com --debug
```

#### Dry Run Mode (Preview Changes)
```bash
python codacy_bulk_add.py --token YOUR_API_TOKEN --organization ORG_NAME --dry-run
```

#### Add Specific Repositories Only
```bash
python codacy_bulk_add.py --token YOUR_API_TOKEN --organization ORG_NAME --reponames "repo1,repo2,repo3"
```

#### Command Line Arguments
- `--token`: (Required) Your Codacy API token
- `--organization`: (Required) Your organization name
- `--provider`: (Optional) Git provider code - default: 'gh' (GitHub)
- `--baseurl`: (Optional) Codacy server address - default: 'https://app.codacy.com'
- `--reponames`: (Optional) Comma-separated list of specific repositories to add
- `--dry-run`: (Optional) Preview what would be added without making actual changes
- `--debug`: (Optional) Enable debug logging

## Output

Both scripts provide:
- Progress updates for each repository
- Success/failure status for each operation
- Summary of total successes and failures
- Execution time
- Detailed logs in debug mode

### Example Output - Repository Follow

```
2024-01-12 10:00:01 - INFO - Starting script with provider: gh, organization: myorg
2024-01-12 10:00:02 - INFO - Retrieved 25 repositories
2024-01-12 10:00:03 - INFO - Successfully followed repo1
2024-01-12 10:00:03 - INFO - Successfully followed repo2
2024-01-12 10:00:04 - INFO - Script completed in 3.45 seconds
2024-01-12 10:00:04 - INFO - Successfully followed 2 repositories
```

### Example Output - Bulk Repository Add

```
2024-01-12 10:00:01 - INFO - Starting bulk add with provider: gh, organization: myorg
2024-01-12 10:00:02 - INFO - Total repositories found: 25
2024-01-12 10:00:02 - INFO - Processing all repositories
2024-01-12 10:00:03 - INFO - Processing repository 1/25: repo1
2024-01-12 10:00:03 - INFO - Successfully added repo1
2024-01-12 10:00:04 - INFO - Successfully updated integration settings for repo1
2024-01-12 10:00:06 - INFO - Processing repository 2/25: repo2
2024-01-12 10:00:06 - WARNING - Repository repo2 already exists
2024-01-12 10:00:07 - INFO - ==================================================
2024-01-12 10:00:07 - INFO - Script completed in 45.67 seconds
2024-01-12 10:00:07 - INFO - Successfully added 24 repositories
2024-01-12 10:00:07 - INFO - Skipped 1 repositories (already exist)
2024-01-12 10:00:07 - INFO - ==================================================
```

## Error Handling

Both scripts handle various error scenarios:
- Invalid API tokens
- Network connectivity issues
- Rate limiting
- Invalid repository names
- Malformed API responses
- Permission issues
- Repositories that already exist (bulk add tool)
- Integration settings update failures (bulk add tool)

All errors are logged with appropriate detail level based on the debug setting.

## Integration Settings

The bulk add tool (`codacy_bulk_add.py`) automatically configures integration settings for each added repository. By default, all integrations are disabled:

- **Commit Status**: Disabled
- **Pull Request Comments**: Disabled
- **Pull Request Summary**: Disabled
- **Coverage Summary**: Disabled
- **Suggestions**: Disabled
- **AI Enhanced Comments**: Disabled

This ensures a clean setup where you can selectively enable integrations as needed.

## Exit Codes

- 0: All operations completed successfully
- 1: One or more operations failed

## Best Practices

1. **Security**: Use environment variables for sensitive information like API tokens
2. **Testing**: Enable debug mode when troubleshooting
3. **Gradual Rollout**: Test with a small set of repositories first using `--reponames`
4. **Rate Limiting**: Monitor rate limits when dealing with large organizations
5. **Dry Run**: Use `--dry-run` mode with the bulk add tool to preview changes
6. **Backup**: Consider backing up your current Codacy configuration before bulk operations

## Security Considerations

- Store API tokens securely
- Use minimal required permissions for API tokens
- Consider using a dedicated service account
- Review logs for sensitive information before sharing

## Troubleshooting

Common issues and solutions:

1. **Rate Limiting**
   - The bulk add tool includes automatic 2-second delays between requests
   - Check API quotas in your Codacy account
   - Consider processing repositories in smaller batches using `--reponames`

2. **Permission Errors**
   - Verify API token permissions
   - Check organization access
   - Verify repository visibility
   - Ensure token has repository management permissions for bulk add operations

3. **Connection Issues**
   - Check network connectivity
   - Verify base URL (default: https://app.codacy.com)
   - Check proxy settings

4. **Repository Already Exists (Bulk Add)**
   - This is normal behavior - the tool will skip existing repositories
   - Use `--dry-run` to see which repositories would be processed
   - Check the summary report for details on skipped repositories

5. **Integration Settings Failures**
   - Repository may be added successfully but integration settings update may fail
   - Check the logs for specific error messages
   - You can manually configure integration settings in the Codacy UI if needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues with:
- Codacy API: Visit the [Codacy API documentation](https://api.codacy.com/docs)
- This script: Open an issue in the repository

## Changelog

### v2.0.0
- Added bulk repository add tool (`codacy_bulk_add.py`)
- Automatic repository discovery using Codacy's organization endpoint
- Integration settings configuration with sensible defaults
- Dry-run mode for safe testing
- Enhanced error handling for bulk operations
- Rate limiting to prevent API throttling

### v1.0.0
- Initial release with repository auto-follow functionality
- Added support for specific repository selection
- Implemented comprehensive error handling
- Added debug mode
- Added success/failure tracking
