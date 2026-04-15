---
sidebar_position: 4
title: Architecture
description: Layers and main packages in the Agentic Web Starter codebase.
---

# Architecture

This page explains how the codebase is structured, how a request flows through the system, and
where to find each type of logic.  Understanding the layered design makes it much easier to add
new features without breaking existing ones.

---

## Request flow

Every HTTP request follows the same path through the application:

```
Client
  └─▶ Routes          (app/routes/)         — parse request, inject deps, format response
        └─▶ Services  (app/services/)        — business logic, orchestration, ACL checks
              └─▶ Repositories (app/repository/) — data access: SQL, Qdrant, Redis
```

Each layer has a single responsibility.  **Routes never contain business logic**, and **services
never talk directly to a database** — they always go through a repository.

---

## Layer responsibilities

### Routes — `app/routes/`

HTTP adapters only.  A route handler should do nothing more than:

1. Parse and validate the incoming request (FastAPI handles this via Pydantic schemas).
2. Call the appropriate service method.
3. Return a formatted response.

There are two route groups:

| Package | Handles |
|---------|---------|
| `app/routes/core_routes/` | Chat (`/api/v1/chat`) and document ingestion (`/api/v1/upload`) |
| `app/routes/iam_routes/` | Auth, users, and roles — **only registered when `USE_SQL=true`** |

---

### Services — `app/services/`

Business rules live here.  Services orchestrate calls to repositories, apply ACL checks, and
raise domain exceptions when something goes wrong.

| Package | Purpose |
|---------|---------|
| `core_services/` | Ingestion pipeline, RAG chat, agent orchestration |
| `iam_services/` | Authentication, user/role CRUD, admin bootstrap |
| `message_queue_services/` | Publishing ingestion jobs to RabbitMQ |

---

### Repositories — `app/repository/`

The only place that touches a data store directly.  Services call repository methods; they never
write raw queries or SDK calls themselves.

| Package | Store |
|---------|-------|
| `sql_repository/` | SQLite — users, roles, components, ACL mappings |
| `vector_repository/` | Qdrant — document chunk embeddings |

---

### Utilities — `app/utils/`

Shared helpers that do not belong in a specific service.

| Package | Contains |
|---------|---------|
| `core_utils/` | File handling, embedding calls, Redis helpers, DB session helpers |
| `iam_utils/` | JWT creation and validation, Argon2 password hashing, FastAPI auth dependencies |

---

## Application entry points

| File | Role |
|------|------|
| `app/main.py` | ASGI entry point — used by Uvicorn and Gunicorn |
| `app/starter.py` | Builds the `FastAPI` app: CORS, exception handlers, router registration, startup tasks |

`app/starter.py` is where feature flags (`USE_SQL`, `USE_QDRANT`, etc.) control which routers are
mounted at startup.

---

## Agents and tools

The agentic layer sits on top of the service layer:

| Package | Purpose |
|---------|---------|
| `app/agents/` | Supervisor and retriever agents; all agents extend `BaseAgent` |
| `app/tools/` | LangChain tools for indexing and retrieval; all tools subclass `BaseTool` |
| `app/prompts/` | Prompt templates used by agents |

---

## Workers

`app/workers/ingestion_worker.py` runs as a separate process.  When `USE_RABBITMQ=true`, it
consumes the ingest queue and indexes documents into Qdrant asynchronously — decoupling the
upload response time from the indexing operation.

---

## Error handling

All domain errors are defined in `app/exceptions/domain.py` and extend a common `AppError` base.
Global handlers in `app/exceptions/handlers.py` translate them into consistent JSON responses.

Never raise raw `Exception`, `ValueError`, or FastAPI's `HTTPException` from services or
repositories — always use the custom hierarchy.

---

## Tests

Tests live under `app/tests/` and mirror the source structure.  Route-level tests use
`httpx.TestClient` with fixtures defined in `app/tests/conftest.py`.

---

## Further reading

- [Authentication & IAM](./authentication-and-iam) — JWT flow and ACL components in detail
- [Configuration](./configuration) — feature flags and environment variables
- [Pull request guidelines](./pull-request-guidelines) — code rules that enforce this architecture
