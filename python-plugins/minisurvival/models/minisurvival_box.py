'''
The model of the minisurvival box.
'''

# pylint: disable=consider-using-f-string

# pylint: disable=import-error
from mcapi import synchronous, location
from org.bukkit import Material
# pylint: enable=import-error

from minisurvival.utils.functions import fill

class MinisurvivalBox:
    '''
    A box for the minisurvival minigame.
    '''

    __width = 0
    __height = 0
    __length = 0

    __x = 0
    __y = 0
    __z = 0

    __players = []

    def __init__(self, x, y, z, width, height, length, players):
        self.__width = width
        self.__height = height
        self.__length = length

        self.__x = x
        self.__y = y
        self.__z = z

        self.__players = players

    def __str__(self):
        return (
            'MinisurvivalBox(width={}, height={}, length={}, x={}, y={}, z={}, players={})'.format(
            self.__width,
            self.__height,
            self.__length,
            self.__x,
            self.__y,
            self.__z,
            self.__players
            )
        )

    def __repr__(self):
        return self.__str__()

    def get_width(self):
        '''
        Returns the width of the box.
        '''

        return self.__width

    def get_height(self):
        '''
        Returns the height of the box.
        '''

        return self.__height

    def get_length(self):
        '''
        Returns the length of the box.
        '''

        return self.__length

    def get_location(self):
        '''
        Returns the location of the box.
        '''

        return location(self.__x, self.__y, self.__z)

    @synchronous()
    def prepare(self):
        fill(
            [ self.__x, self.__y, self.__z ],
            self.__width,
            self.__height,
            self.__length,
            type=Material.BEDROCK
        )

        fill(
            [ self.__x + 1, self.__y + 1, self.__z + 1 ],
            self.__width - 2,
            self.__height - 2,
            self.__length - 2,
            type=Material.AIR
        )

        fill(
            [ self.__y + self.__height ],
            self.__width - 2,
            1,
            self.__length - 2,
            type=Material.BARRIER
        )
