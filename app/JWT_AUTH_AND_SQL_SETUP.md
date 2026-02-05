# JWT, Auth API Endpoints, and SQL Setup

This document describes how JSON Web Tokens (JWT), authentication-related API endpoints, and the SQLite database are set up in this repository.

---

## Table of Contents

1. [JWT Overview](#jwt-overview)
2. [JWT Configuration](#jwt-configuration)
3. [JWT Flow](#jwt-flow)
4. [Auth-Related API Endpoints](#auth-related-api-endpoints)
5. [SQL Setup](#sql-setup)
6. [Environment Variables](#environment-variables)

---

## JWT Overview

The app uses **JWT access tokens** for stateless authentication. After a user logs in with username and password, the server issues a signed token. Protected endpoints expect this token in the `Authorization: Bearer <token>` header.

- **Library:** PyJWT (`jwt`).
- **Algorithm:** Configurable (default `HS256`).
- **Token payload:** `sub` (user id), `role_ids` (list of role ids), `exp` (expiration).

---

## JWT Configuration

Configuration is read from environment variables via `app/config/env_config.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_SECRET_KEY` | Secret used to sign and verify tokens. **Must be set in production.** | `"change-me"` |
| `JWT_ALGORITHM` | Algorithm for signing (e.g. `HS256`). | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes. | `30` |

---

## JWT Flow

### 1. Token creation (`app/utils/jwt_utils.py`)

- **`create_access_token(user_id, role_ids, expires_minutes=None)`**
  - Builds payload: `sub` = user id, `role_ids` = list of role ids, `exp` = UTC expiry.
  - Uses `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` if `expires_minutes` is not provided.
  - Returns a signed JWT string (e.g. for the login response).

### 2. Token validation (`app/utils/jwt_utils.py`)

- **`decode_access_token(token)`**
  - Verifies signature and expiry using `JWT_SECRET_KEY` and `JWT_ALGORITHM`.
  - Raises `JWTError` on invalid or expired token.
  - Returns the decoded payload dict.

### 3. FastAPI dependency (`app/utils/auth_deps.py`)

- **`get_current_user_payload(credentials: HTTPAuthorizationCredentials = Depends(security))`**
  - Uses `HTTPBearer` to read `Authorization: Bearer <token>`.
  - If missing or not Bearer → `401 Unauthorized`.
  - Calls `decode_access_token(credentials.credentials)`; on `JWTError` → `401`.
  - Returns a **`TokenPayload`** Pydantic model: `sub` (user id) and `role_ids` (list of strings).

Protected routes declare:

```python
payload: TokenPayload = Depends(get_current_user_payload)
```

and then use `payload.sub` and `payload.role_ids` for authorization.

### 4. Login and password verification

- **Login** (`app/routes/auth_route.py` → `app/services/auth_service.py`):
  - Accepts `LoginRequest` (username, password).
  - Looks up user by username, verifies password with **bcrypt** (`app/services/security.py`: `verify_password`).
  - Loads user’s roles from DB, builds `role_ids`, calls `create_access_token(user_id, role_ids)`.
  - Returns `TokenResponse` with `access_token` and `token_type: "bearer"`.
- **Password hashing** (`app/services/security.py`): `hash_password` / `verify_password` via Passlib with bcrypt.

---

## Auth-Related API Endpoints

All auth-related routes are mounted under **`/api/v1`** (see `app/starter.py`).

### Public (no JWT)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/auth/login` | Login with `username` and `password` (JSON). Returns `access_token` and `token_type: "bearer"`. |

**Request body (login):**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response (login):**

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Protected (require `Authorization: Bearer <token>`)

**Users** (`/api/v1/users`):

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/users` | List users (filtered by caller’s roles). |
| `GET` | `/api/v1/users/{user_id}` | Get one user. |
| `POST` | `/api/v1/users` | Create user. |
| `PUT` | `/api/v1/users/{user_id}` | Update user. |
| `DELETE` | `/api/v1/users/{user_id}` | Delete user. |

**Roles** (`/api/v1/roles`):

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/roles` | List roles. |
| `GET` | `/api/v1/roles/{role_id}` | Get one role. |
| `POST` | `/api/v1/roles` | Create role. |
| `PUT` | `/api/v1/roles/{role_id}` | Update role. |
| `DELETE` | `/api/v1/roles/{role_id}` | Delete role. |

User and role endpoints use `TokenPayload` (from `get_current_user_payload`) for permission checks (e.g. which users/roles the caller can see or modify). Chat and ingestion routes in this repo do **not** currently require JWT.

### Auth error responses

- **401 Unauthorized:** Missing/invalid Bearer token, expired token, or invalid login credentials. Handled by `AuthenticationError` and JWT validation in `auth_deps`.
- **403 Forbidden:** `PermissionDeniedError` when the caller is not allowed to perform the action.

---

## SQL Setup

### Database and connection

- **Engine:** SQLite.
- **Connection:** `app/repository/sqlite_repository.py`.
  - **`get_db()`** – FastAPI dependency that yields a single SQLite connection per request; closes it when the request ends.
  - **`_connect()`** – Opens `settings.DB_PATH`, sets `row_factory = sqlite3.Row`, and runs `PRAGMA foreign_keys=ON`.
- **Initialization:** **`init_db()`** is called once at app startup in `app/starter.py`. It creates all tables if they do not exist.

### Tables created by `init_db()`

1. **`users`**
   - `id` (TEXT, PK), `username` (TEXT, UNIQUE), `email` (TEXT, UNIQUE), `hashed_password` (TEXT), `created_at`, `created_by`, `updated_at`, `updated_by`.

2. **`roles`**
   - `id` (TEXT, PK), `name` (TEXT, UNIQUE), `description` (TEXT), `created_at`, `created_by`, `updated_at`, `updated_by`.

3. **`components`**
   - `id` (TEXT, PK), `name` (TEXT, UNIQUE), `component_uri` (TEXT, UNIQUE), `created_at`, `created_by`, `updated_at`, `updated_by`.

4. **`user_role_mapping`**
   - `user_id`, `role_id` (composite PK), with `FOREIGN KEY` to `users(id)` and `roles(id)` and `ON DELETE CASCADE`.

5. **`role_component_mapping`**
   - `role_id`, `component_id` (composite PK), with `FOREIGN KEY` to `roles(id)` and `components(id)` and `ON DELETE CASCADE`.

All timestamp columns used for audit are TEXT (e.g. ISO UTC). IDs are UUIDs stored as TEXT.

### Repositories (data access)

- **`UserRepository`** (`app/repository/user_repository.py`) – Users and user–role links: create/get/update/delete user, list users, `get_roles_for_user(user_id)`.
- **`RoleRepository`** (`app/repository/role_repository.py`) – Roles CRUD.
- **`ACLRepository`** (`app/repository/acl_repository.py`) – `get_component_ids_for_roles(role_ids)` from `role_component_mapping`.
- **`ComponentRepository`** (`app/repository/component_repository.py`) – Components CRUD.

Domain models live in `app/models/entities.py` (e.g. `User`, `Role`, `Component`). Services (e.g. `AuthService`, `UserService`, `RoleService`) use these repositories and enforce permissions using `role_ids` from the JWT payload.

---

## Environment Variables

Relevant variables for JWT and SQL (see `env.example` and `app/config/env_config.py`):

**Database**

- `DB_PATH` – Path to the SQLite file (e.g. `./app.db`).

**JWT**

- `JWT_SECRET_KEY` – Secret for signing/verifying tokens; set a strong value in production.
- `JWT_ALGORITHM` – e.g. `HS256`.
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` – Access token lifetime (default `30`).

Copy `env.example` to `.env` and set these (and other app settings) as needed for your environment.
