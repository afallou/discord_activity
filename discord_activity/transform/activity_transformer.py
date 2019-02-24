from collections import Counter, defaultdict
from csv import reader, writer
from os.path import join

from microcosm.api import binding
from numpy import digitize, linspace

from discord_activity.discord.constants import DAY_SECONDS
from discord_activity.discord.message import DiscordMessage


@binding("activity_transformer")
class ActivityTransformer:
    def __init__(self, graph):
        self.message_log = []

    def __call__(self, in_csv_path, out_folder_path):
        self.load_message_log(in_csv_path)
        timestamps = [msg.seconds_timestamp for msg in self.message_log]
        buckets = self.get_timespan_buckets(timestamps)
        bucket_assignments = digitize(timestamps, buckets)
        daily_activity = self.messages_per_user_per_day(buckets, bucket_assignments)
        self.dump_daily_activity(out_folder_path, daily_activity)

    def load_message_log(self, csv_path):
        with open(csv_path, 'r') as f:
            csv_reader = reader(f)
            next(csv_reader)
            self.message_log = [
                DiscordMessage(
                    id=row[0],
                    author_id=row[1],
                    timestamp=row[2],
                    channel_id=row[3],
                )
                for row in csv_reader
            ]

    def dump_daily_activity(self, folder_path, day_activity):
        for day_timestamp, day_activity in day_activity.items():
            with open(join(folder_path, f"{int(day_timestamp)}.csv"), "w+") as f:
                csv_writer = writer(f)
                for user_id, user_message_count in day_activity.items():
                    csv_writer.writerow([user_id, user_message_count])

    def messages_per_user_per_day(self, buckets, bucket_assignments):
        """
        Compute user activity per day with the format
        {
          <timestamp for start of day>: <Counter {<user id>: <user's number of messages for the day>}>
        }

        """
        message_activity = defaultdict(list)
        for message, bucket_index in zip(self.message_log, bucket_assignments):
            # "... - 1" because numpy used 1-based indexing
            message_activity[buckets[bucket_index - 1]].append(message.author_id)

        return {
            day_timestamp: Counter(day_activity)
            for day_timestamp, day_activity
            in message_activity.items()
        }

    def get_timespan_buckets(self, timestamps):
        """
        Compute day-long buckets that can fit all items in `timestamps`

        """
        start_point = DAY_SECONDS * (min(timestamps) // DAY_SECONDS)
        end_point = DAY_SECONDS * (1 + max(timestamps) // DAY_SECONDS)
        last_message_timestamp = max(timestamps)
        return linspace(
            start_point,
            end_point,
            num=(end_point - start_point) // DAY_SECONDS + 1,
        ).tolist()
