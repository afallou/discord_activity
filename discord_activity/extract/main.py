from datetime import datetime as dt

from click import argument, command, option

from discord_activity.app import create_app


def run_extract(graph, destination, before, after):
    if before is None:
        before = now_utc_timestamp()
    graph.activity_extractor(destination, int(before), int(after))

def now_utc_timestamp():
    return 1000 * int(dt.timestamp(dt.utcnow()))

@command()
@option("--before", "-b")
@option("--after", "-a", required=True)
@argument("destination")
def main(before, after, destination):
    graph = create_app()
    run_extract(graph, destination, before, after)
