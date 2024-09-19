from time import sleep
from typing import Any
from threading import Thread
from argparse import ArgumentParser
from datetime import datetime, timezone

from requests import Session


class ChatAPI:
    def __init__(self, chat_base_url: str):
        self.chat_base_url = chat_base_url
        self.http = Session()

    def get_messages(self) -> list[dict[str, Any]]:
        return self.http.get(
            self.chat_base_url + '/messages'
        ).json()

    def send_message(self, text: str) -> dict[str, Any]:
        return self.http.post(
            self.chat_base_url + '/messages/send',
            json={'text': text}
        ).json()

    def get_messages_count(self) -> int:
        return int(
            self.http.get(
                self.chat_base_url + '/messages/count'
            ).text
        )


def print_message(message: dict[str, Any]) -> None:
    ts = (datetime
          .fromisoformat(message['timestamp'])
          .replace(tzinfo=timezone.utc)
          .astimezone()
          .strftime("%m-%d %H:%M"))

    print(f"[{ts}] {message['text']}")


def process_chat(chat: ChatAPI, update_delay: float = 0.5):
    lts = None
    while True:
        messages = chat.get_messages()

        for message in messages:
            if not lts or lts < message['timestamp']:
                print_message(message)
                lts = message['timestamp']

        sleep(update_delay)


def main():
    argp = ArgumentParser('Anonymous Chat')

    argp.add_argument('-u', '--update-delay',
                      type=float, default=0.5)
    argp.add_argument('CHAT_SERVER_URL')

    args = argp.parse_args()
    update_delay, chat_server_url = args.update_delay, args.CHAT_SERVER_URL

    chat = ChatAPI(chat_server_url)

    Thread(
        target=process_chat,
        args=(chat, update_delay),
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
    except ConnectionError:
        print('[!] Connection error')
    except Exception as e:
        print(f'[!] Unknown error: {e}')
