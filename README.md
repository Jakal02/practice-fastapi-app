# practice-fastapi-app
Practice building a FastAPI using best practices for CI/CD.

Here are all of the goals for this repository:

Behavior:
1. ~~Create a PR labeler to automatically tag PRs by the name~~
    - This proved to not be productive. Tags should be added manually.
2. Create a release drafter workflow
    - Done
3. Create a FastAPI app that allows CRUD of Posts
4. Set up precommit for the FastAPI app
5. Connect FastAPI to Meilisearch

## Setup

### Python App
This project uses Poetry to manage dependencies. Install it if you have not [here](https://python-poetry.org/docs/#installation).  

Install the project locally with:
```bash
poetry install
```

Ruff is used as a formatter and a linter for python code.

### Pre Commit

When adding pre-commit hooks to the yaml file, they then need to be installed to git. Run the below to do that:

```bash
poetry run pre-commit install
```

**NOTE: This WON'T run these new hooks on existing code.**  
To do that run the following command before your next commit:
```bash
poetry run pre-commit run --all-files
```

## Acknowledgements:

Lots of the development in this repository was based off of the work done in [this repo](https://github.com/sanders41/meilisearch-fastapi).
