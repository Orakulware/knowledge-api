# Roll the shared rate-limit window fresh (see note in
# 03_post_media_record.hurl) before deliberately exhausting the
# 10-requests/10s budget shared by every rate_limiter-guarded endpoint.
# Login is used here only because it needs no bearer token; the limiter
# itself does not care which guarded endpoint is hit.
POST {{host}}/login/
[Options]
delay: 11000
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 403

# 11th request within the same 10s window -> over budget.
POST {{host}}/login/
{
    "username": "irrelevant",
    "password": "irrelevant"
}
HTTP 429
[Asserts]
jsonpath "$.error_type" == "RateLimitExceeded"
header "Retry-After" exists
