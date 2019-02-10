from csv import reader
from os.path import join
from shutil import rmtree
from tempfile import mkdtemp
from unittest.mock import patch

from hamcrest import assert_that, contains, has_length

from discord_activity.app import create_app
from discord_activity.discord.channel import DiscordChannel
from discord_activity.discord.message import DiscordMessage

class TestDiscordActivityExtractor:
    def setup(self):
        graph = create_app(testing=True)
        self.extractor = graph.activity_extractor
        self.dir_path = mkdtemp()

    def teardown(self):
        rmtree(self.dir_path)

    def test_extract(self):
        with patch.object(self.extractor.discord_client, "iter_channels") as mock_iter_channels:
            with patch.object(self.extractor.discord_client, "iter_channel_messages") as mock_iter_channel_messages:
                mock_iter_channels.return_value = [DiscordChannel(id="channel-1")]
                mock_iter_channel_messages.return_value = [
                    DiscordMessage(
                        author_id="author-1",
                        id="message-1",
                        timestamp=1536522335,
                    ),
                    DiscordMessage(
                        author_id="author-1",
                        id="message-2",
                        timestamp=1536522346,
                    ),
                ]
                outfile_path = join(self.dir_path, "output.csv")
                self.extractor(destination=outfile_path, before=1540000000, after=1530000000)

        with open(outfile_path, "r") as outfile:
            csv_reader = reader(outfile)
            rows = [row for row in csv_reader]

        assert_that(rows, has_length(3))
        assert_that(rows[0], contains("id", "author_id", "timestamp"))
        assert_that(rows[1], contains("message-1", "author-1", "1536522335"))
        assert_that(rows[2], contains("message-2", "author-1", "1536522346"))
