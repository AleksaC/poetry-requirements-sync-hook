from setuptools import setup

from poetry_requirements_sync import __version__


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="poetry-requirements-sync",
    version=__version__,
    author="Aleksa Ćuković",
    author_email="aleksacukovic1@gmail.com",
    description="git pre-commit hook for syncing pyproject.toml with requirements.txt",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/AleksaC/poetry-requirements-sync-hook",
    license="MIT",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    packages=["poetry_requirements_sync"],
    entry_points={
        "console_scripts": ["sync-requirements = poetry_requirements_sync.sync:main"]
    },
)
