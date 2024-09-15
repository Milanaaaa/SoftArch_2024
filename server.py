from typing import List
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

HOST = '127.0.0.1'
PORT = 8080

app = FastAPI()


class Message(BaseModel):
    text: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MessageSent(BaseModel):
    text: str = Field(...)


messages: List[Message] = []


@app.get("/messages", response_model=List[Message])
async def get_messages():
    return messages


@app.post("/messages/send", response_model=Message)
async def send_message(message_sent: MessageSent):
    message = Message(text=message_sent.text)

    messages.append(message)

    return message


@app.get("/messages/count", response_model=int)
async def get_messages_count():
    return len(messages)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
