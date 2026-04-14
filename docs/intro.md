---
sidebar_position: 1
slug: /intro
title: Introduction
description: What Agentic Web Starter is and how this documentation is organized.
---

# Introduction

**Agentic Web Starter** is a FastAPI backend for agentic RAG: document ingestion, retrieval-augmented chat, optional **JWT authentication**, and **user/role** management with component-based ACLs. It integrates **Qdrant** for vectors, **Redis** (or in-memory) for chat history, **SQLite** for IAM when enabled, and optional **RabbitMQ** for async ingestion.

## Documentation map

| Doc | Contents |
|-----|----------|
| [Getting started](./getting-started) | Clone, env file, Docker and local runs |
| [Configuration](./configuration) | Environment variables and feature flags |
| [Architecture](./architecture) | Layers, main packages, request flow |
| [Authentication & IAM](./authentication-and-iam) | JWT, routes, ACL model |
| [API reference](./api-reference) | Where to find interactive OpenAPI docs |
| [Contributing](./contributing) | Workflow and links to full PR rules |
| [Pull request guidelines](./pull-request-guidelines) | Complete PR template and team standards |

## Source of truth

- **Behavior and contracts** — Python code under `app/` and `env.example`.
- **Interactive HTTP docs** — Swagger UI at `/docs` on a running server (see [API reference](./api-reference)).

This site is built with [Docusaurus](https://docusaurus.io/) from the `docs/` folder (`make docs` or `cd website && npm start`).
