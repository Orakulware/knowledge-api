# Correct credentials issue a bearer token and set the auth cookie.
POST {{host}}/login/
{
    "username": "{{admin_login}}",
    "password": "{{admin_password}}"
}
HTTP 200
[Captures]
access_token: jsonpath "$.access_token"
[Asserts]
jsonpath "$.access_token" != ""
cookie "access_token_cookie" exists

# Wrong credentials are rejected, no token issued.
POST {{host}}/login/
{
    "username": "{{admin_login}}",
    "password": "definitely-wrong"
}
HTTP 403
[Asserts]
jsonpath "$.code" == "INVALID_CREDENTIALS"
