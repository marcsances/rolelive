import asyncio
from unittest import mock
from unittest.mock import MagicMock

from test.domain.chatbot.dummy_chatbot import DummyChatbot


# monkey patch MagicMock
async def async_magic():
    pass

MagicMock.__await__ = lambda x: async_magic().__await__()

class TestChatbot:

    @mock.patch.object(DummyChatbot, "say")
    def test_rolelive_command_replies_with_correct_message(self, mocked_method):
        sut = DummyChatbot()
        asyncio.get_event_loop().run_until_complete(sut.handle_message(1, 2, 3, "!rolelive"))
        mocked_method.assert_called_once_with(1, 2, "<@3> Welcome To Rolelive!")
