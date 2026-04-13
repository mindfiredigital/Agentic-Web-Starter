# Pull Request Guidelines

This document defines the strict standards every contributor must follow before raising a Pull Request against this repository. These rules exist to keep the codebase secure, maintainable, and reviewable by everyone on the team.

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

Every branch **must** follow this naming convention. Branches that do not will be asked to rename before review begins.

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
- Use only lowercase letters and hyphens — no underscores, no additional slashes
- Keep the description concise (2–4 words)
- **Never push directly to `main`**

---

## 2. Commit Message Standards

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <short description>

[optional body — explain what and why, not how]

[optional footer — BREAKING CHANGE: ..., Closes #<issue>]
```

### Allowed Types

| Type | When to Use |
|------|------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `refactor` | Code change with no functional impact |
| `test` | Adding or updating tests only |
| `docs` | Documentation changes only |
| `chore` | Dependency bumps, build config, tooling |
| `perf` | Performance improvements |
| `ci` | CI/CD configuration changes |

### Allowed Scopes

Scope must match the module being changed:

`agents` · `routes` · `services` · `repository` · `tools` · `utils` · `config` · `schemas` · `models` · `workers` · `tests` · `deps` · `prompts` · `exceptions`

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

### Rules

- Subject line: **maximum 72 characters**
- Use **imperative mood** — "add" not "added", "fix" not "fixed"
- No trailing period on the subject line
- **No `WIP` commits** in the final PR — squash or rebase before opening

---

## 3. Code Quality Requirements

Every contributor must run and pass all of the following locally before pushing:

### Formatting

```bash
black app/          # PEP 8 compliant auto-formatting
isort app/          # Consistent import ordering
```

### Linting

```bash
ruff check app/     # Fast, comprehensive linting
```

### Type Checking (optional locally; not enforced in CI yet)

```bash
mypy app/ --ignore-missing-imports
```

Black, isort, and Ruff must produce **zero errors** (same as GitHub Actions). Mypy is recommended when you change typed modules; the full tree is not yet clean enough to gate CI on mypy.

### Installation (if not already installed)

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

---

## 4. Project-Specific Code Rules

These rules are derived from the architecture and conventions already established in this codebase.

### 4.1 Architecture

#### Service Layer is Mandatory
Route handlers in `app/routes/` must only handle HTTP concerns (request parsing, response formatting, auth dependency injection). **All business logic belongs in `app/services/`.**

```python
# WRONG — logic in route handler
@router.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    chunks = split_text(content)          # ← business logic here is wrong
    await qdrant.index(chunks)
    return {"status": "ok"}

# CORRECT — delegate to service
@router.post("/upload")
async def upload(file: UploadFile, service: IngestionService = Depends(...)):
    return await service.ingest(file)
```

#### Repository Pattern Must Be Respected
Database access (SQL or vector) must go through the repository layer in `app/repository/`. Services must never query the database directly.

#### New LangChain Tools Must Subclass `BaseTool`
Follow the existing pattern in `app/tools/indexer_tool.py` and `app/tools/retriever_tool.py`. Implement `_run()` (sync) and `_arun()` (async) with proper `name`, `description`, and `args_schema`.

#### New Agents Must Extend `BaseAgent`
All agents must extend `app/agents/base_agent.py`. No standalone agent implementations outside this hierarchy.

#### Singletons at Module Level
Config, service, and agent classes are instantiated **once** as module-level singletons. Do not instantiate them inside functions or request handlers.

```python
# CORRECT — module-level singleton
settings = Settings()

# WRONG — instantiated per-request
def get_settings():
    return Settings()   # ← creates a new instance every call
```

### 4.2 Naming Conventions

| Construct | Convention | Example |
|-----------|-----------|---------|
| Files/modules | `snake_case` | `ingestion_service.py` |
| Classes | `PascalCase` | `IngestionService` |
| Functions/methods | `snake_case` | `index_document()` |
| Variables | `snake_case` | `session_id` |
| Constants/enum values | `UPPER_SNAKE_CASE` | `ALLOWED_FILES`, `ENV_DEV` |
| Module-level singletons | `snake_case` | `settings`, `qdrant_config` |

- No abbreviations unless industry-standard (`llm`, `rag`, `jwt`, `api`, `db`)
- Enum class names: `PascalCase` (e.g., `Environment`, `AllowedFiles`)

### 4.3 Error Handling

- **Always raise from the custom exception hierarchy** in `app/exceptions/domain.py`:
  - `UnauthorizedError` — 401 scenarios
  - `ForbiddenError` — 403 scenarios
  - `NotFoundError` — 404 scenarios
  - `ConflictError` — 409 scenarios
  - `ValidationError` — 422 scenarios
  - `InternalError` — 500 scenarios
- New exception types must extend `AppError`
- Never raise raw `Exception`, `ValueError`, or `HTTPException` directly from services or repositories
- Never silently swallow exceptions with bare `except: pass`

### 4.4 Logging

- Use the structured JSON logger from `app/config/log_config.py` — **never use `print()`**
- Log at the correct level:
  - `DEBUG` — internal traces useful during development
  - `INFO` — significant, expected events (service started, request handled)
  - `WARNING` — degraded behavior that did not cause failure
  - `ERROR` — failures that need attention
- **Never log secrets, API keys, tokens, passwords, or PII**

### 4.5 Environment & Configuration

- **No hardcoded values** — all configuration (hosts, ports, API keys, model names, timeouts, collection names) must come through the `settings` singleton from `app/config/env_config.py`
- New environment variables must be added to **both**:
  1. `app/config/env_config.py` — as a typed `Settings` field with a sensible default
  2. `env.example` — with a descriptive comment explaining the variable and its expected values
- **The `.env` file must never be committed** — it is in `.gitignore`
- Feature flags (`USE_QDRANT`, `USE_REDIS`, `USE_SQL`, `USE_RABBITMQ`) must be respected — new external integrations must be guarded behind a flag so the application can still run without that dependency

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

Private/internal helpers (prefixed `_`) may omit docstrings if their purpose is obvious from the name.

### 4.7 Dependencies

- New dependencies added to `requirements.txt` with a **pinned version** (`==`) for all direct dependencies
- Verify the package is not already included transitively before adding
- No unused dependencies — if a library is imported but not actively used, remove it

---

## 5. Testing Requirements

- Every PR that adds or modifies business logic **must include tests** in `app/tests/`
- Test file location must mirror the source structure (e.g., tests for `app/services/core_services/ingestion_service.py` go in `app/tests/services/core_services/test_ingestion_service.py`)
- Use `pytest` and `httpx.TestClient` for route-level tests — see `app/tests/conftest.py` for available fixtures

### Coverage Expectations

| Scenario | Required |
|----------|---------|
| Happy path | Yes |
| At least one failure/edge case | Yes |
| Auth boundary (unauthorized access) | Yes (for protected routes) |
| Feature flag disabled path | Yes (if the new code is flag-gated) |

### Running Tests

```bash
# Via Docker (full stack with all services)
docker compose run tests

# Locally
pytest app/tests/ -v

# With coverage report
pytest app/tests/ -v --cov=app --cov-report=term-missing
```

### Mocking Rules

- Mock **only at the external boundary** — database calls, Redis, Qdrant operations, LLM API calls
- Do not mock entire modules or internal service methods just to make tests pass
- Use `unittest.mock.patch` or `pytest-mock`'s `mocker` fixture

---

## 6. Security Rules

- **Never commit secrets** — no API keys, JWT secrets, database passwords, or any credentials anywhere in the codebase or config files
- `env.example` must use placeholder values only (e.g., `OPENAI_API_KEY=your-openai-api-key-here`)
- **No `ENV=dev` or `DEBUG` mode** committed as a default value
- JWT-related changes in `app/utils/iam_utils/jwt_utils.py` or `app/utils/iam_utils/auth_utils.py` require **explicit maintainer review** — tag a maintainer directly in the PR
- Password hashing must continue to use **Argon2 via `passlib`** — no weaker algorithms (bcrypt, md5, sha1, plain text)
- `ALLOWED_ORIGINS` must not be set to `["*"]` in any environment configuration committed to the repository
- Validate and sanitize all user-supplied input before passing to LLM prompts to avoid prompt injection

---

## 7. PR Description & Checklist

Every PR description must follow the template below. Copy it into your PR description and fill in every section. A PR with an empty description or unchecked checklist items will be sent back to the author without review.

### PR Description Template

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
- [ ] `mypy app/ --ignore-missing-imports` passes with zero errors — *recommended; not required by CI until repo-wide types are tightened*
- [ ] No `print()` statements — structured logger used throughout
- [ ] No hardcoded values (hosts, ports, model names, API keys) — all sourced from `settings`

### Architecture
_Mark N/A on items that don't apply to this PR type._

- [ ] Business logic lives in `app/services/`, not in route handlers
- [ ] Database access goes through `app/repository/`, not directly from services
- [ ] New LangChain tools subclass `BaseTool` (following `app/tools/` pattern) — *N/A if no new tools*
- [ ] New agents extend `BaseAgent` (following `app/agents/` pattern) — *N/A if no new agents*
- [ ] Custom exceptions raised from `app/exceptions/domain.py` hierarchy — no raw `Exception`

### Documentation
- [ ] All new public classes and methods have Google-style docstrings (`Args:`, `Returns:`, `Raises:`)
- [ ] Relevant docs in `docs/` updated if architecture or flow changed

### Dependencies
- [ ] New dependencies added to `requirements.txt` with a pinned version (`==`)
- [ ] No unused dependencies introduced

### Tests
- [ ] Tests added for all new logic (happy path + at least one failure/edge case)
- [ ] All tests pass: `pytest app/tests/ -v` or `docker compose run tests`
- [ ] Only boundary I/O is mocked (DB, Redis, Qdrant, LLM) — no business logic stubbed out

### PR Hygiene
- [ ] All reviewer comments resolved before requesting merge
```

---

## 8. PR Size Rules

| Metric | Guideline |
|--------|-----------|
| Ideal size | 200–400 lines changed |
| Hard limit | 600 lines changed |
| Exclusions from limit | `requirements.txt` version bumps, auto-generated files, migration files |
| Single concern | One PR = one logical change |

If a PR exceeds 600 lines, it must be split. Each PR should be fully reviewable in under 30 minutes.

**Mixing concerns in a single PR is not allowed.** A refactor and a feature must be separate PRs.

---

## 9. Review & Merge Rules

| Rule | Detail |
|------|--------|
| Minimum approvals | 1 approving review for general changes |
| Security/auth changes | 2 approving reviews required |
| Self-merges | Not allowed — the PR author must not merge their own PR |
| CI status | All checks (tests, linting) must be green before merge |
| Open comments | All reviewer comments must be resolved before merge |
| Merge strategy | **Squash and merge** for features and fixes; **merge commit** only for release branches |
| Branch cleanup | Delete the source branch after merge |

### Responding to Review Comments

- Address every comment — either fix it or explain why it was not changed
- Do not force-push after a review has started (use additional commits, then squash at merge)
- Do not resolve reviewer threads yourself — let the reviewer resolve after they confirm the fix

---

## 10. Automatic Rejection Criteria

PRs exhibiting any of the following will be **closed immediately** and must be re-opened after fixing:

| Violation | Reason |
|-----------|--------|
| `.env` file committed | Exposes credentials — security incident |
| Any secret or API key in code | Security incident |
| `print()` used instead of logger | Breaks structured log pipeline; not visible in production |
| Business logic in a route handler | Violates the service layer architecture |
| Hardcoded host, port, model name, or key | Breaks configurability and portability |
| No tests for new business logic | Untested code enters the main branch |
| Raw `Exception`, `ValueError`, or `HTTPException` raised in a service | Bypasses the global error handler; returns inconsistent error shapes |
| Unrelated changes mixed in one PR | Makes review and rollback impossible |
| New env var missing from `env.example` | Breaks deployments for all other contributors |
| Public methods without docstrings | Breaks documentation standard |
| Branch pushed directly to `main` | Bypasses review process entirely |

---

## Quick Reference Card

```
Before every push, run:
  black app/ && isort app/ && ruff check app/
  # optional: mypy app/ --ignore-missing-imports

Before opening a PR, verify:
  ✓ Branch name follows convention
  ✓ Commits follow Conventional Commits
  ✓ .env not committed
  ✓ env.example updated (if new vars added)
  ✓ No print() — use logger
  ✓ No hardcoded values — use settings
  ✓ Custom exceptions used — no raw Exception
  ✓ Docstrings on all public classes/methods
  ✓ Tests added and passing
  ✓ PR description filled out completely
  ✓ PR is under 600 lines and single-concern
```
