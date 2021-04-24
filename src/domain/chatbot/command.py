from abc import ABC, abstractmethod


class ChatbotCommand(ABC):

    @property
    @abstractmethod
    def alias(self) -> str:
        raise NotImplementedError

    def matches(self, command: str) -> bool:
        return command.startswith(self.alias)

    @abstractmethod
    async def handle(self, chatbot: 'Chatbot', guild_id: int, channel_id: int, user_id: int, *params):
        raise NotImplementedError
