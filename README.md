## Agentic RAG Template

FastAPI-based agentic RAG service with ingestion, retrieval, and chat routes,
plus Qdrant vector search and Redis-backed chat history.

## Features
- File upload and ingestion into Qdrant
- Retrieval for RAG workflows
- Chat endpoint with prompt orchestration
- Health check endpoint

## Requirements
- Python 3.10+ for local runs
- Docker + Docker Compose for containerized runs

## Project Structure
```
agentic_rag_template/
├─ app/
│  ├─ agents/                 # agent orchestration
│  ├─ config/                 # env, logging, qdrant, redis configs
│  ├─ constants/              # app constants
│  ├─ prompts/                # prompt templates
│  ├─ routes/                 # FastAPI routes
│  ├─ schemas/                # Pydantic schemas
│  ├─ services/               # ingestion, retrieval, llm, memory
│  ├─ tools/                  # indexing and retrieving tools
│  ├─ main.py                 # FastAPI app entry
│  └─ starter.py              # app bootstrap
├─ docker-compose.yml
├─ Dockerfile
├─ env.example
├─ requirements.txt
└─ README.md
```

## Setup
1. Create an environment file:
   ```
   cp env.example .env
   ```
2. Update values in `.env` as needed:
   - `OPENAI_API_KEY` or `GEMINI_API_KEY` (at least one required for chat)
   - `QDRANT_HOST`, `QDRANT_PORT` (default: `qdrant:6333` for Docker)
   - `REDIS_HOST`, `REDIS_PORT` (default: `redis:6379` for Docker)

## Run With Docker (Recommended)
This starts the API, Qdrant, and Redis in containers:
```
docker compose up --build
```

The API runs with gunicorn (4 workers, uvicorn worker class) and is available at `http://localhost:8000`.

To run in detached mode:
```
docker compose up -d --build
```

To stop:
```
docker compose down
```

## Run Locally (API) + Docker (Dependencies)
1. Start Qdrant and Redis:
   ```
   docker compose up -d qdrant redis
   ```
2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Start the API (development with auto-reload):
   ```
   uvicorn app.main:app --reload
   ```
   Or with gunicorn (production-style, multiple workers):
   ```
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

## API Endpoints
- `GET /api/v1/health` - health check
- `POST /api/v1/upload` - upload and ingest a document
- `POST /api/v1/chat` - chat with retrieval augmentation

## Notes
- Uploads/logs/vector data are stored under `WORKING_DIR` (default: current directory).
- Hugging Face cache defaults to `WORKING_DIR/hf` unless `HF_HOME` is set.
- The app requires Qdrant and Redis to be reachable at the configured host/port.
