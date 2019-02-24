from microcosm.api import binding, defaults
from microcosm_logging.decorators import logger
from requests import get
from requests.exceptions import HTTPError

from discord_activity.discord.channel import DiscordChannel
from discord_activity.discord.constants import DISCORD_EPOCH_START
from discord_activity.discord.message import DiscordMessage


@binding("discord_client")
@defaults(
    server_id="replace-me",
    bot_token="replace-me",
    base_url="https://discordapp.com/api"
)
@logger
class DiscordClient:
    def __init__(self, graph):
        self.server_id = graph.config.discord_client.server_id
        self.bot_token = graph.config.discord_client.bot_token
        self.base_url = graph.config.discord_client.base_url

    @property
    def _auth_header(self):
        return dict(Authorization=f"Bot {self.bot_token}")

    def _timestamp_to_snowflake(self, timestamp):
        """
        See https://discordapp.com/developers/docs/reference#snowflakes

        :timestamp: millisecond UNIX timestamp

        """
        return (timestamp - DISCORD_EPOCH_START) << 22

    def iter_channels(self):
        # No iteration to do here, the API endpoint returns all channels
        yield from self._get_server_channels()

    def iter_channel_messages(self, channel_id, before_timestamp=None, after_timestamp=None):
        before = self._timestamp_to_snowflake(before_timestamp)
        after = self._timestamp_to_snowflake(after_timestamp)

        # The API only accepts one of `before` or `after` - we send `after`
        # and do the `before` filtering ourselves
        while after < before:
            messages = self._get_channel_messages(
                channel_id=channel_id,
                after=after,
                # We use the largest possible limit to iterate
                limit=100,
            )
            if len(messages) == 0:
                return
            # messages are returned in descending timestamp order
            # i.e. latest message first
            after = int(messages[0].id)

            self.logger.info(
                "Extracted {count} messages starting at snowflake {after}",
                extra=dict(
                    count=len(messages),
                    after=after,
                ),
            )
            yield from [
                message
                for message in reversed(messages)
                if int(message.id) < before
            ]

    def _get_server_channels(self):
        response = get(
            f"{self.base_url}/guilds/{self.server_id}/channels",
            headers=self._auth_header,
        )
        response.raise_for_status()
        return [DiscordChannel.from_api(channel) for channel in response.json()]

    def _get_channel_messages(self,
                              channel_id,
                              after=None,
                              limit=None,
                              ):
        params = dict()
        if after is not None:
            params["after"] = after
        if limit is not None:
            params["limit"] = limit
        uri = f"{self.base_url}/channels/{channel_id}/messages"
        response = get(
            uri,
            headers=self._auth_header,
            params=params,
        )
        try:
            response.raise_for_status()
        except HTTPError as err:
            if response.status_code == 403 and response.json()["code"] == 50001:
                self.logger.warning(f"Missing access for URI {uri}")
                return []
            else:
                raise
        return [DiscordMessage.from_api(message) for message in response.json()]
