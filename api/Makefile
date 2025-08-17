.PHONY: help dev install clean test lint format

# Loads the .env file
ifneq (,$(wildcard .env))
    include .env
    export
endif

help:
	@echo "Available commands:"
	@echo "  make dev      - Start development server"
	@echo "  make install  - Install dependencies"
	@echo "  make clean    - Clean cache and temp files"
	@echo "  make test     - Run all tests"
	@echo "  make lint     - Run linting"
	@echo "  make format   - Format code (when implemented)"

dev:
	@echo "Starting server on port $(SERVER_PORT)."
	uv run uvicorn main:app --reload --host 0.0.0.0 --port $(SERVER_PORT)

install:
	@echo "Installing packages in virtual environment."
	uv sync

clean:
	@echo "Clean not implemented yet. Coming soon!"
	# find . -type d -name "__pycache__" -delete
	# find . -type f -name "*.pyc" -delete
	# find . -type d -name ".pytest_cache" -delete

test:
	@echo "Running all tests."
	uv run pytest tests/ -v

lint:
	@echo "Backend linting process started."
	uv run ruff check .

# Future: Format code
format:
	@echo "Formatting not implemented yet. Coming soon!"
	# uv run black .
	# uv run ruff format .
