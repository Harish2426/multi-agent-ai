from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
    )

    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    route: str
    messages: list[str]
    conversation_id: str


class HistoryItem(BaseModel):
    id: str
    document: str
    metadata: dict[str, Any]


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    history: list[HistoryItem]


class DeleteConversationResponse(BaseModel):
    conversation_id: str
    deleted_count: int