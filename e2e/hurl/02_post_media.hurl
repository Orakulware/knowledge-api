# Log in to get a token for the protected media endpoint below.
POST {{host}}/login/
{
    "username": "{{admin_login}}",
    "password": "{{admin_password}}"
}
HTTP 200
[Captures]
access_token: jsonpath "$.access_token"

# Happy path: valid media is accepted and queued (fire-and-forget -> 202,
# actual persistence happens later in the async consumer and is not
# observable over HTTP, so this only checks the request contract).
POST {{host}}/media/
Authorization: Bearer {{access_token}}
{
    "media_type": "NEWSPAPER",
    "media_name": "The Daily Times",
    "metadata": {"country": "US"}
}
HTTP 202

# Missing required field -> rejected by request validation.
POST {{host}}/media/
Authorization: Bearer {{access_token}}
{
    "media_type": "NEWSPAPER"
}
HTTP 422

# Unknown media_type enum value -> rejected by request validation.
POST {{host}}/media/
Authorization: Bearer {{access_token}}
{
    "media_type": "RADIO",
    "media_name": "Some Radio Station"
}
HTTP 422

# No Authorization header -> rejected before reaching the handler.
POST {{host}}/media/
{
    "media_type": "NEWSPAPER",
    "media_name": "Unauthorized Attempt"
}
HTTP 401
