from abc import ABC, abstractmethod
from asyncio import Future


class Chatbot(ABC):

    @abstractmethod
    def __init__(self):
        pass

    async def handle_message(self, guild_id: int, channel_id: int, user_id: int, message: str):
        if message == "!rolelive":
            await self.say(guild_id, channel_id, self.get_mention(user_id) + " Welcome To Rolelive!")

    @abstractmethod
    def say(self, guild_id: int, channel_id: int, message: str):
        raise NotImplementedError()

    @abstractmethod
    def get_mention(self, user_id: int) -> str:
        raise NotImplementedError()

    @abstractmethod
    def start_chatbot(self) -> Future:
        raise NotImplementedError()
