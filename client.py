import sys
from time import sleep
from threading import Thread
from datetime import datetime, timezone

from requests import Session

CHAT_BASE_URL = 'http://127.0.0.1:8080'

CHAT_UPDATE_DELAY = 0.1


class ChatAPI:
    def __init__(self):
        self.http = Session()

    def get_messages(self):
        return self.http.get(
            CHAT_BASE_URL + '/messages'
        ).json()

    def send_message(self, text: str):
        return self.http.post(
            CHAT_BASE_URL + '/messages/send',
            json={'text': text}
        ).json()

    def get_messages_count(self) -> int:
        return int(
            self.http.get(
                CHAT_BASE_URL + '/messages/count'
            ).text
        )


def print_message(message: dict):
    ts = (datetime
          .fromisoformat(message['timestamp'])
          .replace(tzinfo=timezone.utc)
          .astimezone()
          .strftime("%m-%d %H:%M"))

    print(f"[{ts}] {message['text']}")


def process_chat(chat: ChatAPI):
    lts = None
    while True:
        messages = chat.get_messages()

        for message in messages:
            if not lts or lts < message['timestamp']:
                print_message(message)
                lts = message['timestamp']

        sleep(CHAT_UPDATE_DELAY)


def main():
    chat = ChatAPI()

    Thread(
        target=process_chat,
        args=(chat,),
        daemon=True
    ).start()

    while True:
        text = input()

        print('\033[F\033[K', end='')
        if text == '/count':
            print(
                '[*] Total messages count:',
                chat.get_messages_count()
            )
        else:
            chat.send_message(text)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[*] Exited')
