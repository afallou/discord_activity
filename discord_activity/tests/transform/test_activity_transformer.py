from unittest.mock import Mock

from hamcrest import assert_that, contains, has_entries

from discord_activity.app import create_app
from discord_activity.discord.constants import DAY_SECONDS


class TestActivityTransformer:
    def setup(self):
        graph = create_app(testing=True)
        self.transformer = graph.activity_transformer

    def test_messages_per_user_per_day(self):
        self.transformer.message_log = [
            Mock(author_id="user_1"),
            Mock(author_id="user_1"),
            Mock(author_id="user_2"),
            Mock(author_id="user_3"),
            Mock(author_id="user_2"),
        ]

        daily_activity = self.transformer.messages_per_user_per_day(
            buckets=[0, 10, 20, 30],
            bucket_assignments=[1, 2, 1, 3, 1],
        )

        assert_that(
            list(daily_activity.keys()),
            contains(0, 10, 20),
        )
        assert_that(
            daily_activity[0],
            has_entries(dict(
                user_1=1,
                user_2=2,
            )),
        )
        assert_that(
            daily_activity[10],
            has_entries(dict(
                user_1=1,
            )),
        )
        assert_that(
            daily_activity[20],
            has_entries(dict(
                user_3=1,
            )),
        )

    def test_get_timespan_buckets(self):
        buckets = self.transformer.get_timespan_buckets([
            1 * DAY_SECONDS + 2,
            4 * DAY_SECONDS - 10,
            2 * DAY_SECONDS + 21,
        ])
        assert_that(
            buckets,
            contains(
                float(1 * DAY_SECONDS),
                float(2 * DAY_SECONDS),
                float(3 * DAY_SECONDS),
                float(4 * DAY_SECONDS),
            )
        )
