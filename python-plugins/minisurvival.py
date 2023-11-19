"""
This is a plugin for the Minecraft server CraftBukkit.
It is written in Python and uses the mcapi module.
"""

# pylint: disable=consider-using-f-string

# This is needed to import the typing module.
import sys
from os.path import abspath, sep

sys.path.append(abspath(".") + sep + "site-packages")

# pylint: disable=wrong-import-position

# pylint: disable=import-error
from mcapi import add_command, yell, asynchronous, lookingat  # type: ignore
from org.bukkit.entity import Entity  # type: ignore

# pylint: enable=import-error

from minisurvival.utils.commands import prepare_minigame
from minisurvival.utils.redis import RedisClient

# pylint: enable=wrong-import-position


def add_commands(funcs):
    """Add a command to the server."""

    for name, func in funcs.items():
        add_command(name, func)


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


add_commands(
    {"minigame:prepare": prepare_minigame, "minigame:direction": get_direction}
)
