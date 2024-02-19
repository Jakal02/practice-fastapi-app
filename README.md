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
