'''
The model of the minisurvival box.
'''

# pylint: disable=consider-using-f-string
from functools import partial
from random import randint
from itertools import chain

# pylint: disable=import-error
from mcapi import asynchronous, location, teleport, yell, getblock, setblock
from org.bukkit import Material
# pylint: enable=import-error

from minisurvival.utils.functions import cuboid, dispatch_command

class MinisurvivalBox:
    '''
    A box for the minisurvival minigame.
    '''

    __width = 39
    __height = 21
    __length = 39

    __GROUND_HEIGHT_MULTIPLIER = 0.6

    __position = None
    __exit_door = None

    __players = []

    def __init__(self, position, players):
        self.__x = position.x
        self.__y = position.y + 1
        self.__z = position.z

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

    def size(self):
        '''
        Returns the size of the box.
        '''

        return [ self.__width, self.__height, self.__length ]

    def width(self):
        '''
        Returns the width of the box.
        '''

        return self.__width

    def height(self):
        '''
        Returns the height of the box.
        '''

        return self.__height

    def length(self):
        '''
        Returns the length of the box.
        '''

        return self.__length

    def location(self):
        '''
        Returns the location of the box.
        '''

        return location(self.__x, self.__y, self.__z)

    def exit_position(self):
        '''
        Returns the position of the exit door.
        '''

        return self.__exit_door

    def __calc_size(self):
        '''
        Sets the size of the box for the given amount of players.
        '''

        yell('Calculating size of box for {} players...'.format(len(self.__players)))

        self.__width += len(self.__players) // 2 * 10
        self.__height += len(self.__players) // 4 * 10
        self.__length += len(self.__players) // 2 * 10

    def __run_commands(self, queue):
        '''
        Runs the given commands.
        '''

        for command in queue:
            command()

    @asynchronous()
    def prepare(self):
        '''
        Prepares the box.
        '''

        yell('Preparing minigame for {} players...'.format(len(self.__players)))
        self.__calc_size()

        yell('Calculated size of the box: {}x{}x{}, preparing arena...'.format(
            self.__width,
            self.__height,
            self.__length
        ))
        queue = chain.from_iterable(
            chain(
                self.__teleport_players(self.height() + 1),
                self.__build_box(),
                self.__teleport_players(self.height() + 1)
            )
        )
        self.__run_commands(queue)

        yell('Arena prepared, generating layers...')
        queue = self.__generate_layers()
        self.__run_commands(queue)

        yell('Layers generated, randomizing ores...')
        queue = self.__randomize_ores()
        self.__run_commands(queue)

        yell('Ores randomized, randomly generating the exit door...')
        queue = chain.from_iterable(
            self.__create_door()
        )
        self.__run_commands(queue)

        yell('Exit door generated, game is ready!')

    def __build_box(self):
        '''
        Builds box arena.
        '''

        yield [
            partial(
                dispatch_command,
                cuboid(
                    location(self.__x, self.__y, self.__z),
                    width=self.width(),
                    height=self.height() * self.__GROUND_HEIGHT_MULTIPLIER,
                    length=self.length(),
                    type=Material.BEDROCK
                )
            ),
            partial(
                dispatch_command,
                cuboid(
                    location(
                        self.__x,
                        self.__y + self.height() * self.__GROUND_HEIGHT_MULTIPLIER,
                        self.__z
                    ),
                    width=self.width(),
                    height=self.height() * (1 - self.__GROUND_HEIGHT_MULTIPLIER),
                    length=self.length(),
                    type=Material.BARRIER
                )
            ),
            partial(
                dispatch_command,
                cuboid(
                    location(self.__x, self.__y + 1, self.__z),
                    width=self.width() - 2,
                    height=self.height() - 2,
                    length=self.length() - 2,
                    type=Material.AIR
                )
            )
        ]

    def __create_door(self):
        '''
        Creates the exit door in random place.
        '''

        i = randint(0, 3)

        # for i in range(4):
        offset_x = 0 if i in [0, 2] else (1 if i == 1 else -1) * self.width() // 2
        offset_z = 0 if i in [1, 3] else (1 if i == 0 else -1) * self.length() // 2

        if i == 3:
            offset_x += 1
        elif i == 2:
            offset_z += 1

        if i in [0, 2]:
            offset_x += randint(-self.width() // 2 + 4, self.width() // 2 - 4)
        else:
            offset_z += randint(-self.length() // 2 + 4, self.length() // 2 - 4)

        self.__exit_door = location(self.__x - offset_x, self.__y, self.__z - offset_z)

        yield [
            partial(
                dispatch_command,
                cuboid(
                    location(self.__x - offset_x, self.__y, self.__z - offset_z),
                    width=5 if i in [0, 2] else 3,
                    height=5,
                    length=3 if i in [0, 2] else 5,
                    type=Material.BEDROCK
                )
            ),
            partial(
                dispatch_command,
                cuboid(
                    location(self.__x - offset_x, self.__y + 1, self.__z - offset_z),
                    width=3,
                    height=3,
                    length=3,
                    type=Material.OBSIDIAN
                )
            )
        ]

    def __teleport_players(self, offset=0):
        '''
        Teleports the players to the box.
        '''

        for player in self.__players:
            yield [
                partial(
                    yell,
                    'Teleporting {} to the box...'.format(player.getName())
                ),
                partial(
                    teleport,
                    location(self.__x, self.__y + offset, self.__z),
                    whom=player.getName()
                )
            ]

    def __generate_layers(self):
        '''
        Generates layers of the box.
        '''

        ground_height = self.height() * self.__GROUND_HEIGHT_MULTIPLIER

        layers = {
            'deep': {
                'start': 1,
                'end': ground_height // 3,
                'material': Material.DEEPSLATE
            },
            'underground': {
                'start': ground_height // 3,
                'end': ground_height // 6 * 5 - 1,
                'material': Material.STONE
            },
            'dirt': {
                'start': ground_height // 6 * 5 - 1,
                'end': ground_height - 2,
                'material': Material.DIRT
            },
            'grass': {
                'start': ground_height - 1,
                'end': ground_height - 1,
                'material': Material.GRASS_BLOCK
            }
        }

        for layer in layers.values():
            yield partial(
                dispatch_command,
                cuboid(
                    location(self.__x, self.__y + layer['start'], self.__z),
                    width=self.width() - 2,
                    height=layer['end'] - layer['start'] + 1,
                    length=self.length() - 2,
                    type=layer['material']
                )
            )

    def __randomize_ores(self):
        ground_height = self.height() * self.__GROUND_HEIGHT_MULTIPLIER

        ores = {
            'coal': {
                'min': ground_height // 12 * 7,
                'max': ground_height // 6 * 5 - 2,
                'amount': 20 + randint(len(self.__players), len(self.__players) * 8),
                'materials': [ Material.DEEPSLATE_COAL_ORE, Material.COAL_ORE ]
            },
            'iron': {
                'min': ground_height // 3,
                'max': ground_height // 3 * 2,
                'amount': 10 + randint(len(self.__players), len(self.__players) * 4),
                'materials': [ Material.DEEPSLATE_IRON_ORE, Material.IRON_ORE ]
            },
            'gold': {
                'min': ground_height // 4,
                'max': ground_height // 2,
                'amount': 5 + randint(len(self.__players), len(self.__players) * 2),
                'materials': [ Material.DEEPSLATE_GOLD_ORE, Material.GOLD_ORE ]
            },
            'lapis': {
                'min': ground_height // 12 * 5,
                'max': ground_height // 2,
                'amount': 2 + randint(len(self.__players) - 1, len(self.__players)),
                'materials': [ Material.DEEPSLATE_LAPIS_ORE, Material.LAPIS_ORE ]
            },
            'diamond': {
                'min': 1,
                'max': ground_height // 3,
                'amount': 3 + randint(len(self.__players), len(self.__players) * 2),
                'materials': [ Material.DEEPSLATE_DIAMOND_ORE, Material.DIAMOND_ORE ]
            },
        }

        for oredata in ores.values():
            for i in range(oredata['amount']):
                w = self.width() // 2 - 2
                l = self.length() // 2 - 2

                loc = location(
                    self.__x + randint(-w, w),
                    self.__y + randint(oredata['min'], oredata['max']),
                    self.__z + randint(-l, l)
                )

                block = getblock(loc)

                if 'ore' in str(block.getType()).lower():
                    i -= 1
                    continue

                yield partial(
                        setblock,
                        loc,
                        type=oredata['materials'][
                            0 if loc.y <= self.__y + ground_height // 3 else 1
                        ]
                    )

    def __generate_trees(self):
        '''
        Generates trees in the box.
        '''

        pass
