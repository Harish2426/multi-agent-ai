from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.chat_routes import router as chat_router
from api.routes.conversation_routes import (
    router as conversation_router,
)

app = FastAPI(
    title="Multi-Agent AI API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(conversation_router)