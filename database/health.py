from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from database.sqlite import engine


REQUIRED_TABLES = {
    "users",
    "conversations",
    "messages",
    "alembic_version",
}


def check_database_connection(
    database_engine: Engine = engine,
) -> None:
    with database_engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def get_expected_revision() -> str:
    config = Config("alembic.ini")
    scripts = ScriptDirectory.from_config(config)

    heads = scripts.get_heads()

    if len(heads) != 1:
        raise RuntimeError(
            "Database migrations must have exactly one head."
        )

    return heads[0]


def get_current_revision(
    database_engine: Engine = engine,
) -> str | None:
    inspector = inspect(database_engine)

    if "alembic_version" not in inspector.get_table_names():
        return None

    with database_engine.connect() as connection:
        return connection.execute(
            text(
                "SELECT version_num "
                "FROM alembic_version"
            )
        ).scalar_one_or_none()


def check_required_tables(
    database_engine: Engine = engine,
) -> None:
    existing_tables = set(
        inspect(database_engine).get_table_names()
    )

    missing_tables = (
        REQUIRED_TABLES - existing_tables
    )

    if missing_tables:
        missing = ", ".join(sorted(missing_tables))

        raise RuntimeError(
            f"Database tables are missing: {missing}"
        )


def check_database_migrations(
    database_engine: Engine = engine,
) -> None:
    expected_revision = get_expected_revision()

    current_revision = get_current_revision(
        database_engine
    )

    if current_revision is None:
        raise RuntimeError(
            "Database migration revision is missing."
        )

    if current_revision != expected_revision:
        raise RuntimeError(
            "Database migration revision is not current."
        )


def check_database_readiness(
    database_engine: Engine = engine,
) -> None:
    check_database_connection(database_engine)
    check_required_tables(database_engine)
    check_database_migrations(database_engine)