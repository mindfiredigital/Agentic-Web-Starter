FROM python:3.11-slim

WORKDIR /app

# System deps (optional, useful for some PDF loaders)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/data

COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir .

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]