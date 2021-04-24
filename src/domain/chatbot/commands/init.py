from domain.chatbot.command import ChatbotCommand


class InitCommand(ChatbotCommand):
    @property
    def alias(self) -> str:
        return "!rolelive.init"

    async def handle(self, chatbot: 'Chatbot', guild_id: int, channel_id: int, user_id: int, *params):
        if len(params) == 0:
            return await chatbot.say(guild_id, channel_id, chatbot.get_mention(user_id) +
                                     " please enter the channel you wish to set as the notifications channel. " +
                                     "Example: {} #livestreams".format(self.alias))
        channel = params[0]
        await chatbot.say(guild_id, channel_id, "OK " + chatbot.get_mention(user_id) + ", I've set " + channel +
                          " as the notifications channel for your server. Welcome to RoleLive!")
