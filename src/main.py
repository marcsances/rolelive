#!/usr/bin/env python3
import asyncio
import logging
import os
from asyncio import Future
from typing import List

import inject

from domain.base.config import Config
from domain.chatbot.chatbot import Chatbot
from domain.database.dbapi.database import Database
from util.injector import Injector


@inject.param('database', Database)
@inject.param('config', Config)
async def main_coro(database: Database = None, config: Config = None):
    print("Bootstrapping system")
    connection = database.connect()
    database.get_bootstrap_queries().execute(connection.cursor())
    connection.commit()
    awaitables: List[Future] = []
    for chatbot in config.chatbots:
        bot: Chatbot = Injector.reflect(chatbot)
        # schedule chatbot to run
        awaitables.append(bot.start_chatbot())
    # actually run all scheduled futures
    await asyncio.gather(*awaitables)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if "ROLELIVE_DEBUG" in os.environ:
        logging.basicConfig(level=logging.DEBUG)
    Injector.bind_injector()
    loop.run_until_complete(main_coro())
