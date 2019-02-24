from datetime import datetime as dt

from click import argument, command, option

from discord_activity.app import create_app


def run_transform(graph, source_csv, destination_folder):
    graph.activity_transformer(source_csv, destination_folder)

@command()
@option("--input", "-i", help="Path to input CSV file")
@argument("destination")
def main(input, destination):
    graph = create_app()
    run_transform(graph, input, destination)
