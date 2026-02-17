# Agentic RAG Template

FastAPI-based agentic RAG service with document ingestion, retrieval-augmented chat, JWT authentication, and user/role management. Uses Qdrant for vector search, configurable Redis/in-memory chat history, and optional SQLite for users, roles, and ACLs.

## Features

- **Document ingestion** — File upload and indexing into Qdrant with configurable embedding
- **RAG chat** — Chat endpoint with retrieval augmentation and prompt orchestration
- **Configurable memory** — Redis-backed or in-memory chat history
- **Authentication (optional)** — JWT-based auth with optional admin user bootstrap
- **User & role management (optional)** — CRUD for users and roles with SQLite persistence
- **Global exception handling** — Consistent error responses (401, 403, 404, 422)
- **Health check** — `/health` endpoint for liveness
- **Tests** — Pytest suite runnable via Docker Compose

## Requirements

- **Python 3.10+** for local runs
- **Docker & Docker Compose** for containerized runs
- **Qdrant** and **Redis** (included in Compose)
- **RabbitMQ** (optional; included in Compose)

## Project structure

```
agentic_rag_template/
├── app/
│   ├── agents/           # Retriever and supervisor agents
│   ├── config/           # Env, logging, Qdrant, Redis config
│   ├── constants/        # App constants
│   ├── llms/             # OpenAI and Gemini chat clients
│   ├── models/           # SQLAlchemy/SQLite models
│   ├── prompts/         # Prompt templates
│   ├── repository/      # Qdrant, SQLite, user, role, ACL repos
│   ├── routes/           # Auth, chat, ingestion, users, roles
│   ├── schemas/          # Pydantic request/response schemas
│   ├── services/         # Auth, ingestion, retrieval, user, role, message_queue_services
│   ├── tools/            # Indexer and retriever tools
│   ├── workers/          # Background workers (ingestion consumer, etc.)
│   ├── utils/            # Auth, JWT, embeddings, Redis, file utils
│   ├── tests/            # Pytest tests
│   ├── main.py           # FastAPI app entry (uses starter)
│   └── starter.py        # App bootstrap, routers, exception handlers
├── docker-compose.yml    # app, worker, tests, qdrant, redis, rabbitmq
├── Dockerfile
├── env.example
├── requirements.txt
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
   | `WORKING_DIR` | Base path for uploads, logs, DB (default: current dir) |
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

SQLite data is persisted in `./sqlite_data`; Qdrant storage in `./qdrant_storage`.

RabbitMQ management UI is available at `http://localhost:15672` (default login: `guest/guest`).

## Run locally (API) with Docker dependencies

1. **Start Qdrant, Redis, and RabbitMQ:**

   ```bash
   docker compose up -d qdrant redis rabbitmq
   ```

2. **Create venv and install deps:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
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

- **SQLite** — User/role/ACL data is stored in `WORKING_DIR/sqlite_data/app.db` (e.g. `./sqlite_data/app.db` when using Docker volume).
- **Admin bootstrap** — If `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` are set, the first run creates an admin user when no users exist.
- **Uploads and logs** — Stored under `WORKING_DIR/<PROJECT_NAME>/static/uploads` and `.../logs`.
- **Hugging Face** — Cache defaults to `WORKING_DIR/<PROJECT_NAME>/hf` unless `HF_HOME` is set.
- **OpenAPI docs** — Available at `http://localhost:8000/docs` when the app is running.
