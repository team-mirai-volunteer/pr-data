# Configuration Guide for PR Analysis System

This document provides instructions for configuring the PR analysis system to work with the new file-per-PR data structure.

## PR Analysis Repository Configuration

The `team-mirai-volunteer/pr_analysis` repository needs to be configured to work with the new data structure in `team-mirai-volunteer/pr-data`. The main configuration file is located at `config/settings.yaml`.

### Example Configuration

```yaml
github:
  repo_owner: "team-mirai"
  repo_name: "policy"
  token_env_var: "GITHUB_TOKEN"
  api_base_url: "https://api.github.com"

data:
  storage_type: "file_per_pr"  # Use file-per-PR storage format
  base_dir: "../pr-data"       # Path to pr-data repository
  prs_dir: "prs"               # Directory for PR data files
  indexes_dir: "indexes"       # Directory for index files
  reports_dir: "reports"       # Directory for report files

collectors:
  update_interval: 3600  # Update interval in seconds
  max_workers: 10        # Maximum number of worker threads
  retry_count: 3         # Number of retries for API requests

analyzers:
  section_analysis:
    enabled: true
    output_dir: "reports/sections"

generators:
  label_reports:
    enabled: true
    output_dir: "reports/labels"
```

## GitHub Actions Workflow

The GitHub Actions workflow in the `team-mirai-volunteer/pr-data` repository is configured to run hourly and update the PR data. The workflow file is located at `.github/workflows/hourly_update.yml`.

### Required Secrets

The workflow requires the following secrets to be configured in the repository settings:

1. **GITHUB_TOKEN**: This is automatically provided by GitHub Actions and is used for API access.

2. **GH_TOKEN**: This is a personal access token with repository access permissions. It is used for checking out repositories.

See [GitHub Actions Workflow Setup](github_actions_setup.md) for detailed instructions on setting up these secrets.

## Testing the Configuration

To test the configuration:

1. Clone both repositories:
   ```bash
   gh repo clone team-mirai-volunteer/pr_analysis
   gh repo clone team-mirai-volunteer/pr-data
   ```

2. Ensure the configuration in `pr_analysis/config/settings.yaml` points to the correct paths.

3. Run the PR collector script:
   ```bash
   cd pr_analysis
   python src/collectors/pr_collector_main.py --config config/settings.yaml --output-dir ../pr-data/prs
   ```

4. Verify that PR data files are created in the `pr-data/prs` directory.

5. Run the label report generator:
   ```bash
   python src/generators/label_report_main.py --config config/settings.yaml --input-dir ../pr-data/prs --output-dir ../pr-data/reports/labels
   ```

6. Run the section analyzer:
   ```bash
   python src/analyzers/section_analyzer_main.py --config config/settings.yaml --input-dir ../pr-data/prs --output-dir ../pr-data/reports/sections
   ```

7. Verify that reports are generated in the appropriate directories.

## Troubleshooting

If you encounter issues:

1. Check that the GitHub token has the necessary permissions.
2. Verify that the paths in the configuration file are correct.
3. Ensure that both repositories are properly cloned and accessible.
4. Check the logs for specific error messages.

For more detailed information, refer to the documentation in the respective repositories.
