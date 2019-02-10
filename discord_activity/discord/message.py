from datetime import datetime as dt

from discord_activity.discord.constants import DISCORD_MESSAGE_TIMESTAMP_FORMAT


def discord_to_unix_timestamp(discord_timestamp):
    return int(dt.timestamp(
        dt.strptime(
            discord_timestamp,
            DISCORD_MESSAGE_TIMESTAMP_FORMAT,
        ),
    ))


class DiscordMessage:
    def __init__(self, author_id, id, timestamp):
        self.id = id
        self.author_id = author_id
        self.timestamp = timestamp

    @classmethod
    def from_api(cls, resource_dict):
        return cls(
            author_id=resource_dict["author"]["id"],
            id=resource_dict["id"],
            timestamp=discord_to_unix_timestamp(resource_dict["timestamp"])
        )
