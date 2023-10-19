from github import Github
import os

# Authenticate with your personal access token
g = Github(os.environ["ACCESS_TOKEN"])

# Get the repository
repo = g.get_repo("Abhijith14/Project-SmartGitAuto-v2")

# Get the secrets
secrets = repo.get_secrets()

# Print the secrets and their values
for secret in secrets:
    print(secret.name, "=", secret.created_at, "=", secret.updated_at, "=", secret.url)
