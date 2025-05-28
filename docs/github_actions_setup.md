# GitHub Actions Workflow Setup

This document provides instructions for setting up the GitHub Actions workflow for the PR analysis system.

## Repository Structure

- **pr_analysis repository**: Contains all code, tests, and GitHub Actions workflows
- **pr-data repository**: Contains only data files (PR data, indexes, and reports)

## Required Secrets

The workflow requires the following secrets to be configured in the pr_analysis repository settings:

1. **GITHUB_TOKEN**: This is automatically provided by GitHub Actions and is used for API access.

2. **GH_TOKEN**: This is a personal access token with repository access permissions. It is used for checking out repositories.

### Setting Up GH_TOKEN

1. Go to your GitHub account settings
2. Navigate to Developer settings > Personal access tokens > Fine-grained tokens
3. Click "Generate new token"
4. Give the token a descriptive name (e.g., "PR Analysis Workflow")
5. Set the expiration as needed
6. Select the repositories that need access (team-mirai-volunteer/pr_analysis and team-mirai-volunteer/pr-data)
7. Under "Repository permissions", grant the following permissions:
   - Contents: Read and write
   - Pull requests: Read and write
   - Workflows: Read and write
8. Click "Generate token"
9. Copy the generated token

### Adding Secrets to the Repository

1. Go to the repository settings (team-mirai-volunteer/pr_analysis)
2. Navigate to Secrets and variables > Actions
3. Click "New repository secret"
4. Add the GH_TOKEN secret:
   - Name: GH_TOKEN
   - Value: [paste the token you generated]
5. Click "Add secret"

## Workflow Configuration

The workflow should be configured in the pr_analysis repository to run hourly and can also be triggered manually. The workflow file should be located at `.github/workflows/hourly_update.yml`.

### Manual Trigger

To manually trigger the workflow:

1. Go to the pr_analysis repository on GitHub
2. Navigate to the "Actions" tab
3. Select the "Hourly PR Data Update" workflow
4. Click "Run workflow"
5. Select the branch to run the workflow on
6. Click "Run workflow"

### Workflow Steps

The workflow performs the following steps:

1. Checks out the pr_analysis repository
2. Checks out the pr-data repository
3. Sets up Python
4. Installs dependencies
5. Runs the PR data collection script
6. Generates label reports
7. Generates section reports
8. Commits and pushes changes to the pr-data repository

## Troubleshooting

If the workflow fails, check the following:

1. Ensure that the GH_TOKEN secret is properly configured
2. Verify that the token has the necessary permissions
3. Check that the pr-data repository is accessible
4. Examine the workflow logs for specific error messages

For more detailed information, refer to the [GitHub Actions documentation](https://docs.github.com/en/actions).
