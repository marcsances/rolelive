from domain.base.entity import Entity


class Guild(Entity):
    def __init__(self):
        super().__init__()
        self.guild_id: int = 0
        self.guild_name: str = ''
