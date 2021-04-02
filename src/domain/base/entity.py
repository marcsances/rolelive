from abc import ABC, abstractmethod


class Entity(ABC):

    @abstractmethod
    def __init__(self):
        pass

    def __serialize(self, value):
        if isinstance(value, Entity):
            return value.to_dict()
        elif isinstance(value, list):
            return list(map(lambda item: self.__serialize(item), value))
        elif isinstance(value, dict):
            return self.__serialize_dict(value)
        elif callable(value):
            # we don't want to serialize Python methods
            return None
        else:
            return value

    def __serialize_dict(self, obj):
        out = dict()
        for key, value in obj.items():
            serialized = self.__serialize(value)
            if serialized is not None:
                out[key] = serialized
        return out

    def __deserialize(self, key, original_value, new_value):
        if isinstance(original_value, Entity):
            return original_value.from_dict(new_value)
        elif isinstance(original_value, list):
            return list(map(lambda item: self.__deserialize(key, "", item), new_value))
        elif isinstance(original_value, dict):
            return new_value
        elif callable(original_value):
            return None
        else:
            return new_value

    def __deserialize_dict(self, obj):
        for key1, value1 in self.__dict__.items():
            for key2, value2 in obj.items():
                if key1 == key2:
                    setattr(self, key1, self.__deserialize(key1, value1, value2))
        return self

    def to_dict(self):
        return self.__serialize_dict(self.__dict__)

    def from_dict(self, obj):
        return self.__deserialize_dict(obj)
