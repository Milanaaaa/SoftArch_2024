from typing import List

from fastapi import APIRouter

from .schemas import Message, MessageSent

messages: List[Message] = []

router = APIRouter(
    prefix='/messages',
    tags=['Messages']
)


@router.get('', response_model=List[Message])
async def get_messages():
    return messages


@router.post('/send', response_model=Message)
async def send_message(message_sent: MessageSent):
    message = Message(text=message_sent.text)

    messages.append(message)

    return message


@router.get('/count', response_model=int)
async def get_messages_count():
    return len(messages)
