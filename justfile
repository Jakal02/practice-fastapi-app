set dotenv-load := true

@ruff:
    poetry run ruff check .

@tests: start-databases-detached && stop-databases
    sleep 1
    poetry run alembic downgrade base
    poetry run alembic upgrade head
    poetry run pytest
    poetry run alembic downgrade base

@start-databases-detached:
    docker compose up -d

@stop-databases:
    docker compose down
