---
sidebar_position: 4
title: Architecture
description: Layers and main packages in the Agentic Web Starter codebase.
---

# Architecture

## Layers

Requests follow a consistent path:

**Client → routes → services → repositories → SQLite / Qdrant / Redis**

- **Routes** (`app/routes/`) — HTTP adapters only: parsing, dependencies, response mapping. No business logic.
- **Services** (`app/services/`) — Business rules, orchestration, ACL checks (`core_services`, `iam_services`, `message_queue_services`).
- **Repositories** (`app/repository/`) — Data access: `sql_repository` (SQLite), `vector_repository` (Qdrant).
- **Utils** (`app/utils/`) — `core_utils` (files, embeddings, Redis, DB helpers), `iam_utils` (JWT, auth dependencies, password hashing).

Global errors use **`app/exceptions/domain.py`** and handlers in **`app/exceptions/handlers.py`**.

## Application entry

- **`app/main.py`** — ASGI entry (e.g. Uvicorn/Gunicorn).
- **`app/starter.py`** — Builds `FastAPI`, CORS, exception handlers, conditional IAM router (`USE_SQL`), core router, directories.

## Route packages

| Package | Responsibility |
|---------|----------------|
| `app/routes/core_routes/` | Chat, ingestion/upload |
| `app/routes/iam_routes/` | Auth, users, roles (registered only when `USE_SQL` is true) |

## Agents and tools

- **`app/agents/`** — Supervisor and retriever agents; extend **`BaseAgent`**.
- **`app/tools/`** — LangChain tools for indexing and retrieval.
- **`app/prompts/`** — Prompt templates for agents.

## Workers

- **`app/workers/ingestion_worker.py`** — Consumes the RabbitMQ ingest queue when async ingestion is enabled.

## Tests

- **`app/tests/`** — Pytest; route tests often use **`httpx`** with the FastAPI app from **`app/tests/conftest.py`**.

## Further reading

- [Authentication & IAM](./authentication-and-iam) — JWT and ACL components
- [Configuration](./configuration) — feature flags and env vars
