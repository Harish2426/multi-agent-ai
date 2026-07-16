from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import generate_latest

from api.middleware.request_logging import (
    RequestLoggingMiddleware,
)
from api.routes.auth_routes import (
    router as auth_router,
)
from api.routes.chat_routes import (
    router as chat_router,
)
from api.routes.conversation_routes import (
    router as conversation_router,
)

from app.config import settings
from app.logging_config import configure_logging


# ---------------------------------------------------------
# Configure logging before creating the application
# ---------------------------------------------------------

configure_logging()


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
Multi-Agent AI API

Features

• JWT Authentication

• Multi-Agent LangGraph workflow

• Conversation persistence

• Long-term memory

• Structured logging

• Request tracing

• Prometheus metrics
""",
    contact={
        "name": "Jami",
    },
    license_info={
        "name": "MIT",
    },
)


# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------

app.add_middleware(
    RequestLoggingMiddleware,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------

app.include_router(auth_router)

app.include_router(chat_router)

app.include_router(conversation_router)


# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------

@app.get(
    "/metrics",
    include_in_schema=False,
)
def metrics():

    return Response(
        content=generate_latest(),
        media_type="text/plain",
    )


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get(
    "/",
    tags=["System"],
)
def root():

    return {
        "message": "Multi-Agent AI API is running",
        "version": settings.app_version,
    }


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get(
    "/health",
    tags=["System"],
)
def health():

    return {
        "status": "ok",
    }


# ---------------------------------------------------------
# Readiness Check
# ---------------------------------------------------------

@app.get(
    "/ready",
    tags=["System"],
)
def ready():

    return {
        "status": "ready",
        "database": "available",
    }


# ---------------------------------------------------------
# Startup Event
# ---------------------------------------------------------

@app.on_event("startup")
def startup():

    # Reserved for future startup initialization.
    # Example:
    #
    # - warm AI models
    # - verify database connectivity
    # - initialize vector store
    #
    pass


# ---------------------------------------------------------
# Shutdown Event
# ---------------------------------------------------------

@app.on_event("shutdown")
def shutdown():

    # Reserved for graceful shutdown tasks.
    #
    # Example:
    #
    # - close database pools
    # - flush metrics
    # - close model clients
    #
    pass