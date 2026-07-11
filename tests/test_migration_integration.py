import os
import subprocess
import sys

from sqlalchemy import create_engine, inspect


def test_upgrade_head_creates_fresh_database(
    tmp_path,
):
    database_path = tmp_path / "migration_test.db"

    database_url = (
        f"sqlite:///{database_path.as_posix()}"
    )

    environment = os.environ.copy()
    environment["DATABASE_URL"] = database_url

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "upgrade",
            "head",
        ],
        capture_output=True,
        text=True,
        env=environment,
        check=False,
    )

    assert result.returncode == 0, (
        result.stdout + result.stderr
    )

    engine = create_engine(database_url)

    try:
        tables = set(
            inspect(engine).get_table_names()
        )

        assert tables == {
            "alembic_version",
            "users",
            "conversations",
            "messages",
        }

    finally:
        engine.dispose()


def test_upgrade_downgrade_upgrade_cycle(
    tmp_path,
):
    database_path = tmp_path / "migration_cycle.db"

    database_url = (
        f"sqlite:///{database_path.as_posix()}"
    )

    environment = os.environ.copy()
    environment["DATABASE_URL"] = database_url

    def run_alembic(*arguments):
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "alembic",
                *arguments,
            ],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )

    upgrade = run_alembic(
        "upgrade",
        "head",
    )

    assert upgrade.returncode == 0, (
        upgrade.stdout + upgrade.stderr
    )

    downgrade = run_alembic(
        "downgrade",
        "base",
    )

    assert downgrade.returncode == 0, (
        downgrade.stdout + downgrade.stderr
    )

    engine = create_engine(database_url)

    try:
        tables_after_downgrade = set(
            inspect(engine).get_table_names()
        )

        assert tables_after_downgrade == {
            "alembic_version",
        }

    finally:
        engine.dispose()

    second_upgrade = run_alembic(
        "upgrade",
        "head",
    )

    assert second_upgrade.returncode == 0, (
        second_upgrade.stdout
        + second_upgrade.stderr
    )

    engine = create_engine(database_url)

    try:
        tables_after_upgrade = set(
            inspect(engine).get_table_names()
        )

        assert tables_after_upgrade == {
            "alembic_version",
            "users",
            "conversations",
            "messages",
        }

    finally:
        engine.dispose()