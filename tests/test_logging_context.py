from app.logging_context import (
    get_request_id,
    reset_request_id,
    set_request_id,
)


def test_default_request_id():
    assert get_request_id() == "-"


def test_request_id_can_be_set_and_reset():
    token = set_request_id(
        "request-123"
    )

    try:
        assert (
            get_request_id()
            == "request-123"
        )

    finally:
        reset_request_id(token)

    assert get_request_id() == "-"