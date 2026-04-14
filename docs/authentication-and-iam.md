---
sidebar_position: 5
title: Authentication & IAM
description: JWT login, protected routes, and component-based ACLs when USE_SQL is enabled.
---

# Authentication & IAM

When **`USE_SQL`** is **`true`**, the app registers IAM routes under the API v1 prefix and persists users, roles, and ACL metadata in **SQLite** (path derived from **`WORKING_DIR`** in `env_config`).

When **`USE_SQL`** is **`false`**, IAM routes are **not** mounted; only core routes (e.g. health, chat, upload depending on other flags) apply.

## Login

- **Endpoint:** `POST /api/v1/auth/login` (see **`app/routes/iam_routes/auth_route.py`**).
- **Service:** **`app/services/iam_services/auth_service.py`** — validates credentials, loads roles, issues JWT.
- **Tokens:** Created and validated in **`app/utils/iam_utils/jwt_utils.py`**; passwords verified with **`app/utils/iam_utils/auth_utils.py`** (Argon2 via passlib).

## Protected routes

- Dependencies in **`app/utils/iam_utils/auth_deps.py`** extract the bearer token and build a payload (e.g. user id and role ids) for handlers.

## Authorization (ACL)

- **Components** represent API surfaces (e.g. by URI). **Roles** are mapped to **components** so services can enforce access before mutating data.
- Repositories under **`app/repository/sql_repository/`** implement user, role, component, and ACL storage; services call **`_ensure_access()`**-style checks where applicable.

## Admin bootstrap

If **`ADMIN_USERNAME`**, **`ADMIN_EMAIL`**, and **`ADMIN_PASSWORD`** are set, **`app/starter.py`** attempts a one-time admin creation via **`AuthService.bootstrap_admin`** when no users exist.

For exact request/response shapes, use the running app’s **OpenAPI** documentation ([API reference](./api-reference)).
