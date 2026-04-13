# Agentic Web Starter

FastAPI-based agentic RAG service with document ingestion, retrieval-augmented chat, JWT authentication, and user/role management. Uses Qdrant for vector search, configurable Redis/in-memory chat history, and optional SQLite for users, roles, and ACLs.

## Features

- **Document ingestion** — File upload and indexing into Qdrant with configurable embedding
- **RAG chat** — Chat endpoint with retrieval augmentation and prompt orchestration
- **Configurable memory** — Redis-backed or in-memory chat history
- **Authentication (optional)** — JWT-based auth with optional admin user bootstrap
- **User & role management (optional)** — CRUD for users and roles with SQLite persistence
- **Global exception handling** — Consistent error responses (401, 403, 404, 422)
- **Health check** — `/health` endpoint for liveness
- **Tests** — Pytest suite runnable via Docker Compose; **CI** runs the same checks on GitHub Actions (Black, isort, Ruff, pytest — see `.github/workflows/ci.yml`)

## Requirements

- **Python 3.10+** for local runs
- **Docker & Docker Compose** for containerized runs
- **Qdrant** and **Redis** (included in Compose)
- **RabbitMQ** (optional; included in Compose)

## Project structure

```
agentic_web_starter/
├── app/
│   ├── agents/           # Retriever and supervisor agents
│   ├── config/           # Env, logging, Qdrant, Redis, RabbitMQ config
│   ├── constants/        # App constants
│   ├── exceptions/       # Domain exceptions and global handlers
│   ├── llms/             # OpenAI and Gemini chat clients
│   ├── models/           # SQLAlchemy/SQLite models (user, role, component)
│   ├── prompts/          # Prompt templates
│   ├── repository/       # vector_repository (Qdrant), sql_repository (user, role, ACL)
│   ├── routes/
│   │   ├── core_routes/  # Chat and ingestion endpoints
│   │   └── iam_routes/   # Auth, users, roles endpoints
│   ├── schemas/          # core_schemas, iam_schemas (Pydantic request/response)
│   ├── services/         # core_services, iam_services, message_queue_services
│   ├── tools/            # Indexer and retriever tools
│   ├── workers/          # Ingestion worker (consumes RabbitMQ queue)
│   ├── utils/            # core_utils, iam_utils (auth, JWT, embeddings, Redis)
│   ├── tests/            # Pytest tests
│   ├── health.py        # Health check endpoint
│   ├── main.py           # FastAPI app entry (uses starter)
│   └── starter.py        # App bootstrap, routers, exception handlers
├── docker-compose.yml    # app, worker, tests, qdrant, redis, rabbitmq
├── Dockerfile
├── Makefile              # local bootstrap (`make setup`)
├── env.example
├── pyproject.toml         # dependencies, dev extras, isort profile=black
├── .pre-commit-config.yaml # optional local hooks (run: pre-commit install)
├── .github/workflows/ci.yml
└── README.md
```

## Setup

1. **Copy environment file and set variables:**

   ```bash
   cp env.example .env
   ```

2. **Edit `.env` as needed:**

   | Variable | Description |
   |----------|-------------|
   | `OPENAI_API_KEY` / `GEMINI_API_KEY` | At least one required for chat |
   | `JWT_SECRET_KEY` | Secret for JWT signing (required for auth) |
   | `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` | Optional; creates initial admin on first run |
   | `USE_QDRANT` | If `false`, ingestion is disabled and `/api/v1/upload` returns a configuration alert |
   | `USE_REDIS` | If `false`, chat history is handled in-memory instead of Redis |
   | `USE_SQL` | If `false`, SQL init/bootstrap are skipped and IAM routes (`/auth`, `/users`, `/roles`) are disabled |
   | `QDRANT_HOST`, `QDRANT_PORT`, `QDRANT_PROTOCOL` | Default `qdrant:6333` (http) in Docker |
   | `REDIS_HOST`, `REDIS_PORT` | Default `redis:6379` in Docker |
   | `USE_RABBITMQ` | If `true`, use message queue for async processing (ingestion, etc.); `/api/v1/upload` queues instead of indexing inline |
   | `RABBITMQ_HOST`, `RABBITMQ_PORT` | Default `rabbitmq:5672` in Docker |
   | `RABBITMQ_USERNAME`, `RABBITMQ_PASSWORD` | RabbitMQ credentials (defaults: `guest/guest`) |
   | `RABBITMQ_VHOST` / `RABBITMQ_AMQP_URL` | VHost or full AMQP URL override |
   | `RABBITMQ_INGEST_QUEUE` | Queue name for async ingestion jobs |
   | `WORKING_DIR` | Base path for uploads, logs, DB (default: `./temp` in Docker) |
   | `PROJECT_NAME` | Used for upload/log paths under `WORKING_DIR` (default: `agentic_rag`) |
   | `COLLECTION_NAME` | Qdrant collection name (default: `agentic_web_starter`) |
   | `ALLOWED_ORIGINS`, `BASE_PATH` | CORS and root path for the API |

## Run with Docker (recommended)

Starts the API, ingestion worker, Qdrant, Redis, and RabbitMQ:

```bash
docker compose up --build
```

API is served with Gunicorn (4 workers, uvicorn) at **http://localhost:8000**.

- **Detached:** `docker compose up -d --build`
- **Stop:** `docker compose down`

**Services included:**

| Service | Description |
|---------|-------------|
| `app` | FastAPI API server |
| `worker` | Ingestion worker — consumes RabbitMQ queue and indexes uploaded documents into Qdrant (required when `USE_RABBITMQ=true`) |
| `qdrant` | Vector database |
| `redis` | Chat history cache |
| `rabbitmq` | Message queue for async ingestion |

**Run tests in Docker:**

```bash
docker compose run tests
```

Data persistence uses `WORKING_DIR` (default: `./temp` when running via Docker). SQLite is at `{WORKING_DIR}/sqlite_data/app.db`; Qdrant storage at `{WORKING_DIR}/qdrant_storage`; RabbitMQ data at `{WORKING_DIR}/rabbitmq_data`.

RabbitMQ management UI is available at `http://localhost:15672` (default login: `guest/guest`).

## Run locally (API) with Docker dependencies

1. **Start Qdrant, Redis, and RabbitMQ:**

   ```bash
   docker compose up -d qdrant redis rabbitmq
   ```

   Then set `QDRANT_HOST=localhost`, `REDIS_HOST=localhost`, and `RABBITMQ_HOST=localhost` in `.env` so the local API can reach the containers.

2. **Bootstrap local developer setup (recommended):**

   ```bash
   make setup
   ```

   This creates `.venv`, installs dev dependencies, and installs both pre-commit and pre-push hooks.

   **Or manually, if you do not use `make`:**

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   python -m pip install --upgrade pip
   python -m pip install -e ".[dev]"
   pre-commit install
   pre-commit install --hook-type pre-push
   ```

3. **Start the API:**

   ```bash
   uvicorn app.main:app --reload
   ```

   Or production-style with Gunicorn:

   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

4. **If using RabbitMQ** (`USE_RABBITMQ=true`), start the worker in a separate terminal:

   ```bash
   python -m app.workers.ingestion_worker
   ```

5. **Run tests locally** (with Qdrant and Redis up):

   ```bash
   pytest -q app/tests
   ```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/auth/login` | Login (returns JWT; available when `USE_SQL=true`) |
| `POST` | `/api/v1/upload` | Upload and ingest document |
| `POST` | `/api/v1/chat` | RAG chat |
| `GET` | `/api/v1/users/list_users` | List users (auth; available when `USE_SQL=true`) |
| `GET` | `/api/v1/users/get_user/{user_id}` | Get user (auth; available when `USE_SQL=true`) |
| `POST` | `/api/v1/users/create_user` | Create user (auth; available when `USE_SQL=true`) |
| `PUT` | `/api/v1/users/update_user/{user_id}` | Update user (auth; available when `USE_SQL=true`) |
| `DELETE` | `/api/v1/users/delete_user/{user_id}` | Delete user (auth; available when `USE_SQL=true`) |
| `GET` | `/api/v1/roles/list_roles` | List roles (auth; available when `USE_SQL=true`) |
| `GET` | `/api/v1/roles/get_role/{role_id}` | Get role (auth; available when `USE_SQL=true`) |
| `POST` | `/api/v1/roles/create_role` | Create role (auth; available when `USE_SQL=true`) |
| `PUT` | `/api/v1/roles/update_role/{role_id}` | Update role (auth; available when `USE_SQL=true`) |
| `DELETE` | `/api/v1/roles/delete_role/{role_id}` | Delete role (auth; available when `USE_SQL=true`) |

Protected routes require a valid JWT in the `Authorization: Bearer <token>` header.

## Notes

- **SQLite** — User/role/ACL data is stored in `WORKING_DIR/sqlite_data/app.db` (e.g. `./temp/sqlite_data/app.db` when using Docker default `WORKING_DIR=./temp`).
- **Admin bootstrap** — If `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` are set, the first run creates an admin user when no users exist.
- **Uploads and logs** — Stored under `WORKING_DIR/<PROJECT_NAME>/static/uploads` and `WORKING_DIR/<PROJECT_NAME>/logs` (e.g. `./temp/agentic_rag/static/uploads` with default `PROJECT_NAME=agentic_rag`).
- **Hugging Face** — Cache defaults to `WORKING_DIR/<PROJECT_NAME>/hf` unless `HF_HOME` is set.
- **OpenAPI docs** — Available at `http://localhost:8000/docs` when the app is running. If `BASE_PATH` is set (e.g. `/agentic_rag`), use `http://localhost:8000{BASE_PATH}/docs` when behind a reverse proxy.
