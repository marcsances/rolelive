from abc import ABC, abstractmethod
from asyncio import Future

from domain.chatbot.commands.init import InitCommand
from domain.chatbot.commands.rolelive import RoleliveCommand


class Chatbot(ABC):

    @abstractmethod
    def __init__(self):
        self.commands = [
            InitCommand(),
            RoleliveCommand()
        ]

    async def handle_message(self, guild_id: int, channel_id: int, user_id: int, message: str):
        for command in self.commands:
            if command.matches(message):
                await command.handle(self, guild_id, channel_id, user_id, *filter(lambda x: len(x) > 0,
                                                                                  message.replace(command.alias, "")
                                                                                  .strip()
                                                                                  .split(" ")))
                break

    @abstractmethod
    def say(self, guild_id: int, channel_id: int, message: str):
        raise NotImplementedError()

    @abstractmethod
    def get_mention(self, user_id: int) -> str:
        raise NotImplementedError()

    @abstractmethod
    def start_chatbot(self) -> Future:
        raise NotImplementedError()
