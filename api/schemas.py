from typing import List

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1
    )


class ChatResponse(BaseModel):
    response: str
    route: str
    messages: List[str]