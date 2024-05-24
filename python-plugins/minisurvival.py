"""
This is a plugin for the Minecraft server CraftBukkit.
It is written in Python and uses the mcapi module.
"""

# pylint: disable=consider-using-f-string

# This is needed to import the typing module.
import sys
import os

CHUNKDATA_DIR = os.path.join(os.getcwd(), "chunkdata")
SITE_PACKAGES_DIR = os.path.join(os.getcwd(), "site-packages")

sys.path.append(SITE_PACKAGES_DIR)

# pylint: disable=wrong-import-position
from typing import Callable

# pylint: disable=import-error
from mcapi import add_command, add_event_listener, yell, asynchronous, lookingat  # type: ignore

from org.bukkit.entity import Entity  # type: ignore
from org.bukkit.event.world import ChunkLoadEvent  # type: ignore

# pylint: enable=import-error

from minisurvival.utils.commands import (
    prepare_minigame,
    read_chunks,
    start_chunkgen,
    stop_chunkgen,
)
from minisurvival.utils.events import on_chunkload
from minisurvival.utils.redis import RedisClient

# pylint: enable=wrong-import-position

listeners = {}


def add_commands(funcs):
    # type: (dict[str, Callable]) -> None

    """Add a command to the server."""

    for name, func in funcs.items():
        add_command(name, func)


def add_listeners(funcs):
    # type: (dict[str, tuple[ChunkLoadEvent, Callable]]) -> None

    """Add a listener to the server."""

    for name, data in funcs.items():
        listeners[name] = add_event_listener(data[0], data[1])


@asynchronous()
def get_direction(caller, _params):
    # type: (Entity, list[str]) -> None

    """
    This command is used to test the getEyeLocation and getDirection
    methods of the Player class.

    It is not used in the minisurvival minigame.
    """

    dir1 = caller.getEyeLocation().getDirection()
    yell("dir1.x: {}, dir1.y: {}, dir1.z: {}".format(dir1.x, dir1.y, dir1.z))

    block = lookingat(caller)
    biome = block.getBiome()

    yell("biome: {}".format(biome))

    redis_client = RedisClient()

    response = redis_client.get("foo")
    yell("foo is '{}'".format(response))

    redis_client.set("foo", "test")

    response = redis_client.get("foo")
    yell("foo is '{}'".format(response))


if __name__ == "__main__":
    print("This is a plugin for the Minecraft server CraftBukkit.")
    print("It is written in Python and uses the mcapi module.")

    if not os.path.isdir(CHUNKDATA_DIR):
        print("Creating chunkdata directory.")
        os.mkdir(CHUNKDATA_DIR)

    add_commands(
        {
            "minigame:prepare": prepare_minigame,
            "minigame:direction": get_direction,
            "minigame:read_chunks": read_chunks,
            "minigame:start_mapgen": start_chunkgen,
            "minigame:stop_mapgen": stop_chunkgen,
        }
    )

    add_listeners({"on_chunkload": (ChunkLoadEvent, on_chunkload)})
