from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory

from database.sqlite import Base


def test_alembic_has_single_head():
    config = Config("alembic.ini")

    scripts = ScriptDirectory.from_config(
        config
    )

    heads = scripts.get_heads()

    assert len(heads) == 1


def test_alembic_metadata_contains_tables():
    assert set(Base.metadata.tables) == {
        "users",
        "conversations",
        "messages",
    }


def test_migration_directory_exists():
    assert Path(
        "migrations/versions"
    ).is_dir()
