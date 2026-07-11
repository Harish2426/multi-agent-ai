from uuid import uuid4

from sqlalchemy.orm import Session

from database.sqlite import (
    SessionLocal,
    User,
)


class UserRepository:

    def __init__(
        self,
        session: Session | None = None,
    ):
        self.session = session or SessionLocal()
        self._owns_session = session is None

    def create_user(
        self,
        email: str,
        password_hash: str,
    ) -> User:

        user = User(
            id=str(uuid4()),
            email=email,
            password_hash=password_hash,
        )

        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

            return user

        except Exception:
            self.session.rollback()
            raise

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        return (
            self.session.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_id(
        self,
        user_id: str,
    ) -> User | None:

        return (
            self.session.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def list_users(
        self,
    ) -> list[User]:

        return (
            self.session.query(User)
            .order_by(User.created_at.desc())
            .all()
        )

    def delete_user(
        self,
        user_id: str,
    ) -> bool:

        user = self.get_by_id(user_id)

        if user is None:
            return False

        try:
            self.session.delete(user)
            self.session.commit()

            return True

        except Exception:
            self.session.rollback()
            raise

    def close(self):
        if self._owns_session:
            self.session.close()


user_repository = UserRepository()