#!/usr/bin/bash

echo "--- running ruff format ---"

# automatically format code
poetry run ruff format


echo "--- running ruff check ---"

# check with ruff linter
poetry run ruff check
