from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.auth_routes import (
    router as auth_router,
)
from api.routes.chat_routes import (
    router as chat_router,
)
from api.routes.conversation_routes import (
    router as conversation_router,
)
from api.routes.system_routes import (
    router as system_router,
)
from app.config import settings
from database.health import (
    check_database_readiness,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.database_ready = False

    check_database_readiness()

    app.state.database_ready = True

    yield

    app.state.database_ready = False


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(conversation_router)
app.include_router(system_router)