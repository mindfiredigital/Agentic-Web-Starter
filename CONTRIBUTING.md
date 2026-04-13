# Contributing to Agentic RAG Template

We welcome and appreciate your contributions. These guidelines exist to keep collaboration smooth, the codebase secure, and every change reviewable by the team.

---

## How Can You Contribute?

- Reporting bugs or issues
- Submitting feature requests
- Writing or improving documentation
- Fixing bugs
- Implementing new features

---

## Contribution Workflow

1. **Fork** the repository to your GitHub account.
2. **Clone** your fork locally.
3. Create a new **branch** following the naming convention:
   ```
   git checkout -b feature/<short-description>
   ```
   See [Branch Naming](#branch-naming) below for all allowed prefixes.
4. **Make your changes** and ensure they follow the [code rules](#code-rules).
5. **Install dev tooling** (once per environment) so lint commands match CI:
   ```bash
   make setup
   ```
   This creates `.venv`, installs dev dependencies, and installs pre-commit hooks.

   **Manual alternative:**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   python -m pip install --upgrade pip
   python -m pip install -e ".[dev]"
   pre-commit install
   pre-commit install --hook-type pre-push
   ```
   Test hooks on the whole tree once: `pre-commit run --all-files`
6. **Run quality checks** before committing (same commands as CI):
   ```bash
   black app/ && isort app/ && ruff check app/
   ```
   Optional — run mypy locally when you touch typed modules: `mypy app/ --ignore-missing-imports` (full-repo mypy is not enforced in CI yet).
7. **Run the test suite** and make sure everything passes:
   ```bash
   pytest app/tests/ -v
   # or via Docker:
   docker compose run tests
   ```
8. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/) format:
   ```
   feat(agents): add timeout handling to supervisor agent
   fix(repository): handle empty result set in base_repository
   ```
9. **Push** your branch and open a **Pull Request** against `main`.
10. Fill in the **PR description template** from [`docs/PR_GUIDELINES.md`](./docs/PR_GUIDELINES.md#7-pr-description--checklist) completely — PRs with empty descriptions will not be reviewed.

---

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<short-description>` | `feature/add-redis-history-ttl` |
| Bug fix | `fix/<short-description>` | `fix/qdrant-collection-init-error` |
| Refactor | `refactor/<short-description>` | `refactor/llm-factory-fallback-logic` |
| Docs | `docs/<short-description>` | `docs/update-jwt-auth-flow` |
| Tests | `test/<short-description>` | `test/ingestion-service-coverage` |
| Chore | `chore/<short-description>` | `chore/bump-langchain-version` |
| Hotfix | `hotfix/<short-description>` | `hotfix/supervisor-agent-crash` |

**Never push directly to `main`.**

---

## Code Rules

A summary of the most important rules. See the full reference in [`docs/PR_GUIDELINES.md`](./docs/PR_GUIDELINES.md).

- **Service layer** — all business logic goes in `app/services/`, not in route handlers
- **Repository pattern** — all database access goes through `app/repository/`
- **No hardcoded values** — use the `settings` singleton from `app/config/env_config.py`
- **Custom exceptions only** — raise from `app/exceptions/domain.py`, never raw `Exception`
- **Structured logging** — use the JSON logger, never `print()`
- **Docstrings** — all public classes and methods require Google-style docstrings
- **No secrets committed** — `.env` is gitignored; add new vars to `env.example` instead
- **Tests required** — all new business logic must have tests covering happy path and failure cases

---

## Pull Request Requirements

Every PR must:

- Address **exactly one concern** (no mixing features and refactors)
- Have a **filled-out PR description** using the template in [`docs/PR_GUIDELINES.md`](./docs/PR_GUIDELINES.md#7-pr-description--checklist)
- Pass **all CI checks** on GitHub Actions (Black, isort, Ruff, pytest — see [`.github/workflows/ci.yml`](./.github/workflows/ci.yml); install locally with `pip install -e ".[dev]"`)
- Have **at least 1 approving review** (2 for security/auth changes)
- Have **all reviewer comments resolved** before merge

PRs that violate the rules in [`docs/PR_GUIDELINES.md`](./docs/PR_GUIDELINES.md) will be closed and must be corrected before re-opening.

---

## Quick Pre-PR Checklist

```
✓ Branch name follows convention
✓ Commits follow Conventional Commits format
✓ .env not committed; env.example updated if new vars added
✓ black, isort, ruff — all pass with zero errors (mypy optional until enforced in CI)
✓ No print() — structured logger used
✓ No hardcoded values — all config from settings
✓ Custom exceptions used — no raw Exception
✓ Docstrings on all public classes and methods
✓ Tests added and passing
✓ PR description filled out completely
✓ PR is under 600 lines and single-concern
```

---

## Full PR Guidelines

For the complete set of rules covering branch naming, commit standards, architecture rules, security requirements, testing expectations, review process, and automatic rejection criteria, read:

**[docs/PR_GUIDELINES.md](./docs/PR_GUIDELINES.md)**

---

## Licensing

By contributing, you agree that your contributions will be licensed under the project's [License](./LICENSE.md).

---

## Need Help?

If you need clarification, open an issue or reach out to the maintainers directly.

Thank you for contributing to Agentic RAG Template!