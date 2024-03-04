set dotenv-load := true

@ruff:
    poetry run ruff check .

@tests: start-databases-detached && stop-databases
    poetry run alembic downgrade base
    poetry run alembic upgrade head
    poetry run pytest
    poetry run alembic downgrade base

@start-databases-detached:
    docker compose up -d
    sleep 1

@stop-databases:
    docker compose down

@api-startup: start-databases-detached
    poetry run alembic upgrade head
    poetry run uvicorn app.main:PracticeAPI --reload
