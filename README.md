# knowledge-api

A FastAPI service for ingesting and managing events parsed from external newsletters (Telegram, Bloomberg, etc.).

---

## Feature Backlog

---

### Feature 1 — User Management (Admin-only creation)

Users exist in the platform but cannot register themselves. The admin creates accounts directly in the database.

#### Acceptance Criteria

- No `POST /register` endpoint exists or is reachable by clients
- A `User` record contains: `id`, `email`, `password_hash`, `is_active`, `created_at`
- Passwords are stored as bcrypt hashes — never plaintext
- Only `is_active = true` users can authenticate
- Admin creates users via a DB script or CLI command (not an API)

#### Scenarios

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Admin inserts a user row directly into the DB | User attempts login with those credentials | Login succeeds and token is issued |
| 2 | No registration endpoint is implemented | Client sends `POST /auth/register` | `404 Not Found` is returned |
| 3 | User exists but `is_active = false` | User attempts login | `401 Unauthorized` — account inactive |
| 4 | A user record is inserted with a plaintext password by mistake | System checks the password field | Hash validation fails, login rejected |

---

### Feature 2 — JWT Stateful Authentication

Users log in via `POST /auth/login`. The server issues a signed JWT and persists a token record in the DB (stateful), enabling logout and revocation.

#### Acceptance Criteria

- `POST /auth/login` accepts `{ email, password }` and returns a signed JWT
- JWT payload includes `user_id` and a unique `jti` (JWT ID) claim
- A `Token` record is stored in DB: `jti`, `user_id`, `expires_at`, `revoked`
- Every request to a protected endpoint validates the JWT signature **and** checks the DB record is not expired/revoked
- `POST /auth/logout` marks the token as `revoked = true` in the DB
- Tokens expire after a configurable TTL (e.g., 24h)

#### Scenarios

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Valid email and password | `POST /auth/login` | `200 OK` with `{ access_token, token_type }` |
| 2 | Wrong password | `POST /auth/login` | `401 Unauthorized` |
| 3 | Non-existent email | `POST /auth/login` | `401 Unauthorized` (no user enumeration) |
| 4 | Valid JWT, token record active in DB | Request to any protected endpoint | Request proceeds, `200 OK` |
| 5 | Valid JWT signature, but token is past `expires_at` | Request to any protected endpoint | `401 Unauthorized` — token expired |
| 6 | Valid JWT, user calls logout | `POST /auth/logout` | `200 OK`, token record set to `revoked = true` |
| 7 | Previously valid JWT, but now revoked | Request to protected endpoint | `401 Unauthorized` — token revoked |
| 8 | No `Authorization` header | Request to any protected endpoint | `401 Unauthorized` |
| 9 | Malformed or tampered JWT | Request to any protected endpoint | `401 Unauthorized` |

---

### Feature 3 — Post Events

Authenticated users can post events — structured records parsed from external newsletters (Telegram channels, Bloomberg, etc.).

#### Acceptance Criteria

- `POST /events` is a protected endpoint (requires valid JWT)
- An `Event` record contains: `id`, `user_id`, `source`, `title`, `content`, `published_at`, `created_at`, `raw_content` (optional)
- `source` is a constrained enum: `TELEGRAM`, `BLOOMBERG`, `OTHER` (extensible)
- `published_at` is the original publication timestamp from the source, not the ingestion time
- The event is linked to the user who posted it via `user_id`
- Response on success: `201 Created` with the full event object including `id`

#### Scenarios

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Authenticated user, valid payload | `POST /events` | `201 Created` with event including generated `id` |
| 2 | No auth token | `POST /events` | `401 Unauthorized` |
| 3 | Revoked/expired token | `POST /events` | `401 Unauthorized` |
| 4 | Missing required field (`title`) | `POST /events` | `422 Unprocessable Entity` with field error |
| 5 | `source = "TELEGRAM"` in payload | `POST /events` | Event stored with `source = TELEGRAM` |
| 6 | `source = "BLOOMBERG"` in payload | `POST /events` | Event stored with `source = BLOOMBERG` |
| 7 | Unknown `source` value | `POST /events` | `422 Unprocessable Entity` |
| 8 | `published_at` is in the past (backdated newsletter) | `POST /events` | Event stored with the provided `published_at`, not overridden |
