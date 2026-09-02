# The rate limiter (10 requests / 10s) is shared by every guarded endpoint and
# keyed by client IP, so it accumulates across every file in this suite. The
# 11s delay here rolls the window fresh before this file's own 5 requests,
# instead of inheriting leftover count from 01_login.hurl and 02_post_media.hurl.
POST {{host}}/login/
[Options]
delay: 11000
{
    "username": "{{admin_login}}",
    "password": "{{admin_password}}"
}
HTTP 200
[Captures]
access_token: jsonpath "$.access_token"

# Happy path: valid media record is accepted and queued (fire-and-forget ->
# 202; the FK/duplicate checks happen later in the async consumer and are not
# observable over HTTP).
POST {{host}}/
Authorization: Bearer {{access_token}}
{
    "posted_in_media": "018f2c9a-6b1a-7c3e-8f4d-1a2b3c4d5e6f",
    "content": "Breaking news content...",
    "posted_at": "2026-08-22T12:00:00Z",
    "metadata": {"source": "wire"}
}
HTTP 202

# Missing required field -> rejected by request validation.
POST {{host}}/
Authorization: Bearer {{access_token}}
{
    "content": "Missing posted_in_media"
}
HTTP 422

# Malformed UUID -> rejected by request validation.
POST {{host}}/
Authorization: Bearer {{access_token}}
{
    "posted_in_media": "not-a-uuid",
    "content": "Bad reference",
    "posted_at": "2026-08-22T12:00:00Z"
}
HTTP 422

# Malformed datetime -> rejected by request validation.
POST {{host}}/
Authorization: Bearer {{access_token}}
{
    "posted_in_media": "018f2c9a-6b1a-7c3e-8f4d-1a2b3c4d5e6f",
    "content": "Bad timestamp",
    "posted_at": "not-a-date"
}
HTTP 422

# No Authorization header -> rejected before reaching the handler.
POST {{host}}/
{
    "posted_in_media": "018f2c9a-6b1a-7c3e-8f4d-1a2b3c4d5e6f",
    "content": "Unauthorized attempt",
    "posted_at": "2026-08-22T12:00:00Z"
}
HTTP 401
