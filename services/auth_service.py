from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from database.repositories.user_repository import (
    UserRepository,
    user_repository,
)


SECRET_KEY = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class AuthService:

    def __init__(
        self,
        user_repository_instance: (
            UserRepository | None
        ) = None,
    ):
        self.users = (
            user_repository_instance
            or user_repository
        )

    def hash_password(
        self,
        password: str,
    ) -> str:
        return pwd_context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        password_hash: str,
    ) -> bool:
        return pwd_context.verify(
            plain_password,
            password_hash,
        )

    def create_access_token(
        self,
        user_id: str,
    ) -> str:

        expire = (
            datetime.now(UTC)
            + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

        payload = {
            "sub": user_id,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

    def decode_access_token(
        self,
        token: str,
    ) -> dict | None:

        try:
            return jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
            )

        except JWTError:
            return None

    def authenticate(
        self,
        email: str,
        password: str,
    ):

        user = self.users.get_by_email(email)

        if user is None:
            return None

        if not self.verify_password(
            password,
            user.password_hash,
        ):
            return None

        return user

    def get_current_user(
        self,
        token: str,
    ):

        payload = self.decode_access_token(token)

        if payload is None:
            return None

        user_id = payload.get("sub")

        if not user_id:
            return None

        return self.users.get_by_id(user_id)


auth_service = AuthService()