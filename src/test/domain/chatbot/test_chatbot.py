from unittest import mock

from test.domain.chatbot.dummy_chatbot import DummyChatbot


class TestChatbot:

    @mock.patch.object(DummyChatbot, "say")
    def test_rolelive_command_replies_with_correct_message(self, mocked_method):
        sut = DummyChatbot()
        sut.handle_message(1, 2, 3, "!rolelive")
        mocked_method.assert_called_once_with(1, 2, "<@3> Welcome To Rolelive!")
