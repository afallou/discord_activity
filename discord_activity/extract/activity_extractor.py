from csv import writer

from microcosm.api import binding
from microcosm_logging.decorators import logger


@logger
@binding("activity_extractor")
class DiscordActivityExtractor:
    """
    Extract a message log from Discord and write it to a CSV file

    """
    def __init__(self, graph):
        self.discord_client = graph.discord_client
        self.message_log = []

    def __call__(self, destination, before, after, channel_limit=None, message_limit=None):
        channel_count = 0
        for channel in self.discord_client.iter_channels():
            if channel_limit and channel_count > channel_limit:
                break
            if message_limit and len(self.message_log) > message_limit:
                break
            self._extract_channel_messages(channel.id, before, after)
            channel_count += 1

        self._write_log_to_csv(destination)

    def _extract_channel_messages(self, channel_id, before, after):
        self.logger.warning(f"Getting messages for channel {channel_id}")
        self.message_log.extend([
            message
            for message in self.discord_client.iter_channel_messages(
                channel_id,
                before_timestamp=before,
                after_timestamp=after,
            )
        ])

    def _write_log_to_csv(self, destination):
        with open(destination, "w+") as outfile:
            csv_writer = writer(outfile)
            csv_writer.writerow(["id", "author_id", "timestamp", "channel_id"])
            for message in self.message_log:
                csv_writer.writerow([
                    message.id,
                    message.author_id,
                    message.timestamp,
                    message.channel_id,
                ])
