import inject

from domain.chatbot.command import ChatbotCommand
from domain.database.dbapi.database import Database


class InitCommand(ChatbotCommand):
    @property
    def alias(self) -> str:
        return "!rolelive.init"

    @inject.param('database', Database)
    def create_guild(self, guild_id: int, guild_name: str, database: Database = None):
        database.get_guild_queries().create_guild(guild_id, guild_name).execute(database.connection.cursor())

    @inject.param('database', Database)
    def set_channel(self, guild_id: int, channel: str, database: Database = None):
        database.get_guild_queries().set_guild_preference(guild_id, "channel", channel).execute(database.connection.cursor())

    @inject.param('database', Database)
    async def handle(self, chatbot: 'Chatbot', guild_id: int, channel_id: int, user_id: int, *params,
                     database: Database = None):
        if len(params) == 0:
            return await chatbot.say(guild_id, channel_id, chatbot.get_mention(user_id) +
                                     " please enter the channel you wish to set as the notifications channel. " +
                                     "Example: {} #livestreams".format(self.alias))
        channel = params[0]
        self.create_guild(guild_id, chatbot.get_guild_name(guild_id))
        #self.set_channel(guild_id, channel)
        database.connection.commit()
        await chatbot.say(guild_id, channel_id, "OK " + chatbot.get_mention(user_id) + ", I've set " + channel +
                          " as the notifications channel for your server. Welcome to RoleLive!")
