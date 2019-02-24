from microcosm.api import create_object_graph
from microcosm.loaders import load_each, load_from_dict, load_from_environ

import discord_activity.discord.client  # noqa: F401
import discord_activity.extract.activity_extractor  # noqa: F401
import discord_activity.transform.activity_transformer  # noqa: F401


def create_app(testing=False):
    config_loader = load_each(
        load_from_environ,
    )
    graph = create_object_graph(
        "bplc",
        testing=testing,
        loader=config_loader,
    )

    graph.use(
        "discord_client",
        "activity_extractor",
        "activity_transformer",
    )

    graph.lock()
    return graph
