from datetime import datetime

from pydantic import BaseModel, Field


class Message(BaseModel):
    text: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MessageSent(BaseModel):
    text: str = Field(...)
