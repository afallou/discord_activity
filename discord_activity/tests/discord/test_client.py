from hamcrest import assert_that, equal_to, has_length
from unittest.mock import patch

from discord_activity.app import create_app
from discord_activity.discord.client import DISCORD_EPOCH_START


class TestDiscordClient:
    def setup(self):
        graph = create_app(testing=True)
        self.client = graph.discord_client

    def test_iter_messages_stops_on_before(self):
        before_timestamp = (182000000000000000 >> 22) + DISCORD_EPOCH_START
        with patch("discord_activity.discord.client.get") as mock_get:
            mock_get.side_effect = [
                [dict(
                    id="181000000000000000",
                    author=dict(id=1),
                    timestamp="2018-09-09T19:45:35.602000+00:00",
                )],
                # This one should get filtered out by "before" filter
                [dict(
                    id="185000000000000000",
                    author=dict(id=1),
                    timestamp="2018-09-09T20:45:35.602000+00:00",
                )],
            ]

            iterator = self.client.iter_channel_messages(
                "channel-id",
                before_timestamp=before_timestamp,
                after_timestamp=1,
            )
            messages = [item for item in iterator]
            assert_that(messages, has_length(1))
            assert_that(messages[0].id, equal_to("181000000000000000"))

    def test_iter_messages_stops_on_empty_result(self):
        before_timestamp = (190000000000000000 >> 22) + DISCORD_EPOCH_START
        with patch("discord_activity.discord.client.get") as mock_get:
            mock_get.side_effect = [
                [dict(
                    id="181000000000000000",
                    author=dict(id=1),
                    timestamp="2018-09-09T19:45:35.602000+00:00",
                )],
                [dict(
                    id="185000000000000000",
                    author=dict(id=1),
                    timestamp="2018-09-09T20:45:35.602000+00:00",
                )],
                # `before` didn't stop iteration, so we get to the point where the server
                # returns an empty list of messages
                [],
            ]

            iterator = self.client.iter_channel_messages(
                "channel-id",
                before_timestamp=before_timestamp,
                after_timestamp=1,
            )
            messages = [item for item in iterator]
            assert_that(messages, has_length(2))

    def test_iter_channels(self):
        with patch("discord_activity.discord.client.get") as mock_get:
            mock_get.return_value = [
                dict(id="181000000000000000"),
                dict(id="185000000000000000"),
            ]
            channels = [item for item in self.client.iter_channels()]
            assert_that(channels, has_length(2))
