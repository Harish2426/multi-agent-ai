import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.exception_handlers import (
    model_error_handler,
    unexpected_error_handler,
)
from api.routes import router
from app.config import CORS_ORIGINS
from app.models import ModelError


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    ),
)


app = FastAPI(
    title="Multi-Agent AI API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(
    ModelError,
    model_error_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Multi-Agent AI API",
    }