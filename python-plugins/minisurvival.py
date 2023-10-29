'''
This is a plugin for the Minecraft server CraftBukkit.
It is written in Python and uses the mcapi module.
'''

# pylint: disable=consider-using-f-string

# pylint: disable=import-error
from mcapi import add_command, yell, asynchronous, lookingat
# pylint: enable=import-error

from minisurvival.utils.commands import prepare_minigame

add_command('minigame:prepare', prepare_minigame)

@asynchronous()
def get_direction(caller, _params):
    '''
    This command is used to test the getEyeLocation and getDirection
    methods of the Player class.
    
    It is not used in the minisurvival minigame.
    '''

    dir1 = caller.getEyeLocation().getDirection()
    yell('dir1.x: {}, dir1.y: {}, dir1.z: {}'.format(dir1.x, dir1.y, dir1.z))

    block = lookingat(caller)
    biome = block.getBiome()

    yell('biome: {}'.format(biome))

add_command('minigame:direction', get_direction)
