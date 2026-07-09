from uuid import uuid4

from database.sqlite import (
    SessionLocal,
    User,
)


class UserRepository:

    def create_user(
        self,
        email: str,
        password_hash: str,
    ) -> User:

        db = SessionLocal()

        try:
            user = User(
                id=str(uuid4()),
                email=email,
                password_hash=password_hash,
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            return user

        finally:
            db.close()

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        db = SessionLocal()

        try:
            return (
                db.query(User)
                .filter(User.email == email)
                .first()
            )

        finally:
            db.close()

    def get_by_id(
        self,
        user_id: str,
    ) -> User | None:

        db = SessionLocal()

        try:
            return (
                db.query(User)
                .filter(User.id == user_id)
                .first()
            )

        finally:
            db.close()

    def list_users(
        self,
    ) -> list[User]:

        db = SessionLocal()

        try:
            return (
                db.query(User)
                .order_by(User.created_at.desc())
                .all()
            )

        finally:
            db.close()

    def delete_user(
        self,
        user_id: str,
    ) -> bool:

        db = SessionLocal()

        try:
            user = (
                db.query(User)
                .filter(User.id == user_id)
                .first()
            )

            if user is None:
                return False

            db.delete(user)
            db.commit()

            return True

        finally:
            db.close()


user_repository = UserRepository()