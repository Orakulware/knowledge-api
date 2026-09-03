# Liveness needs no token and touches no downstream component.
GET {{host}}/health/live/
HTTP 200
[Asserts]
jsonpath "$.status" == "up"

# Readiness reports one entry per downstream component, in probe order.
# The whole stack is up in this suite, so all of them are "up".
GET {{host}}/health/ready/
HTTP 200
[Asserts]
jsonpath "$.status" == "up"
jsonpath "$.components" count == 3
jsonpath "$.components[0].name" == "database"
jsonpath "$.components[0].status" == "up"
jsonpath "$.components[0].error" == null
jsonpath "$.components[1].name" == "broker"
jsonpath "$.components[1].status" == "up"
jsonpath "$.components[2].name" == "result_backend"
jsonpath "$.components[2].status" == "up"

# Probes are not rate limited: an orchestrator polling faster than the
# 10-requests/10s budget must never be answered with a 429.
GET {{host}}/health/live/
[Options]
repeat: 15
HTTP 200
