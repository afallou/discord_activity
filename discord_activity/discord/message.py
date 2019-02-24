from datetime import datetime as dt

from discord_activity.discord.constants import MESSAGE_FULL_TIMESTAMP_FORMAT, MESSAGE_REDUCED_TIMESTAMP_FORMAT


def to_datetime(discord_timestamp):
    try:
        return dt.strptime(
            discord_timestamp,
            MESSAGE_FULL_TIMESTAMP_FORMAT,
        )
    except ValueError:
        return dt.strptime(
            discord_timestamp,
            MESSAGE_REDUCED_TIMESTAMP_FORMAT,
        )


class DiscordMessage:
    def __init__(self,
                 id,
                 author_id=None,
                 timestamp=None,
                 content=None,
                 author_name=None,
                 channel_id=None
                ):
        self.id = id
        self.author_id = author_id
        self.timestamp = timestamp
        if self.timestamp is not None:
            self.date_time = to_datetime(timestamp)
            self.seconds_timestamp = int(dt.timestamp(self.date_time))
        self.content = content
        self.author_name = author_name
        self.channel_id = channel_id

    @classmethod
    def from_api(cls, resource_dict):
        return cls(
            author_id=resource_dict["author"]["id"],
            id=resource_dict["id"],
            timestamp=resource_dict["timestamp"],
            content=resource_dict["content"],
            author_name=resource_dict["author"]["username"],
            channel_id=resource_dict["channel_id"],
        )
