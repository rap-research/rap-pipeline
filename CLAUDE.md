# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**rap-pipeline** is an Apache Airflow-based data pipeline for automatically collecting academic papers from arXiv and updating citation counts via the Semantic Scholar API.

Planned DAGs:
- `collect_papers_dag` — daily at 02:00 UTC: collect arXiv papers, generate embeddings, apply tags
- `update_citations_dag` — daily at 03:00 UTC: update citation counts via Semantic Scholar API

## Setup

```bash
# Create virtual environment and install Airflow (Python 3.13)
uv venv && source .venv/bin/activate
AIRFLOW_VERSION=3.1.3
PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
uv pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
uv sync

# Copy and configure environment variables
cp .env.example .env
```

## Commands

```bash
make up        # Start Airflow standalone (sets AIRFLOW_HOME=.airflow, runs airflow standalone)
make down      # Kill Airflow processes
make restart   # Restart Airflow
make logs      # Tail scheduler logs
```

Airflow web UI runs on `localhost:8081` by default. Initial credentials are in `.airflow/simple_auth_manager_passwords.json.generated`.

## Architecture

```
dags/          # Airflow DAG definitions
pipeline/
  collect/     # arXiv paper collection logic
  process/     # Embedding and tagging logic
  export/      # Data export logic
.airflow/      # Airflow metadata (auto-generated, git-excluded): SQLite DB, logs, config
```

DAG files go in `dags/`. Pipeline business logic lives in `pipeline/` and is imported by DAGs.

## Key Constraints

- **Semantic Scholar API**: max 100 requests/5 minutes — use 3-second delays between requests
- **arXiv API**: recommend 3-second delays between requests
- **Database**: SQLite for local dev (`.airflow/airflow.db`); use PostgreSQL + pgvector in production
- **Environment**: `AIRFLOW_HOME` is set to `.airflow/` (not the default `~/airflow`)