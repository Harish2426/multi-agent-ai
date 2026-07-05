from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.config import MAX_MESSAGE_LENGTH


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=MAX_MESSAGE_LENGTH,
    )
    conversation_id: str | None = Field(
        default=None,
        max_length=128,
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Message cannot contain only whitespace."
            )

        return value

    @field_validator("conversation_id")
    @classmethod
    def validate_conversation_id(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "conversation_id cannot be empty."
            )

        return value


class ChatResponse(BaseModel):
    response: str
    route: str
    messages: list[str]
    conversation_id: str


class HistoryItem(BaseModel):
    id: str
    role: Literal["user", "assistant"]
    content: str
    timestamp: str
    sequence: int


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    history: list[HistoryItem]


class DeleteConversationResponse(BaseModel):
    conversation_id: str
    deleted_count: int


class HealthResponse(BaseModel):
    status: str


class ReadinessResponse(BaseModel):
    status: str
    memory: str