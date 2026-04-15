---
sidebar_position: 8
title: Pull request guidelines
description: Branch naming, commits, code quality, testing, security, and PR checklist for Agentic Web Starter.
---

# Pull request guidelines

This document defines the standards every contributor must follow before opening a pull request.
These rules exist to keep the codebase secure, maintainable, and reviewable by the whole team.

**Violations of the [automatic rejection criteria](#10-automatic-rejection-criteria) result in
immediate closure of the PR.** Fix the issue and open a new PR rather than force-pushing.

---

## Table of Contents

1. [Branch Naming](#1-branch-naming)
2. [Commit Message Standards](#2-commit-message-standards)
3. [Code Quality Requirements](#3-code-quality-requirements)
4. [Project-Specific Code Rules](#4-project-specific-code-rules)
5. [Testing Requirements](#5-testing-requirements)
6. [Security Rules](#6-security-rules)
7. [PR Description & Checklist](#7-pr-description--checklist)
8. [PR Size Rules](#8-pr-size-rules)
9. [Review & Merge Rules](#9-review--merge-rules)
10. [Automatic Rejection Criteria](#10-automatic-rejection-criteria)

---

## 1. Branch Naming

Every branch **must** follow the naming convention below.  Branches that do not will be asked to
rename before review begins.

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<short-description>` | `feature/add-redis-history-ttl` |
| Bug fix | `fix/<short-description>` | `fix/qdrant-collection-init-error` |
| Refactor | `refactor/<short-description>` | `refactor/llm-factory-fallback-logic` |
| Docs | `docs/<short-description>` | `docs/update-jwt-auth-flow` |
| Tests | `test/<short-description>` | `test/ingestion-service-coverage` |
| Chore | `chore/<short-description>` | `chore/bump-langchain-version` |
| Hotfix | `hotfix/<short-description>` | `hotfix/supervisor-agent-crash` |

**Rules:**

- Use only lowercase letters and hyphens — no underscores, no extra slashes.
- Keep the description concise: 2–4 words is the target.
- **Never push directly to `main`.**

---

## 2. Commit Message Standards

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) spec.
The `commit-msg` pre-commit hook enforces this automatically after `make setup`.

### Format

```
<type>(<scope>): <short description>

[optional body — explain what and why, not how]

[optional footer — BREAKING CHANGE: ..., Closes #<issue>]
```

### Allowed types

| Type | When to use |
|------|------------|
| `feat` | A new feature visible to users or callers |
| `fix` | A bug fix |
| `refactor` | Code change with no functional impact |
| `test` | Adding or updating tests only |
| `docs` | Documentation changes only |
| `chore` | Dependency bumps, build config, tooling |
| `perf` | Performance improvements |
| `ci` | CI/CD configuration changes |

### Allowed scopes

The scope must match the module being changed:

`agents` · `routes` · `services` · `repository` · `tools` · `utils` · `config` · `schemas` ·
`models` · `workers` · `tests` · `deps` · `prompts` · `exceptions`

### Examples

```
feat(agents): add timeout handling to supervisor agent
fix(repository): handle empty result set in base_repository query
refactor(config): consolidate feature flags into a FeatureFlags model
test(utils): add unit tests for history_factory_utils fallback path
docs(auth): update JWT flow diagram for refresh token support
chore(deps): upgrade langchain to 0.3.x
perf(tools): cache embedding model instance across requests
```

### Subject line rules

- Maximum **72 characters**
- Use **imperative mood** — "add" not "added", "fix" not "fixed"
- No trailing period
- No `WIP` commits in the final PR — squash or rebase before opening

---

## 3. Code Quality Requirements

Run and pass all of the following locally before pushing.  These are the same checks that run in
GitHub Actions CI.

### Formatting

```bash
black app/     # PEP 8-compliant auto-formatting
isort app/     # consistent import ordering
```

### Linting

```bash
ruff check app/
```

### Type checking

```bash
mypy app/ --ignore-missing-imports
```

Type checking is recommended whenever you change typed modules.  It is not yet enforced in CI
because the full tree is not clean, but it should pass for any code you touch.

### Quick shortcut

If you have pre-commit installed (`make setup`), this runs everything at once:

```bash
pre-commit run --all-files
```

---

## 4. Project-Specific Code Rules

These rules are derived from the architecture already established in this codebase.  Following them
keeps features easy to test, easy to reason about, and easy to roll back.

### 4.1 Architecture

**Service layer is mandatory** — Route handlers in `app/routes/` must only handle HTTP concerns:
request parsing, response formatting, and auth dependency injection.  All business logic belongs
in `app/services/`.

```python
# WRONG — business logic inside the route handler
@router.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    chunks = split_text(content)       # ← belongs in a service
    await qdrant.index(chunks)
    return {"status": "ok"}

# CORRECT — delegate everything to the service
@router.post("/upload")
async def upload(file: UploadFile, service: IngestionService = Depends(...)):
    return await service.ingest(file)
```

**Repository pattern must be respected** — Database access (SQL or vector) must go through the
repository layer in `app/repository/`.  Services must never query a data store directly.

**New LangChain tools must subclass `BaseTool`** — Follow the pattern in
`app/tools/indexer_tool.py` and `app/tools/retriever_tool.py`.  Implement `_run()` (sync) and
`_arun()` (async) with proper `name`, `description`, and `args_schema`.

**New agents must extend `BaseAgent`** — All agents must extend `app/agents/base_agent.py`.
No standalone agent implementations outside this hierarchy.

**Singletons at module level** — Config, service, and agent instances are created once at module
level.  Do not instantiate them inside functions or request handlers.

```python
# CORRECT — created once at import time
settings = Settings()

# WRONG — a new instance on every call
def get_settings():
    return Settings()
```

---

### 4.2 Naming conventions

| Construct | Convention | Example |
|-----------|-----------|---------|
| Files / modules | `snake_case` | `ingestion_service.py` |
| Classes | `PascalCase` | `IngestionService` |
| Functions / methods | `snake_case` | `index_document()` |
| Variables | `snake_case` | `session_id` |
| Constants / enum values | `UPPER_SNAKE_CASE` | `ALLOWED_FILES`, `ENV_DEV` |
| Module-level singletons | `snake_case` | `settings`, `qdrant_config` |

Abbreviations are only allowed when they are industry-standard: `llm`, `rag`, `jwt`, `api`, `db`.

---

### 4.3 Error handling

Always raise from the custom exception hierarchy in `app/exceptions/domain.py`:

| Exception class | HTTP status | Use for |
|-----------------|-------------|---------|
| `UnauthorizedError` | 401 | Missing or invalid credentials |
| `ForbiddenError` | 403 | Authenticated but not permitted |
| `NotFoundError` | 404 | Resource does not exist |
| `ConflictError` | 409 | State conflict (e.g. duplicate user) |
| `ValidationError` | 422 | Invalid input |
| `InternalError` | 500 | Unexpected failures |

New exception types must extend `AppError`.  
Never raise raw `Exception`, `ValueError`, or FastAPI's `HTTPException` from services or repositories.  
Never silently swallow exceptions with `except: pass`.

---

### 4.4 Logging

- Use the structured JSON logger from `app/config/log_config.py` — **never `print()`**.
- Log at the correct level:

| Level | When to use |
|-------|------------|
| `DEBUG` | Internal traces useful during development |
| `INFO` | Significant, expected events (service started, request handled) |
| `WARNING` | Degraded behaviour that did not cause a failure |
| `ERROR` | Failures that need attention |

- **Never log secrets, API keys, tokens, passwords, or PII** at any level.

---

### 4.5 Environment & configuration

- No hardcoded values anywhere — hosts, ports, API keys, model names, timeouts, collection names
  must all come from `settings`.
- When you add a new environment variable, update **both**:
  1. `app/config/env_config.py` — typed `Settings` field with a sensible default
  2. `env.example` — descriptive comment explaining the variable and its expected values
- Feature flags (`USE_QDRANT`, `USE_REDIS`, `USE_SQL`, `USE_RABBITMQ`) must be respected — guard
  new external integrations behind a flag so the app runs without that dependency.

---

### 4.6 Docstrings

Every new **public** class and **public** method must have a Google-style docstring:

```python
def index_document(self, file_path: str, collection_name: str) -> int:
    """Index a document into the vector store.

    Args:
        file_path: Absolute path to the file to be indexed.
        collection_name: Name of the Qdrant collection to index into.

    Returns:
        The number of chunks successfully indexed.

    Raises:
        NotFoundError: If the file does not exist at the given path.
        InternalError: If the Qdrant indexing operation fails.
    """
```

Private helpers prefixed with `_` may omit docstrings when their purpose is obvious from the name.

---

### 4.7 Dependencies

- Pin all direct dependencies with `==` in `pyproject.toml`.
- Verify the package is not already included transitively before adding it.
- Remove unused imports — if a library is imported but not actively used, delete it.

---

## 5. Testing Requirements

Every PR that adds or modifies business logic **must include tests** in `app/tests/`.

Test file location mirrors the source structure. For example, tests for
`app/services/core_services/ingestion_service.py` belong in
`app/tests/services/core_services/test_ingestion_service.py`.

### Coverage expectations

| Scenario | Required? |
|----------|----------|
| Happy path | Yes |
| At least one failure or edge case | Yes |
| Auth boundary (unauthorized access) | Yes — for protected routes |
| Feature-flag-disabled path | Yes — if the new code is flag-gated |

### Running tests

```bash
# Via Docker — full stack, no local deps required
docker compose run tests

# Locally
pytest app/tests/ -v

# With coverage report
pytest app/tests/ -v --cov=app --cov-report=term-missing
```

### Mocking rules

- Mock **only at the external boundary** — database calls, Redis, Qdrant, LLM API calls.
- Do not mock entire modules or internal service methods just to make tests pass.
- Use `unittest.mock.patch` or `pytest-mock`'s `mocker` fixture.

---

## 6. Security Rules

Security violations are grounds for immediate PR closure.

- **Never commit secrets** — no API keys, JWT secrets, database passwords, or credentials anywhere
  in the codebase.
- `env.example` must contain placeholder values only, e.g. `OPENAI_API_KEY=your-key-here`.
- Do not commit `ENV=dev` or `DEBUG=true` as a default value.
- Changes to `app/utils/iam_utils/jwt_utils.py` or `app/utils/iam_utils/auth_utils.py` require
  **explicit maintainer review** — tag a maintainer directly in the PR.
- Password hashing must continue to use **Argon2 via `passlib`** — do not replace it with bcrypt,
  md5, sha1, or plain text.
- `ALLOWED_ORIGINS` must not be set to `["*"]` in any committed configuration.
- Sanitize all user-supplied input before passing it to LLM prompts to prevent prompt injection.

---

## 7. PR Description & Checklist

Every PR description must follow the template below.  A PR with an empty description or unchecked
checklist items will be returned to the author without review.

### PR description template

```markdown
## Summary

_What does this PR do? Provide a clear 2–4 sentence description._

## Motivation

_Why is this change needed? What problem does it solve?_

Closes #<!-- replace with issue number, or delete this line -->

## Type of Change

_Check all that apply._

- [ ] Bug fix
- [ ] New feature
- [ ] Refactor (no functional change)
- [ ] Documentation update
- [ ] Dependency bump
- [ ] Test coverage
- [ ] CI / chore
- [ ] Breaking change

> **If "Breaking change" is checked:** describe the impact and migration steps below.
>
> _e.g. "Renamed `get_docs()` to `fetch_documents()` — callers must update import paths."_

## Changes Made

_Bullet list of the key files/modules changed and what was done._

-
-

## Testing

_How was this tested? Check what applies and fill in details._

- [ ] Unit tests added / updated (`pytest app/tests/ -v`)
- [ ] Integration tests added / updated
- [ ] Manually verified — steps:
  1.
  2.

<details>
<summary>Sample output / screenshots (if applicable)</summary>

\```
# paste output here
\```

</details>

---

## Pre-PR Checklist

### Branch & Commits
- [ ] Branch name follows convention: `feature/`, `fix/`, `refactor/`, `docs/`, `test/`, `chore/`, `hotfix/`
- [ ] Commits follow Conventional Commits format (`feat(scope): description`)
- [ ] No `WIP` commits — squashed or rebased before opening this PR

### Security
- [ ] `.env` file is **not** committed
- [ ] No secrets, API keys, tokens, or passwords anywhere in the code
- [ ] `env.example` updated if new environment variables were added

### Code Quality
- [ ] `black app/` passes with zero errors
- [ ] `isort app/` passes with zero errors
- [ ] `ruff check app/` passes with zero errors
- [ ] `mypy app/ --ignore-missing-imports` passes — *recommended; not yet required by CI*
- [ ] No `print()` statements — structured logger used throughout
- [ ] No hardcoded values — all sourced from `settings`

### Architecture
_Mark N/A on items that don't apply to this PR._

- [ ] Business logic lives in `app/services/`, not in route handlers
- [ ] Database access goes through `app/repository/`, not directly from services
- [ ] New LangChain tools subclass `BaseTool` — *N/A if no new tools*
- [ ] New agents extend `BaseAgent` — *N/A if no new agents*
- [ ] Custom exceptions raised from `app/exceptions/domain.py` — no raw `Exception`

### Documentation
- [ ] All new public classes and methods have Google-style docstrings
- [ ] Relevant pages in `docs/` updated if architecture or behaviour changed

### Dependencies
- [ ] New dependencies added to `pyproject.toml` with a pinned version (`==`)
- [ ] No unused dependencies introduced

### Tests
- [ ] Tests cover happy path + at least one failure/edge case
- [ ] All tests pass: `pytest app/tests/ -v` or `docker compose run tests`
- [ ] Only boundary I/O is mocked — no business logic stubbed out

### PR Hygiene
- [ ] All reviewer comments resolved before requesting merge
```

---

## 8. PR Size Rules

Keeping PRs small makes them faster to review and easier to roll back.

| Metric | Guideline |
|--------|-----------|
| Ideal size | 200–400 lines changed |
| Hard limit | 600 lines changed |
| Exclusions | `pyproject.toml` version bumps, auto-generated files, migration files |
| Single concern | One PR = one logical change |

If a PR exceeds 600 lines it must be split.  Each PR should be fully reviewable in under 30 minutes.

**Mixing concerns is not allowed.** A refactor and a feature must be separate PRs.

---

## 9. Review & Merge Rules

| Rule | Detail |
|------|--------|
| Minimum approvals | 1 approving review for general changes |
| Security / auth changes | 2 approving reviews required |
| Self-merges | Not allowed — the PR author must not merge their own PR |
| CI status | All checks (tests, linting) must be green before merge |
| Open comments | All reviewer comments must be resolved before merge |
| Merge strategy | **Squash and merge** for features and fixes; **merge commit** only for release branches |
| Branch cleanup | Delete the source branch after merge |

### Responding to review comments

- Address every comment — either fix it or explain why you disagree.
- Do not force-push after a review has started; add new commits, then squash at merge time.
- Do not resolve reviewer threads yourself — let the reviewer mark them resolved after confirming.

---

## 10. Automatic Rejection Criteria

PRs exhibiting any of the following will be **closed immediately**.  Fix the issue and open a new PR.

| Violation | Reason |
|-----------|--------|
| `.env` file committed | Exposes credentials — treated as a security incident |
| Any secret or API key in code | Security incident |
| `print()` used instead of logger | Breaks the structured log pipeline; invisible in production |
| Business logic in a route handler | Violates the service layer architecture |
| Hardcoded host, port, model name, or key | Breaks configurability and portability |
| No tests for new business logic | Untested code enters the main branch |
| Raw `Exception`, `ValueError`, or `HTTPException` raised in a service | Bypasses the global error handler; returns inconsistent error shapes |
| Unrelated changes mixed in one PR | Makes review and rollback impossible |
| New env var missing from `env.example` | Breaks deployments for all other contributors |
| Public methods without docstrings | Breaks the documentation standard |
| Branch pushed directly to `main` | Bypasses the review process entirely |

---

## Quick reference card

Copy this somewhere handy while you work:

```
Before every push:
  black app/ && isort app/ && ruff check app/
  mypy app/ --ignore-missing-imports   (recommended)

Before opening a PR:
  ✓ Branch name follows convention
  ✓ Commits follow Conventional Commits
  ✓ .env is NOT committed
  ✓ env.example updated (if new vars added)
  ✓ No print() — use the structured logger
  ✓ No hardcoded values — use settings
  ✓ Custom exceptions used — no raw Exception
  ✓ Google-style docstrings on all public classes/methods
  ✓ Tests added and passing
  ✓ PR description filled out completely
  ✓ PR is under 600 lines and single-concern
```
