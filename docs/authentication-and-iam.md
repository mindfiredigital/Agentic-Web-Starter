---
sidebar_position: 5
title: Authentication & IAM
description: JWT login, protected routes, and component-based ACLs when USE_SQL is enabled.
---

# Authentication & IAM

The IAM (Identity and Access Management) subsystem provides JWT-based authentication, user and
role management, and a component-level access control model.

**All IAM features require `USE_SQL=true`.** When the flag is `false`, the `/auth`, `/users`, and
`/roles` routes are not mounted and SQLite is never initialised.  Only the core routes (health,
chat, upload) remain available.

---

## How authentication works

The flow is straightforward:

1. A client sends credentials to `POST /api/v1/auth/login`.
2. The server validates the password (Argon2 via `passlib`) and loads the user's roles.
3. A signed JWT is returned.
4. Subsequent requests include the token as a Bearer header — FastAPI's dependency system verifies
   it automatically on every protected route.

On login, the server validates the password, loads the user's roles from SQLite, and returns a
signed JWT.  Every subsequent call carries that token in the `Authorization` header; the auth
dependency decodes it, checks the ACL, and passes the user context down to the handler.

---

## Login endpoint

**`POST /api/v1/auth/login`**

Handled by `app/routes/iam_routes/auth_route.py`.  
Business logic lives in `app/services/iam_services/auth_service.py`.

**Request body:**

```json
{
  "username": "alice",
  "password": "s3cr3t"
}
```

**Success response `200 OK`:**

```json
{
  "access_token": "<signed-jwt>",
  "token_type": "bearer"
}
```

**Error responses:**

| Status | Cause |
|--------|-------|
| `401 Unauthorized` | Wrong username or password |
| `404 Not Found` | IAM routes not registered (`USE_SQL=false`) |

---

## Using the token

Include the token in the `Authorization` header for every protected request:

```
Authorization: Bearer <access_token>
```

The `auth_deps.py` dependency (`app/utils/iam_utils/auth_deps.py`) extracts the token, verifies
the signature, and makes the decoded payload (user ID, role IDs) available to the route handler.

---

## Authorization model

Access control is component-based:

- A **Component** represents an API surface — typically identified by a URI pattern.
- A **Role** is assigned to a user.
- Roles are mapped to Components, defining which roles may access which surfaces.
- Services call internal `_ensure_access()` checks before any write operation.

This model is implemented in the `sql_repository/` layer and orchestrated by `iam_services/`.

---

## Admin bootstrap

If the following three variables are set in `.env` and no users yet exist in the database, the app
automatically creates an admin account on first startup:

| Variable | Description |
|----------|-------------|
| `ADMIN_USERNAME` | Login name |
| `ADMIN_EMAIL` | Email address |
| `ADMIN_PASSWORD` | Password — hashed with Argon2 before storage |

This happens inside `app/starter.py` via `AuthService.bootstrap_admin`.  On subsequent restarts the
check is a no-op if any users already exist.

---

## Key source files

| File | Responsibility |
|------|----------------|
| `app/routes/iam_routes/` | HTTP handlers for auth, users, and roles |
| `app/services/iam_services/auth_service.py` | Login logic, JWT issuance, admin bootstrap |
| `app/utils/iam_utils/jwt_utils.py` | Token creation and verification |
| `app/utils/iam_utils/auth_utils.py` | Password hashing and verification (Argon2) |
| `app/utils/iam_utils/auth_deps.py` | FastAPI dependencies for protected routes |
| `app/repository/sql_repository/` | User, role, component, and ACL data access |

---

## Further reading

- [API reference](./api-reference) — login request/response shapes and all user/role endpoints
- [Configuration](./configuration) — JWT variables and admin bootstrap settings
