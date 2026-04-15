---
sidebar_position: 2
title: Getting started
description: Environment setup, Docker, and running the API locally.
---

# Getting started

This page walks you from a fresh clone to a running API in three steps.  
If you run into trouble, check the [Configuration](./configuration) page for a full
variable reference or open an issue.

---

## Prerequisites

Before you begin, make sure you have the following installed:

| Requirement | Notes |
|-------------|-------|
| **Python 3.11** | See `pyproject.toml` for the supported range |
| **Docker & Docker Compose** | Required for the recommended setup |
| **OpenAI or Gemini API key** | At least one is needed for the chat endpoint |

---

## Step 1 — Configure your environment

Copy the example file and fill in your values:

```bash
cp env.example .env
```

Open `.env` in your editor.  The most important variables to set right away are:

| Variable | Why it matters |
|----------|----------------|
| `OPENAI_API_KEY` or `GEMINI_API_KEY` | Powers the chat endpoint |
| `JWT_SECRET_KEY` | Signs tokens — required when `USE_SQL=true` |
| `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` | Creates a first admin user on startup |

See [Configuration](./configuration) for the full list.

**Never commit `.env` to version control.** It is already in `.gitignore`, but double-check before pushing.

---

## Step 2 — Start the service

### Option A — Docker Compose (recommended)

This starts the API, ingestion worker, Qdrant, Redis, and RabbitMQ in one command:

```bash
docker compose up --build
```

The API is available at **http://localhost:8000**.  
Open **http://localhost:8000/docs** for interactive Swagger UI.

Other useful commands:

```bash
docker compose up -d --build   # run in the background (detached)
docker compose down            # stop all services
docker compose run tests       # run the full test suite inside Docker
```

### Option B — Local Python with Docker dependencies

Use this if you want faster reload cycles during development.

**1. Start only the backing services:**

```bash
docker compose up -d qdrant redis rabbitmq
```

Then update your `.env` so the local API can reach the containers:

```
QDRANT_HOST=localhost
REDIS_HOST=localhost
RABBITMQ_HOST=localhost
```

**2. Bootstrap your Python environment (run once per clone):**

```bash
make setup
```

This creates `.venv`, installs all dev dependencies, and registers the pre-commit, pre-push, and
commit-msg hooks automatically.

**Manual setup (without Make):**

```bash
python3.11 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pre-commit install
pre-commit install --hook-type pre-push
pre-commit install --hook-type commit-msg
```

**3. Start the API:**

```bash
uvicorn app.main:app --reload
```

Or production-style with Gunicorn:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**4. Start the ingestion worker (only when `USE_RABBITMQ=true`):**

Open a second terminal and run:

```bash
python -m app.workers.ingestion_worker
```

---

## Step 3 — Verify everything is working

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

Then open **http://localhost:8000/docs** to explore the full API interactively.

---

## Running tests

```bash
# Recommended — full stack inside Docker, no local deps required
docker compose run tests

# Locally — requires Qdrant and Redis to be running
pytest -q app/tests
```

---

## Next steps

- [Configuration](./configuration) — understand every env variable and feature flag
- [Architecture](./architecture) — learn how the layers fit together
- [API reference](./api-reference) — endpoint list with request/response examples
