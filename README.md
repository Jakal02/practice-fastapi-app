# practice-fastapi-app
Practice building a FastAPI using best practices for CI/CD.

Here are all of the goals for this repository:

Behavior:  
1. Create a workflow that makes sure PRs have labels
    - Done
    - ~~Create a PR labeler to automatically tag PRs by the name~~
        - This proved to not be productive. Tags should be added manually.

2. Create a release drafter workflow
    - Done. After every PR, the title is added to a section in the release notes relating to the tag attached to the PR.
3. Set up precommit for the FastAPI app
    - Done
4. Create a FastAPI app that allows CRUD of Posts
    - [X] ~~Setup alembic to connect to sqlite database (ignore prod DB considerations for now)~~
        - Set up postgres connection via docker image
    - [X] Set up reading config file to load envrionment variables
        - no using `os.environ.get()`
    - [X] Create code for Post table using sqlalchemy
    - [X] Update database via alembic
    - [X] Add CRUD routes for Post
    - [X] Introduce ghost delete functionality
    - [X] Make API async. Test the async functionality

5. Connect FastAPI to Meilisearch
    - [X] create async process that runs continuously every few seconds
            - create route to inspect async process
    - [X] configure meilisearch via docker
    - [X] print to terminal updates made to posts during async process
            - create CRUD function to get all posts not ghost deleted.
    - [ ] update meilisearch index with changes made to posts
    - [ ] remove posts from index when post is deleted for real

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

### Database Local Setup

To instantiate the database, run:
```bash
just start-postgres-detached
```

To create all the relevant database tables, you must run all of the alembic migrations.

```bash
poetry run alembic ugrade head
```

To close the database run the following command (NOTE: this deletes the database.)
```bash
just stop-postgres
```

### Continuous Integration with Just

Just helps run command line commands. Follow [the instructions](https://github.com/casey/just?tab=readme-ov-file#installation) to install it. If you're on a WSL Unbuntu 22.04 system. Follow the instructions to setup [PreBuilt-MPR](https://docs.makedeb.org/prebuilt-mpr/getting-started/#setting-up-the-repository)

Now, to run any of the recipes specified in the `justfile`, just open your command line and run `just RECIPE`. For example, to run pytest, run:
```bash
just tests
```

## Acknowledgements:

Lots of the development in this repository was based off of the work done in [this repo](https://github.com/sanders41/meilisearch-fastapi).
And [this one](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master)


## Notes

# Limitations of current design:

- I don't know how to test the continuous async process that keeps the search index in-sync with the database.
    1. Because the pytest environment runs unit tests. I don't think starting the httpx AsyncClient starts the async process
    2. The true_delete route for posts calls meilisearch directly and then deletes it.
- I am using the current .env files for running the API locally for testing also. They are not fully decoupled like they should be!
- I do not know the best design practice for supporting the permanently running background task of syncing the search index to the database.
    - Should it be an external process? (Some super-process will start the API and this process)
    - Is the design I have good practice already? If so, there is probably a nuance I am missing still
- I do like the ghost_delete aspect, but supporting true deletes feels incomplete currently
    - Because true deletes have to delete from the database and search index at the same time
    - Real root of the problem is I don't have a way to manage what has been deleted (hence ghost delete, but this also helps keep data)
