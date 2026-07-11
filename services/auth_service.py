from datetime import (
    UTC,
    datetime,
    timedelta,
)

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import Settings, settings
from database.repositories.user_repository import (
    UserRepository,
    user_repository,
)


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
        settings_instance: Settings | None = None,
    ):
        self.users = (
            user_repository_instance
            or user_repository
        )

        self.settings = (
            settings_instance
            or settings
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
                minutes=(
                    self.settings
                    .access_token_expire_minutes
                )
            )
        )

        payload = {
            "sub": user_id,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            self.settings.secret_key,
            algorithm=(
                self.settings.jwt_algorithm
            ),
        )

    def decode_access_token(
        self,
        token: str,
    ) -> dict | None:

        try:
            return jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=[
                    self.settings.jwt_algorithm
                ],
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