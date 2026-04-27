# Variables
PYTHON = uv run
FLASK = $(PYTHON) flask
PYTEST = $(PYTHON) pytest

.PHONY: help install db-up db-down migrate db-init run test clean

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies using uv"
	@echo "  make db-up    - Start the PostgreSQL database via Docker"
	@echo "  make db-down  - Stop and remove the database container"
	@echo "  make migrate  - Apply database migrations"
	@echo "  make db-init  - Initialize migrations (only run once per project)"
	@echo "  make run      - Start the database, apply migrations, and run the dev server"
	@echo "  make test     - Run the test suite"
	@echo "  make clean    - Remove cache and temporary files"

install:
	uv sync --all-extras --dev

db-up:
	docker compose up -d db
	@echo "Waiting for database to be ready..."
	@sleep 3

db-down:
	docker compose down

db-init: db-up
	$(FLASK) db init
	$(FLASK) db migrate -m "Initial migration"
	$(FLASK) db upgrade

migrate: db-up
	$(FLASK) db upgrade

run: db-up migrate
	$(FLASK) run --debug

test:
	$(PYTEST) tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf .uv/