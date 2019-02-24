from datetime import datetime as dt

from click import argument, command, option

from discord_activity.app import create_app


def run_extract(graph, destination, before, after, channel_limit, message_limit):
    if before is None:
        before = now_utc_timestamp()
    graph.activity_extractor(destination, 1000 * before, 1000 * after, channel_limit, message_limit)

def now_utc_timestamp():
    return int(dt.timestamp(dt.utcnow()))

@command()
@option("--before", "-b", type=int, help="Late time boundary for discord messages - as a Unix seconds timestamp")
@option("--after", "-a", type=int, required=True, help="Early time boundary for discord messages - as a Unix seconds timestamp")
@option("--channel-limit", type=int, help="Limit on number of channels to get messages from")
@option("--message-limit", type=int, help="Limit on number of extracted messages")
@argument("destination")
def main(before, after, destination, channel_limit, message_limit):
    graph = create_app()
    run_extract(graph, destination, before, after, channel_limit, message_limit)
