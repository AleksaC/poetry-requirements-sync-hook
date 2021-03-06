# poetry-requirements-sync-hook

Pre-commit hook for syncing `pyproject.toml` with `requirements.txt`

## About

Recently I've switched over to poetry for some of my projects and I mostly like
it so far. However even in those projects it is often be useful to include
`requirements.txt` file (e.g. for building Docker images). Poetry makes it easy
to to do that, but you need to explicitly run a command to do it. Over time this
usually leads to `requirements.txt` not being up to date with all the packages 
installed using poetry. For this reason I've decided to create a pre-commit hook
that will update `requirements.txt` each time `pyproject.toml` gets updated with
a dependency. 

### Options
By default the hook doesn't include dev dependencies and it includes hashes. The
main reason for this is that this is how `poetry`'s export works by default. 
Like `poetry` you can modify this by adding `--dev` and `--without-hashes` args.
The hook autmatically fixes the inconsistencies and can be configured to 
automatically stage the fixes by adding `--auto-add` argument.

**Note**: For the hook to work you need to have `poetry` installed.

## Usage
You can use the hook by renaming the `sync.py` file to `pre-commit` and moving
it to `.git/hooks/`. Assuming you are in the root of your project and have 
already initialized a git repo you can use the following command:
```shell script
wget https://raw.githubusercontent.com/AleksaC/poetry-requirements-sync-hook/master/poetry_requirements_sync/sync.py -O .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
``` 

### With [pre-commit](https://pre-commit.com/)
Add the following lines to `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/AleksaC/poetry-requirements-sync-hook
    rev: master
    hooks:
      - id: poetry-requirements-sync
        args: [--dev, --without-hashes, --auto-add]
```
