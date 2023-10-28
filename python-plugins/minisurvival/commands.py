# pylint: disable=consider-using-f-string
from time import sleep

from mcapi import bolt, yell, location, asynchronous, lookingat, player
# from random import randint

# pylint: disable=import-error
from org.bukkit import Material
# pylint: enable=import-error

from .functions import setcommandblock, fill

@asynchronous()
def hand_of_zeus(caller, params):
    yell('{} calls for the aid of Zeus!'.format(caller.getName()))

    position = location(caller)

    for i in range(3):
        yell(str(i))
        sleep(1.0)

    bolt(position)
    yell('Zeus, I summon thee!')

@asynchronous()
def prepare_minigame(caller, params):
    if len(params) == 0:
        yell('Usage: /minigame:prepare <player> [player] [player] ...')
        return

    yell('Preparing minigame for {} players'.format(len(params)))

    plr = player(caller.getName())

    position = lookingat(plr)

    dir1 = plr.getEyeLocation().getDirection()

    yell('dir1.x: {}, dir1.y: {}, dir1.z: {}'.format(dir1.x, dir1.y, dir1.z))

    size = [8, 10, 8]
    
    '''
    setcommandblock(
        {
            'auto': 1,
            'Command': '/fill ~-{0} ~-1 ~-{2} ~{0} ~{1} ~{2} minecraft:bedrock'.format(
                round(size[0] / 2),
                size[1] - 3,
                round(size[2] / 2)
            ),
            'name': 'minigame:bedrock_border'
        },
        [ position.x, position.y + 3, position.z ]
    )

    setcommandblock(
        {
            'auto': 1,
            'Command': '/fill ~-{0} ~-1 ~-{2} ~{0} ~{1} ~{2} minecraft:air'.format(
                round(size[0] / 2) - 1,
                size[1] - 3,
                round(size[2] / 2) - 1
            ),
            'name': 'minigame:air_border'
        },
        [ position.x, position.y + 4, position.z ]
    )
    '''
    
    fill(
        [ position.x, position.y, position.z ],
        size,
        type=Material.BEDROCK
    )

    fill(
        [ position.x + 1, position.y + 1, position.z + 1 ],
        [ size[0] - 2, size[1] - 2, size[2] - 2 ],
        type=Material.AIR
    )

# @synchronous()
# def create_box(position):
