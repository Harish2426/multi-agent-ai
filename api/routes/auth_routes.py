from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from api.dependencies import (
    get_auth_service,
    get_user_repository,
)
from api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from database.repositories.user_repository import (
    UserRepository,
)
from services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    service: AuthService = Depends(
        get_auth_service
    ),
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    user = service.get_current_user(
        credentials.credentials
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    return user


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    users: UserRepository = Depends(
        get_user_repository
    ),
    service: AuthService = Depends(
        get_auth_service
    ),
):
    email = request.email.lower()

    existing = users.get_by_email(email)

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )

    password_hash = service.hash_password(
        request.password
    )

    user = users.create_user(
        email=email,
        password_hash=password_hash,
    )

    token = service.create_access_token(
        user.id
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):
    user = service.authenticate(
        request.email.lower(),
        request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    token = service.create_access_token(
        user.id
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }


@router.get(
    "/me",
    response_model=dict,
)
def me(
    current_user=Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }