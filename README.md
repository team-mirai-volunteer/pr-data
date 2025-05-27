# PR Data Repository

This repository stores PR data from the team-mirai/policy repository in a file-per-PR format. It is designed to separate data storage from code, ensuring that data updates don't pollute the code repository's commit history.

## Repository Structure

```
pr-data/
├── prs/                  # Individual PR data files
│   ├── 1.json            # PR #1 data
│   ├── 2.json            # PR #2 data
│   └── ...
├── indexes/              # Index files for quick access
│   ├── by_label/         # PRs grouped by label
│   │   ├── education.json
│   │   └── ...
│   └── by_section/       # PRs grouped by section
│       ├── section1.json
│       └── ...
├── reports/              # Generated reports
│   ├── labels/           # Label-based reports
│   │   ├── education.md
│   │   └── ...
│   └── sections/         # Section-based reports
│       ├── section1.md
│       └── ...
└── scripts/              # Utility scripts
    ├── migrate_data.py   # Data migration script
    └── README.md         # Script documentation
```

## Data Migration

The `scripts/migrate_data.py` script converts the original merged_prs_data.json to the file-per-PR format:

```bash
python scripts/migrate_data.py --input /path/to/merged_prs_data.json --output-dir .
```

## GitHub Actions Workflow

This repository is updated hourly by a GitHub Actions workflow that:

1. Fetches PR data using the pr_analysis repository code
2. Generates label and section reports
3. Commits and pushes changes to this repository

## Required Secrets

For the GitHub Actions workflow to function properly, the following secrets need to be configured:

- `GITHUB_TOKEN`: For GitHub API access
- `GH_TOKEN`: For repository checkout

## Related Repositories

- [team-mirai-volunteer/pr_analysis](https://github.com/team-mirai-volunteer/pr_analysis): Contains the code for PR data collection and analysis
- [team-mirai/policy](https://github.com/team-mirai/policy): The source repository for PR data
