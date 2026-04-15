---
sidebar_position: 3
title: Configuration
description: Environment variables and feature flags loaded by app.config.env_config.Settings.
---

# Configuration

All settings are loaded at startup from the `Settings` class in `app/config/env_config.py`.
The singleton is available throughout the app as `settings`.

To configure the project:

```bash
cp env.example .env
# Edit .env with your values
```

**Never commit `.env`.** Use `env.example` for placeholder defaults — it is safe to commit.

---

## Feature flags

These four flags control which subsystems are active.  Each defaults to a sensible value so the
app runs without every dependency being present.

| Flag | Default | When set to `false` |
|------|---------|---------------------|
| `USE_QDRANT` | `true` | The upload/ingestion path is disabled; `/api/v1/upload` returns a configuration alert |
| `USE_REDIS` | `true` | Chat history falls back to in-memory storage (not persisted across restarts) |
| `USE_SQL` | `false` | SQLite is not initialised; `/auth`, `/users`, and `/roles` routes are not registered |
| `USE_RABBITMQ` | `false` | Ingestion happens inline (synchronous); the separate worker process is not needed |

You can run the service with all flags set to `false` for a minimal, dependency-free setup — useful for demos or quick local testing without Docker.

---

## API and project identity

These variables control the FastAPI app metadata and URL structure.

| Variable | Description |
|----------|-------------|
| `PROJECT_NAME` | Used in FastAPI metadata and as a sub-path under `WORKING_DIR` for uploads and logs |
| `PROJECT_VERSION` | Appears in the OpenAPI schema |
| `PROJECT_DESCRIPTION` | Appears in the OpenAPI schema |
| `BASE_PATH` | Root path when running behind a reverse proxy (e.g. `/agentic_web_starter`). Also shifts the OpenAPI URL. |
| `ALLOWED_ORIGINS` | Comma-separated list of CORS origins (e.g. `http://localhost:3000,https://myapp.com`) |
| `WORKING_DIR` | Base directory for uploads, logs, SQLite data, and HF cache (default: `./temp`) |

---

## LLM keys

At least one of the following is required for the chat endpoint to work.

| Variable | Provider |
|----------|---------|
| `OPENAI_API_KEY` | OpenAI (GPT-3.5, GPT-4, etc.) |
| `GEMINI_API_KEY` | Google Gemini |

If neither is set the API will start but chat requests will fail at the LLM call.

---

## Authentication — JWT

These variables are only relevant when `USE_SQL=true`.

| Variable | Description |
|----------|-------------|
| `JWT_SECRET_KEY` | Secret used to sign and verify tokens — **use a long random string in production** |
| `JWT_ALGORITHM` | Signing algorithm (default: `HS256`) |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | How long an access token remains valid |

### Admin bootstrap

If you set all three variables below, the app will create an admin user on first startup when no
users exist in the database.

| Variable | Description |
|----------|-------------|
| `ADMIN_USERNAME` | Login username for the bootstrapped admin |
| `ADMIN_EMAIL` | Email address for the bootstrapped admin |
| `ADMIN_PASSWORD` | Password — hashed with Argon2 before storage |

---

## Qdrant

| Variable | Description |
|----------|-------------|
| `QDRANT_HOST` | Hostname or IP (default: `qdrant` in Docker, `localhost` locally) |
| `QDRANT_PORT` | Port (default: `6333`) |
| `QDRANT_PROTOCOL` | `http` or `https` |
| `COLLECTION_NAME` | Name of the Qdrant collection used for document embeddings |

---

## Redis

| Variable | Description |
|----------|-------------|
| `REDIS_HOST` | Hostname or IP (default: `redis` in Docker, `localhost` locally) |
| `REDIS_PORT` | Port (default: `6379`) |
| `REDIS_PROTOCOL` | `redis` or `rediss` (TLS) |
| `REDIS_DB` | Database index (default: `0`) |

---

## RabbitMQ

| Variable | Description |
|----------|-------------|
| `RABBITMQ_HOST` | Hostname or IP |
| `RABBITMQ_PORT` | AMQP port (default: `5672`) |
| `RABBITMQ_USERNAME` | Username (default: `guest`) |
| `RABBITMQ_PASSWORD` | Password (default: `guest`) |
| `RABBITMQ_VHOST` | Virtual host (default: `/`) |
| `RABBITMQ_AMQP_URL` | Full AMQP URL — overrides individual host/port/user fields if set |
| `RABBITMQ_INGEST_QUEUE` | Name of the queue the ingestion worker consumes |

---

## Full reference

For the complete list of variables with defaults, see:

- **`env.example`** in the repository root — human-readable defaults and comments
- **`app/config/env_config.py`** — typed `Settings` fields with validation
