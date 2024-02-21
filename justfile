set dotenv-load := true

@ruff:
    poetry run ruff check .

@tests: start-postgres-detached && stop-postgres
    - sleep 1
    - poetry run alembic upgrade head
    - poetry run pytest tests/crud/
    - poetry run alembic downgrade base

@start-postgres-detached:
    docker compose up -d

@stop-postgres:
    docker compose down
