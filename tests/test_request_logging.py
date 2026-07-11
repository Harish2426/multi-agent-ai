from fastapi.testclient import TestClient

from api.main import app


def test_response_contains_request_id():
    with TestClient(
        app,
        raise_server_exceptions=False,
    ) as client:
        response = client.get("/health")

    assert response.status_code == 200

    request_id = response.headers.get(
        "X-Request-ID"
    )

    assert request_id
    assert len(request_id) > 0


def test_existing_request_id_is_preserved():
    with TestClient(
        app,
        raise_server_exceptions=False,
    ) as client:
        response = client.get(
            "/health",
            headers={
                "X-Request-ID": "request-123",
            },
        )

    assert response.status_code == 200

    assert (
        response.headers["X-Request-ID"]
        == "request-123"
    )


def test_completed_request_is_logged(
    caplog,
):
    caplog.set_level(
        "INFO",
        logger="api.middleware.request_logging",
    )

    with TestClient(
        app,
        raise_server_exceptions=False,
    ) as client:
        response = client.get(
            "/health",
            headers={
                "X-Request-ID": "logged-request",
            },
        )

    assert response.status_code == 200

    middleware_records = [
        record
        for record in caplog.records
        if record.name
        == "api.middleware.request_logging"
    ]

    assert any(
        "request_completed" in record.getMessage()
        and "logged-request" in record.getMessage()
        for record in middleware_records
    )


def test_request_log_does_not_include_query_string(
    caplog,
):
    caplog.set_level(
        "INFO",
        logger="api.middleware.request_logging",
    )

    with TestClient(
        app,
        raise_server_exceptions=False,
    ) as client:
        response = client.get(
            "/health?token=secret-value",
        )

    assert response.status_code == 200

    middleware_records = [
        record
        for record in caplog.records
        if record.name
        == "api.middleware.request_logging"
    ]

    assert middleware_records

    assert all(
        "secret-value"
        not in record.getMessage()
        for record in middleware_records
    )