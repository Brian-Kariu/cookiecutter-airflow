# Makefile for common-data-platform-data-pipelines dev workflows (no Hatch)

.PHONY: help init install install-airflow install-dbt install-test lint fmt type-check test coverage docs \
	airflow-up airflow-down airflow-init \
	airbyte-up airbyte-down \
	dbt-run dbt-test \
	clean

# === Helpers ===
help:             ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "[36m%-20s[0m %s", $$1, $$2}'

# === Environment setup ===
init:             ## Create & activate venv and install core deps
	@if [ -z "$$VIRTUAL_ENV_PATH" ]; then \
	    echo "VIRTUAL_ENV_PATH not set, creating .venv. You must have the require python version"; \
	    python{{cookiecutter.python_version}} -m venv .venv; \
	    VENV_PATH=.venv; \
	else \
	    echo "Using existing virtualenv at $$VIRTUAL_ENV_PATH"; \
	    VENV_PATH=$$VIRTUAL_ENV_PATH; \
	fi; \
	. $$VENV_PATH/bin/activate && . scripts/setup.sh; \
	echo "Setup up base dependencies."; \

install:          ## Install all optional groups (airflow, dbt, test)
	hatch env create
	echo "Installed all optional dependencies and hatch envs. Your current envs are: `hatch env show`"


install-airflow:  ## Install only Airflow dependencies
	hatch env create airflow
	echo "Installed all optional dependencies and airflow hatch envs. Your current envs are: `hatch env show`"

install-dbt:      ## Install only dbt dependencies
	hatch env create dbt
	echo "Installed all optional dependencies and dbt hatch envs. Your current envs are: `hatch env show`"

install-test:     ## Install only test dependencies
	hatch env create test
	echo "Installed all optional dependencies and test hatch envs. Your current envs are: `hatch env show`"

# === Linting, formatting, typing ===
lint:             ## Run ruff, sqlfluff, mypy
	ruff check

fmt:              ## Auto-format code
	ruff check --fix .

type-check:       ## Only mypy
	mypy airflow

# === Testing & Coverage ===
test:             ## Run tests via tox
	pytest

coverage:         ## Run tests & produce coverage report
	coverage run -m pytest
	coverage report

# === Documentation ===
docs:             ## Build Sphinx docs
	sphinx-build -b html docs/ docs/_build/html

# === Airflow local ===
airflow-init:     ## Initialize Airflow DB & users
	airflow db init
	airflow users create \
	  --username admin --firstname Admin --lastname User \
	  --role Admin --email admin@example.com

airflow-up:       ## Start Airflow webserver & scheduler
	airflow scheduler & \
	airflow webserver

airflow-down:     ## Stop all Airflow processes
	pkill -f "airflow webserver" || true
	pkill -f "airflow scheduler" || true

# === Cleanup ===
clean:            ## Remove Python artifacts and caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .venv
