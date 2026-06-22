from prometheus_client import Counter

auth_failures_total = Counter(
    "auth_failures_total", 
    "Total number of authentication failures"
)

websocket_auth_failures_total = Counter(
    "websocket_auth_failures_total", 
    "Total number of websocket authentication failures"
)

token_refresh_total = Counter(
    "token_refresh_total", 
    "Total number of tokens refreshed"
)

permission_denials_total = Counter(
    "permission_denials_total", 
    "Total number of permission denials",
    ["role", "permission"]
)

tenant_requests_total = Counter(
    "tenant_requests_total", 
    "Total number of requests per tenant",
    ["tenant_id"]
)

api_key_usage_total = Counter(
    "api_key_usage_total", 
    "Total number of API key usages",
    ["tenant_id"]
)

audit_events_total = Counter(
    "audit_events_total", 
    "Total number of audit events generated",
    ["action"]
)
