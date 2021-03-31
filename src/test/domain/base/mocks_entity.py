from domain.base.entity import Entity


class EmptyEntity(Entity):

    def __init__(self):
        super().__init__()


class EmptyEntityWithMethods(Entity):

    def __init__(self):
        super().__init__()

    def my_method_that_shouldnt_be_serialized(self):
        print("Hello")


class EntityWithOneField(Entity):

    def __init__(self):
        super().__init__()
        self.my_field = "Hello"


class EntityWithList(Entity):

    def __init__(self):
        super().__init__()
        self.my_list = ["item1", "item2"]


class EntityWithChild(Entity):

    def __init__(self):
        super().__init__()
        self.my_field = "Hey there"
        self.my_child = EntityWithOneField()


class EntityWithMoreChild(Entity):

    def __init__(self):
        super().__init__()
        self.my_field = "Deeper"
        self.my_child = EntityWithChild()
        self.another_child = EntityWithList()
        self.this_one_is_empty = EmptyEntityWithMethods()


class EntityWithDict(Entity):

    def __init__(self):
        super().__init__()
        self.my_dict = {"key": "value", "foo": "bar"}
