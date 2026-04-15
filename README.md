# Agentic Web Starter

<!-- Replace the URL below with your actual project logo/banner once available -->
![Agentic Web Starter](https://placehold.co/900x200?text=Agentic+Web+Starter)

FastAPI-based agentic RAG service with document ingestion, retrieval-augmented chat, JWT
authentication, and user/role management.

## Table of Contents

- [Agentic Web Starter](#agentic-web-starter)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

---

## Description

**Agentic Web Starter** is a production-ready, batteries-included template for building agentic
RAG (Retrieval-Augmented Generation) web services with FastAPI.  It ships with:

- a vectorised document ingestion pipeline backed by **Qdrant**,
- a **chat endpoint** that retrieves relevant context before querying an LLM,
- optional **JWT-based authentication** and a full **user / role management** sub-system,
- configurable **Redis** or in-memory chat history,
- an optional **RabbitMQ** worker for asynchronous document processing,
- a **Docusaurus** documentation site under `docs/` / `website/`, and
- CI via GitHub Actions running Black, isort, Ruff, and Pytest on every push.

The starter is designed to be cloned and extended.  Disable features you do not need through
environment flags and add your own agents, prompts, or data sources on top of the existing
foundation.

---

## Features

- **Document ingestion** — File upload and indexing into Qdrant with configurable embedding
- **RAG chat** — Chat endpoint with retrieval augmentation and prompt orchestration
- **Configurable memory** — Redis-backed or in-memory chat history
- **Authentication (optional)** — JWT-based auth with optional admin user bootstrap
- **User & role management (optional)** — CRUD for users and roles with SQLite persistence
- **Async ingestion (optional)** — RabbitMQ worker for non-blocking document processing
- **Global exception handling** — Consistent error responses (401, 403, 404, 422, 500)
- **Health check** — `/health` endpoint for liveness probes
- **Comprehensive tests** — Pytest suite runnable locally or via Docker Compose
- **CI pipeline** — GitHub Actions: Black, isort, Ruff, mypy, and Pytest on every push
- **Documentation site** — Docusaurus handbook with setup, architecture, API, and contribution guides

---

## Getting Started

### Prerequisites

- **Python 3.10+** (3.11 recommended) for local development
- **Docker & Docker Compose** for containerised runs (recommended for production-like setups)
- **Qdrant** and **Redis** (included as Docker Compose services)
- **RabbitMQ** (optional; included in Compose)
- An **OpenAI** or **Gemini** API key for the LLM back-end

### Installation

1. **Clone the repository and enter the directory:**

   ```bash
   git clone https://github.com/<your-org>/agentic_web_starter.git
   cd agentic_web_starter
   ```

2. **Copy the environment template and fill in your values:**

   ```bash
   cp env.example .env
   ```

   Key variables to configure:

   | Variable | Description |
   |----------|-------------|
   | `OPENAI_API_KEY` / `GEMINI_API_KEY` | At least one required for chat |
   | `JWT_SECRET_KEY` | Secret used to sign JWTs (required when `USE_SQL=true`) |
   | `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` | Optional bootstrap admin user |
   | `USE_QDRANT` | Set `false` to disable ingestion |
   | `USE_REDIS` | Set `false` to use in-memory chat history |
   | `USE_SQL` | Set `false` to disable IAM routes |
   | `USE_RABBITMQ` | Set `true` to enable async ingestion via RabbitMQ |

   See `.env.example` and the [Configuration guide](docs/configuration.md) for the full list.

3. **Run with Docker Compose (recommended):**

   ```bash
   docker compose up --build
   ```

   The API is available at **http://localhost:8000**.

   *Or* bootstrap a local development environment:

   ```bash
   make setup          # creates .venv, installs deps, and registers all git hooks
   source .venv/bin/activate   # put the venv on PATH for this shell (uvicorn, local pytest, etc.)
   docker compose up -d qdrant redis rabbitmq   # start dependencies only
   uvicorn app.main:app --reload
   ```

   `make setup` does not activate the virtualenv for you. Activate it in each new terminal session
   (or use explicit paths like `.venv/bin/uvicorn`) when running the API or tests locally without
   Docker. Pre-push hooks (`mypy`, `pytest`) use pre-commit’s own Python environment and install the
   project there, so you do **not** need a local `.venv` on `PATH` to push—only a normal Python
   install for `pre-commit` itself (as installed by `make setup`).

---

## Usage

### Interactive API docs

Open **http://localhost:8000/docs** in your browser for Swagger UI.
Click **Authorize** and paste your JWT to test protected endpoints.

### Quick examples

**Health check:**

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

**Upload a document:**

```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@my_document.pdf"
```

**Chat with RAG:**

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Summarise the document", "session_id": "session-1"}'
```

**Login (when `USE_SQL=true`):**

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

### Run tests

```bash
# In Docker (recommended — no local deps required)
docker compose run tests

# Locally (with Qdrant + Redis running; activate .venv first or use .venv/bin/pytest)
pytest -q app/tests
```

### Documentation site

```bash
make docs        # starts Docusaurus dev server at http://localhost:3000
make docs-build  # production build → website/build/
```

Refer to the [full documentation](docs/) for architecture decisions, configuration reference,
authentication flows, and the API reference.

---

## Contributing

Contributions are welcome!  Please read [CONTRIBUTING.md](docs/contributing.md) before opening a
pull request or issue.  The key points:

- Use [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.
  The `commit-msg` hook enforces this automatically after `make setup`.
- Run `pre-commit run --all-files` before pushing to ensure linting and formatting pass.
- All PRs must use the [pull request template](.github/pull_request_template.md) and reference a
  linked issue.
- Never push directly to `main`.

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — the web framework powering the API
- [Qdrant](https://qdrant.tech/) — vector database for similarity search
- [LangChain](https://www.langchain.com/) — orchestration framework for LLM pipelines
- [Docusaurus](https://docusaurus.io/) — documentation site generator
- [pre-commit](https://pre-commit.com/) — multi-language pre-commit hook framework
- [commitizen](https://commitizen-tools.github.io/commitizen/) — Conventional Commits enforcement
