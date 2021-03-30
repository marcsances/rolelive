import json
from abc import ABC, abstractmethod


class Config(ABC):

    @abstractmethod
    def __init__(self, json_file):
        self._config = None

    @property
    def config(self) -> dict:
        return self._config


class ConfigImpl(Config):
    def __init__(self, json_file: str):
        super().__init__(json_file)
        with open(json_file, "r") as f:
            self._config = json.load(f)
