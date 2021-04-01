from abc import ABC, abstractmethod


class Chatbot(ABC):

    @abstractmethod
    def __init__(self):
        pass

    def handle_message(self, guild_id: int, channel_id: int, user_id: int, message: str):
        if message == "!rolelive":
            self.say(guild_id, channel_id, self.get_mention(user_id) + " Welcome To Rolelive!")

    @abstractmethod
    def say(self, guild_id: int, channel_id: int, message: str):
        raise NotImplementedError()

    @abstractmethod
    def get_mention(self, user_id: int) -> str:
        raise NotImplementedError()