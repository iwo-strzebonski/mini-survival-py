# pylint: disable=consider-using-f-string

# pylint: disable=import-error
from mcapi import yell, asynchronous, lookingat, player
# pylint: enable=import-error

from minisurvival.models import MinisurvivalBox

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

    box = MinisurvivalBox(*position, *size, params)
