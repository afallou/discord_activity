class DiscordChannel:
    def __init__(self, id):
        self.id = id

    @classmethod
    def from_api(cls, resource_dict):
        return cls(id=resource_dict["id"])
