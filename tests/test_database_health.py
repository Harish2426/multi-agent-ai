from unittest.mock import patch

import pytest

from database.health import (
    check_database_migrations,
    check_database_readiness,
)


@patch(
    "database.health.get_current_revision"
)
@patch(
    "database.health.get_expected_revision"
)
def test_current_migration_is_ready(
    mock_expected,
    mock_current,
):
    mock_expected.return_value = "revision-1"
    mock_current.return_value = "revision-1"

    check_database_migrations()


@patch(
    "database.health.get_current_revision"
)
@patch(
    "database.health.get_expected_revision"
)
def test_missing_migration_revision_fails(
    mock_expected,
    mock_current,
):
    mock_expected.return_value = "revision-1"
    mock_current.return_value = None

    with pytest.raises(
        RuntimeError,
        match="migration revision is missing",
    ):
        check_database_migrations()


@patch(
    "database.health.get_current_revision"
)
@patch(
    "database.health.get_expected_revision"
)
def test_outdated_migration_revision_fails(
    mock_expected,
    mock_current,
):
    mock_expected.return_value = "revision-2"
    mock_current.return_value = "revision-1"

    with pytest.raises(
        RuntimeError,
        match="migration revision is not current",
    ):
        check_database_migrations()


@patch(
    "database.health.check_database_migrations"
)
@patch(
    "database.health.check_required_tables"
)
@patch(
    "database.health.check_database_connection"
)
def test_readiness_runs_all_checks(
    mock_connection,
    mock_tables,
    mock_migrations,
):
    check_database_readiness()

    mock_connection.assert_called_once()
    mock_tables.assert_called_once()
    mock_migrations.assert_called_once()