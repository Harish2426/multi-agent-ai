from collections.abc import Generator

from sqlalchemy.orm import Session

from database.sqlite import SessionLocal


def get_database_session() -> Generator[
    Session,
    None,
    None,
]:
    session = SessionLocal()

    try:
        yield session

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()