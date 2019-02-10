from datetime import datetime as dt

from click import argument, command, option

from discord_activity.app import create_app


def run_extract(graph, destination, before, after):
    if before is None:
        before = now_utc_timestamp()
    graph.activity_extractor(destination, 1000 * int(before), 1000 * int(after))

def now_utc_timestamp():
    return int(dt.timestamp(dt.utcnow()))

@command()
@option("--before", "-b", help="Late time boundary for discord messages - as a Unix seconds timestamp")
@option("--after", "-a", required=True, help="Early time boundary for discord messages - as a Unix seconds timestamp")
@argument("destination")
def main(before, after, destination):
    graph = create_app()
    run_extract(graph, destination, before, after)
