"""
The model for a player in the minisurvival game.
"""

from typing import Union

# pylint: disable=import-error
from mcapi import player  # type: ignore
from org.bukkit.entity import Player  # type: ignore

# pylint: enable=import-error


class MinisurvivalPlayer:
    """This class is used to store the player's data."""

    __player = None  # type: Union[Player, None]

    def __init__(self, player_name):
        # type: (str) -> None

        self.__player = player(player_name)
