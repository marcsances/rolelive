import sys
from abc import ABC
from typing import TypeVar

import inject

from domain.base.config import Config
from domain.base.reifiable import Reifiable
from domain.chatbot.chatbot import Chatbot

T = TypeVar('T')


class Injector(ABC):

    @staticmethod
    def reflect(info: Reifiable[T], extra_args=None, injectors=None) -> T:
        if injectors is None:
            injectors = {}
        if extra_args is None:
            extra_args = {}
        module = __import__(info.package, fromlist=[info.module])
        klass = getattr(module, info.module)
        args = info.args
        args.update(extra_args)
        for k, v in injectors.items():
            if k in args:
                args[k] = v
        return klass(**args)

    @staticmethod
    def configure_injector(binder):
        if len(sys.argv) > 1:
            json_file = sys.argv[1]
        else:
            json_file = "config/default.json"
        config = Config()
        config.load(json_file)
        for chatbot in config.chatbots:
            bot: Chatbot = Injector.reflect(chatbot)
            bot.start_chatbot()

        # here are some examples that I leave for later use
        # catalog_repository = Injector.reflect(config["database"]["provider"])
        # catalog_service = Injector.reflect(config["catalog"]["provider"], {}, {"catalog_repository": catalog_repository})
        # index = Injector.reflect(config["index"]["provider"], {}, {"catalog_service": catalog_service})
        # binder.bind(Config, config_class)
        # binder.bind(CatalogService, catalog_service)
        # binder.bind(CatalogRepository, catalog_repository)
        # binder.bind(Index, index)
        # binder.bind(ISessionManager, DictSessionManager())

    @staticmethod
    def bind_injector():
        inject.configure(Injector.configure_injector)
