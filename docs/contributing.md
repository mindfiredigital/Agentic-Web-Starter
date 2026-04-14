---
sidebar_position: 7
title: Contributing
description: How to contribute and where to find pull request standards.
---

# Contributing

We welcome issues, documentation improvements, and code contributions.

## Workflow (summary)

1. Fork and clone the repository.
2. Create a branch that matches your team’s naming rules (see [Pull request guidelines](./pull-request-guidelines#1-branch-naming)).
3. Install dev dependencies: **`make setup`** (or `pip install -e ".[dev]"` and pre-commit hooks as in the root **`README.md`**).
4. Make changes; run **Black**, **isort**, **Ruff**, and **pytest** locally (same checks as CI).
5. Open a pull request with a **complete description** using the template in [Pull request guidelines](./pull-request-guidelines#7-pr-description--checklist).

## Canonical guides

| Resource | Contents |
|----------|----------|
| **[Pull request guidelines](./pull-request-guidelines)** | Branch names, Conventional Commits, architecture rules, security, testing, full PR template |
| **[CONTRIBUTING.md](https://github.com/thiga-mindfire/agentic_web_starter/blob/main/CONTRIBUTING.md)** in the repo root | Same workflow, links into this docs site |

If you use a fork, open `CONTRIBUTING.md` at the root of your clone instead of the link above.

## Licensing

Contributions are accepted under the license in **`LICENSE.md`** at the repository root.
