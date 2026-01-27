## Agentic RAG Template

FastAPI-based agentic RAG service with ingestion, retrieval, and chat routes,
plus Qdrant vector search and Redis-backed chat history.

## Features
- File upload and ingestion into Qdrant
- Retrieval for RAG workflows
- Chat endpoint with prompt orchestration
- Health check endpoint

## Requirements
- Python 3.10+
- Docker (optional, for Qdrant/Redis via compose)

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
1. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure environment variables:
   ```
   cp env.example .env
   ```
   Update values in `.env` as needed:
   - `OPENAI_API_KEY`
   - `QDRANT_HOST`, `QDRANT_PORT`
   - `REDIS_HOST`, `REDIS_PORT`

## Running Locally
Run Qdrant/Redis (optional):
```
docker compose up -d
```

Start the API:
```
uvicorn app.main:app --reload
```

## API Endpoints
- `GET /api/v1/health` - health check
- `POST /api/v1/upload` - upload and ingest a document
- `POST /api/v1/chat` - chat with retrieval augmentation

## Notes
- Uploads are saved to `app/static/uploads` (created at startup).
- Qdrant must be reachable at the configured host/port.
