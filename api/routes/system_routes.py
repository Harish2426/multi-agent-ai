from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)


router = APIRouter(
    tags=["System"],
)


@router.get("/")
def root():
    return {
        "message": "Multi-Agent AI API is running"
    }


@router.get("/health")
def health():
    # Liveness only:
    # the process is running and can serve HTTP.
    return {
        "status": "ok"
    }


@router.get("/ready")
def ready(request: Request):
    database_ready = getattr(
        request.app.state,
        "database_ready",
        False,
    )

    if not database_ready:
        raise HTTPException(
            status_code=503,
            detail="Application is not ready.",
        )

    return {
        "status": "ready",
        "database": "available",
    }