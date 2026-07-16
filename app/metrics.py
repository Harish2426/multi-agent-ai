from prometheus_client import (
    Counter,
    Histogram,
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
)

AGENT_DURATION = Histogram(
    "agent_duration_seconds",
    "Execution time of agents",
    ["agent"],
)

CHAT_COUNT = Counter(
    "chat_requests_total",
    "Total chat requests",
)