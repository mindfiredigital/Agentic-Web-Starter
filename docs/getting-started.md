---
sidebar_position: 2
title: Getting started
description: Environment setup, Docker, and running the API locally.
---

# Getting started

## Prerequisites

- **Python 3.11** (see `pyproject.toml` for the supported range)
- **Docker** and **Docker Compose** for the recommended stack
- API keys: at least one of **OpenAI** or **Gemini** for chat (see `env.example`)

## 1. Configure environment

```bash
cp env.example .env
```

Edit `.env` for your environment. Important variables are summarized in [Configuration](./configuration).

## 2. Run with Docker (recommended)

From the repository root:

```bash
docker compose up --build
```

The API is served at **http://localhost:8000** (Gunicorn + Uvicorn workers). Use `docker compose up -d --build` to run detached.

Included services typically include the API, ingestion worker (when RabbitMQ is used), Qdrant, Redis, and RabbitMQ. See `docker-compose.yml` for service names.

**Run tests in Docker:**

```bash
docker compose run tests
```

## 3. Run the API locally (dependencies in Docker)

Start backing services only:

```bash
docker compose up -d qdrant redis rabbitmq
```

Point `.env` at localhost (`QDRANT_HOST`, `REDIS_HOST`, `RABBITMQ_HOST`, etc.).

Bootstrap Python (once):

```bash
make setup
```

Or manually: create `.venv`, `pip install -e ".[dev]"`, and install pre-commit hooks as in the root `README.md`.

Start the app:

```bash
uvicorn app.main:app --reload
```

If `USE_RABBITMQ=true`, run the ingestion worker in another terminal:

```bash
python -m app.workers.ingestion_worker
```

## 4. Documentation site (this handbook)

```bash
make docs
```

Or: `cd website && npm install && npm start` — usually **http://localhost:3000**.

## Next steps

- [Configuration](./configuration) — flags and env vars
- [API reference](./api-reference) — OpenAPI URL
