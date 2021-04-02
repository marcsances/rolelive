from domain.base.entity import Entity
from domain.base.list_holder import ListHolder
from domain.base.reifiable import Reifiable


class Config(Entity):

    def __init__(self):
        super().__init__()
        self.chatbots: ListHolder[Reifiable] = ListHolder[Reifiable](lambda: Reifiable())
