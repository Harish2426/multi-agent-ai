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

from api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from database.repositories.user_repository import (
    user_repository,
)
from services.auth_service import auth_service


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
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    user = auth_service.get_current_user(
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
def register(request: RegisterRequest):

    email = request.email.lower()

    existing = user_repository.get_by_email(
        email
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )

    password_hash = auth_service.hash_password(
        request.password
    )

    user = user_repository.create_user(
        email=email,
        password_hash=password_hash,
    )

    token = auth_service.create_access_token(
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
def login(request: LoginRequest):

    user = auth_service.authenticate(
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

    token = auth_service.create_access_token(
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