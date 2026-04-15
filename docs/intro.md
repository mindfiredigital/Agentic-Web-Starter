---
sidebar_position: 1
slug: /intro
title: Introduction
description: What Agentic Web Starter is and how this documentation is organized.
---

# Introduction

**Agentic Web Starter** is a production-ready FastAPI template for building AI-powered web services.
It gives you a complete foundation — document ingestion, retrieval-augmented chat, authentication,
and role management — so you can focus on your domain logic rather than boilerplate.

## What's included

| Capability | Details |
|-----------|---------|
| **RAG pipeline** | Upload documents → embed → store in Qdrant → retrieve at chat time |
| **Chat endpoint** | Retrieval-augmented responses via OpenAI or Gemini |
| **Chat history** | Redis-backed (persistent) or in-memory (ephemeral), switchable via a flag |
| **Authentication** | JWT login, token validation, and Argon2 password hashing |
| **User & role management** | Full CRUD for users, roles, and component-level ACLs, stored in SQLite |
| **Async ingestion** | Optional RabbitMQ worker for non-blocking document processing |
| **Observability** | Health endpoint, structured JSON logging, and a CI pipeline |
| **Documentation site** | This Docusaurus handbook, built from the `docs/` folder |

Everything optional (Qdrant, Redis, SQL, RabbitMQ) can be toggled off with a single environment
flag, so the service runs even in a minimal setup.

---

## How to navigate this handbook

| Page | What you will find |
|------|--------------------|
| [Getting started](./getting-started) | Clone the repo, configure `.env`, and run with Docker or locally |
| [Configuration](./configuration) | Every environment variable and feature flag explained |
| [Architecture](./architecture) | How the layers fit together and where each piece of logic lives |
| [Authentication & IAM](./authentication-and-iam) | JWT flow, protected routes, and the ACL model |
| [API reference](./api-reference) | Endpoint list, request/response shapes, and error codes |
| [Contributing](./contributing) | How to open issues and pull requests |
| [Pull request guidelines](./pull-request-guidelines) | Branch naming, commit standards, code rules, and the PR checklist |

---

## Source of truth

**The code is always authoritative.** The docs explain intent; the Swagger UI at `/docs` reflects the live schema.

- **Behavior and contracts** — Python source under `app/` and `env.example`
- **Interactive HTTP docs** — Swagger UI served at `/docs` on a running instance (see [API reference](./api-reference))

---

## Building this site

```bash
make docs        # starts Docusaurus dev server at http://localhost:3000
make docs-build  # production build → website/build/
```

Or manually: `cd website && npm install && npm start`.
