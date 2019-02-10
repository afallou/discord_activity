from csv import writer

from microcosm.api import binding


@binding("activity_extractor")
class DiscordActivityExtractor:
    """
    Extract a message log from Discord and write it to a CSV file

    """
    def __init__(self, graph):
        self.discord_client = graph.discord_client
        self.message_log = []

    def __call__(self, destination, before, after):
        for channel in self.discord_client.iter_channels():
            self._extract_channel_messages(channel.id, before, after)

        self._write_log_to_csv(destination)

    def _extract_channel_messages(self, channel_id, before, after):
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
            csv_writer.writerow(["id", "author_id", "timestamp"])
            for message in self.message_log:
                csv_writer.writerow([
                    message.id,
                    message.author_id,
                    message.timestamp,
                ])
