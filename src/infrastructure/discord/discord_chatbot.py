import asyncio
from asyncio import Future

from discord import Client, Message

from domain.chatbot.chatbot import Chatbot


class DiscordChatbot(Chatbot, Client):
    def __init__(self, bot_token):
        Chatbot.__init__(self)
        Client.__init__(self)
        self.__bot_token = bot_token

    async def say(self, guild_id: int, channel_id: int, message: str):
        channel = self.get_channel(channel_id)
        if not channel:
            return
        coro = channel.send(message)
        task = asyncio.create_task(coro)
        # This needs to change soon.
        # I am worried on the performance of this once it scales up.
        # Problem is out of order execution in the same channel.
        # Maybe queues could solve it. For now I'm leaving it like this but it needs a second thought.
        await asyncio.wait(task)

    async def on_message(self, message: Message):
        if message.author.bot:
            return
        await self.handle_message(message.guild.id, message.channel.id, message.author.id, message.content)

    async def on_ready(self):
        print("Discord Chatbot started")

    def start_chatbot(self) -> Future:
        return asyncio.create_task(self.start(self.__bot_token))

    def get_mention(self, user_id: int) -> str:
        return "<@" + str(user_id) + ">"
