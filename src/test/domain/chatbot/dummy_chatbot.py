from domain.chatbot.chatbot import Chatbot


class DummyChatbot(Chatbot):

    def __init__(self):
        super().__init__()

    def say(self, guild_id: int, channel_id: int, message: str):
        print("Channel %d @ Guild %d: %s" % (channel_id, guild_id, message))

    def get_mention(self, user_id: int) -> str:
        return "<@" + str(user_id) + ">"
