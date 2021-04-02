import json

from domain.base.entity import Entity
from domain.base.list_holder import ListHolder
from domain.base.reifiable import Reifiable
from domain.chatbot.chatbot import Chatbot


class Config(Entity):

    def __init__(self):
        super().__init__()
        self.chatbots: ListHolder[Reifiable[Chatbot]] = ListHolder[Reifiable[Chatbot]](lambda: Reifiable[Chatbot]())

    def load(self, json_file):
        with open(json_file, "r") as f:
            self.from_dict(json.load(f))
