import sys

from log_repo_history import RepoHistory

path = sys.argv[1]

repoHistory = RepoHistory(path)
print(repoHistory.get_authors_with_commits())