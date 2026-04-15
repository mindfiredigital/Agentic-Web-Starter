---
sidebar_position: 7
title: Contributing
description: How to contribute code, documentation, and issue reports to Agentic Web Starter.
---

# Contributing

Contributions of all kinds are welcome — whether you are fixing a bug, improving the docs,
proposing a new feature, or helping review pull requests.

---

## Before you start

1. **Search open issues** to see if someone has already reported the bug or requested the feature.
2. **Open an issue first** for any non-trivial change — this aligns expectations before you invest
   time in a PR.
3. **Fork the repository** and work on a branch.  Never push directly to `main`.

---

## Contribution workflow

Follow these steps for every contribution:

### 1 — Set up your environment

```bash
git clone https://github.com/<your-fork>/agentic_web_starter.git
cd agentic_web_starter
cp env.example .env          # configure your local settings
make setup                   # creates .venv, installs deps, registers git hooks
```

`make setup` installs pre-commit (pre-commit, pre-push, and commit-msg stages), so formatting and
Conventional Commits validation run automatically before every push.

### 2 — Create a branch

Follow the naming convention defined in [Pull request guidelines § 1](./pull-request-guidelines#1-branch-naming):

```
feature/add-redis-history-ttl
fix/qdrant-collection-init-error
docs/update-jwt-auth-flow
```

### 3 — Make your changes

- Keep changes focused — one concern per PR.
- Write or update tests for any logic you add or modify.
- Add Google-style docstrings to new public classes and methods.
- Never hardcode values — use `settings` from `app/config/env_config.py`.

### 4 — Check locally before pushing

```bash
black app/ && isort app/ && ruff check app/
pytest -q app/tests
```

Or let the pre-commit hooks do it for you:

```bash
pre-commit run --all-files
```

### 5 — Open a pull request

Use the [PR template](.github/pull_request_template.md) — fill in every section.  PRs with empty
descriptions are returned without review.

All commit messages must follow [Conventional Commits](https://www.conventionalcommits.org/).
The `commit-msg` hook enforces this automatically, but a quick reminder:

```
feat(agents): add timeout handling to supervisor agent
fix(repository): handle empty result set in base_repository query
docs(auth): update JWT flow diagram for refresh token support
```

---

## Standards reference

| Resource | What it covers |
|----------|----------------|
| [Pull request guidelines](./pull-request-guidelines) | Branch naming, commit format, code rules, security, testing, PR checklist, review process |
| [Architecture](./architecture) | Layer responsibilities and where new code should live |
| [Configuration](./configuration) | How to add new environment variables correctly |

---

## Licensing

By opening a pull request you agree that your contribution will be licensed under the project
license in `LICENSE.md` at the repository root.
