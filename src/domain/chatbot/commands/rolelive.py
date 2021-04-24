from domain.chatbot.command import ChatbotCommand


class RoleliveCommand(ChatbotCommand):
    @property
    def alias(self) -> str:
        return "!rolelive"

    async def handle(self, chatbot: 'Chatbot', guild_id: int, channel_id: int, user_id: int, *params):
        await chatbot.say(guild_id, channel_id, chatbot.get_mention(user_id) + " Welcome To Rolelive!")
