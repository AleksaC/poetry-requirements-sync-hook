# poetry-requirements-sync-hook
git pre-commit hook for removing pkg-resources from requirements.txt

## About


## Usage
You can use the hook by renaming the `sync.py` file to `pre-commit` and moving
it to `.git/hooks/`
### With [pre-commit](https://pre-commit.com/)
Add the following lines to `.pre-commit-config.yaml`
```yaml
repos:
-   repo: https://github.com/AleksaC/poetry-requirements-sync-hook
    rev: stable
    hooks:
    - id: poetry-requirements-sync
```
