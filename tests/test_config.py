from app.config import Settings


def test_default_settings():

    settings = Settings(
        _env_file=None
    )

    assert (
        settings.app_name
        == "Multi-Agent AI API"
    )

    assert settings.app_version == "1.0.0"

    assert (
        settings.database_url
        == "sqlite:///database/app.db"
    )

    assert settings.jwt_algorithm == "HS256"

    assert (
        settings.access_token_expire_minutes
        == 60
    )

    assert (
        "http://localhost:5173"
        in settings.cors_origins
    )


def test_cors_origins_from_string():

    settings = Settings(
        _env_file=None,
        cors_origins_raw=(
            "http://localhost:3000,"
            "http://localhost:5173"
        ),
    )

    assert settings.cors_origins == [
        "http://localhost:3000",
        "http://localhost:5173",
    ]


def test_settings_can_be_overridden():

    settings = Settings(
        _env_file=None,
        database_url="sqlite:///test.db",
        secret_key=(
            "test-secret-key-that-is-long-enough"
        ),
        access_token_expire_minutes=15,
    )

    assert (
        settings.database_url
        == "sqlite:///test.db"
    )

    assert (
        settings.access_token_expire_minutes
        == 15
    )