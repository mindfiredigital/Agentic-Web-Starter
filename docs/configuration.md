---
sidebar_position: 3
title: Configuration
description: Environment variables and feature flags loaded by app.config.env_config.Settings.
---

# Configuration

Settings are loaded in **`app/config/env_config.py`** via the **`settings`** singleton. Copy **`env.example`** to **`.env`** and adjust values. Never commit `.env`.

## Feature flags

| Flag | When `false` |
|------|----------------|
| `USE_QDRANT` | RAG/upload path is disabled or limited; see runtime behavior for `/api/v1/upload`. |
| `USE_REDIS` | Chat history uses in-memory storage instead of Redis. |
| `USE_SQL` | SQLite init and IAM routes (`/auth`, `/users`, `/roles`) are not registered. |
| `USE_RABBITMQ` | Ingestion is not queued via RabbitMQ (behavior depends on ingestion implementation). |

## API and project

| Variable | Role |
|----------|------|
| `PROJECT_NAME`, `PROJECT_VERSION`, `PROJECT_DESCRIPTION` | FastAPI metadata and paths under `WORKING_DIR`. |
| `BASE_PATH` | Root path when behind a reverse proxy (also affects OpenAPI URL). |
| `ALLOWED_ORIGINS` | CORS origins (comma-separated). |
| `WORKING_DIR` | Base for logs, uploads, SQLite path segment, HF cache default. |

## LLM keys

At least one of **`OPENAI_API_KEY`** or **`GEMINI_API_KEY`** is required for chat features, depending on your LLM configuration.

## JWT (when `USE_SQL` is true)

| Variable | Role |
|----------|------|
| `JWT_SECRET_KEY` | Signing secret for tokens. |
| `JWT_ALGORITHM` | Default `HS256`. |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime. |

Optional **`ADMIN_USERNAME`**, **`ADMIN_EMAIL`**, **`ADMIN_PASSWORD`** bootstrap a first admin user when the database has no users.

## Qdrant

`QDRANT_HOST`, `QDRANT_PORT`, `QDRANT_PROTOCOL`, and **`COLLECTION_NAME`** (default collection name in code: `agentic_web_starter` unless overridden).

## Redis

`REDIS_HOST`, `REDIS_PORT`, `REDIS_PROTOCOL`, `REDIS_DB`.

## RabbitMQ

`RABBITMQ_*` variables and **`RABBITMQ_INGEST_QUEUE`** for the ingestion worker queue name.

For the full list and defaults, see **`env.example`** and **`app/config/env_config.py`**.
