"""
The model for a tree in the minisurvival game.
"""

# pylint: disable=import-error
from mcapi import location  # type: ignore
from org.bukkit import Location  # type: ignore

# pylint: enable=import-error


class MinisurvivalTree:
    """This class represents a tree in the minisurvival game.

    Returns:
        MinisurvivalTree: A new instance of MinisurvivalTree.

    """

    __x = 0
    __y = 0
    __z = 0

    def __init__(self, x, y, z):
        self.__x = x
        self.__y = y
        self.__z = z

    def location(self):
        # type: () -> Location
        """
        Returns the location of the tree.
        """

        return location(self.__x, self.__y, self.__z)

    def generate(self):
        """
        Generates the tree.
        """

        pass
