from microcosm.api import create_object_graph

import discord_activity.discord.client  # noqa: F401
import discord_activity.extract.activity_extractor  # noqa: F401


def create_app(testing=False):
    graph = create_object_graph("bplc", testing=testing)

    graph.use(
        "discord_client",
        "activity_extractor",
    )

    graph.lock()
    return graph
