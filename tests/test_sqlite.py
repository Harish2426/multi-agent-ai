from sqlalchemy import inspect

from database.sqlite import (
    engine,
    init_database,
)


def test_database_initialization():
    init_database()

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    assert "conversations" in tables
    assert "messages" in tables