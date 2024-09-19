import os
import sys
import unittest
from time import time

from fastapi.testclient import TestClient

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../server'
        )
    )
)

from client import ChatAPI
from server.main import app


class TestChat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app, base_url='http://testserver')

        cls.api = ChatAPI('http://testserver')
        cls.api.http = cls.client

    def test_response_time(self):
        start_time = time()

        response = self.client.get("/messages/count")

        duration = time() - start_time

        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 0.5,
                        f"Response took too long: {duration:.3f} seconds")

        print(f"Response time: {duration:.3f} seconds")

    def test_get_messages(self):
        response = self.api.get_messages()

        self.assertIsInstance(response, list)
        self.assertEqual(response, [])

    def test_send_message(self):
        message_text = 'Hello, world!'
        response = self.api.send_message(message_text)

        self.assertIsInstance(response, dict)
        self.assertEqual(response['text'], message_text)

        messages = self.api.get_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['text'], message_text)

    def test_get_messages_count(self):
        count = self.api.get_messages_count()

        self.assertEqual(count, len(self.api.get_messages()))


if __name__ == '__main__':
    unittest.main()
