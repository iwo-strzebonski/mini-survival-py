from time import sleep

from mcapi import parseargswithpos, setblock, yell, WORLD, synchronous
# from random import randint

# pylint: disable=import-error
from org.bukkit import Material
from org.bukkit.block import CommandBlock
# pylint: enable=import-error

def cuboid(*args, **kwargs):
    r = parseargswithpos(args, kwargs, ledger={
        'type':['type', 0, Material.COBBLESTONE],
        'length':['length', 1, 4],
        'width':['width', 1, 4],
        'height':['height', 1, 4],
    })

    length = r['length']
    width = r['width']
    height = r['height']

    for x in range(length):
        for y in range(height):
            for z in range(width):
                setblock(x + r['x'], y + r['y'], z + r['z'], r['type'])

def box(*args, **kwargs):
    r = parseargswithpos(args, kwargs, ledger={
        'type':['type', 0, Material.COBBLESTONE],
        'length':['length', 1, 4],
        'height':['height', 1, 4],
        'width':['width', 1, 4],
    })

    length = r['length']
    height = r['height']
    width = r['width']


    for x in range(length):
        for y in range(height):
            for z in range(width):
                if x in [0, length - 1] or y in [0, height - 1] or z in [0, width - 1]:
                    setblock(x + r['x'], y + r['y'], z + r['z'], r['type'])

@synchronous()
def setcommandblock(meta, *args, **kwargs):
    r = parseargswithpos(args, kwargs, ledger={
        'type':['type', 0, Material.COMMAND_BLOCK]
    })

    if 'auto' in meta:
        r['type'] = Material.REPEATING_COMMAND_BLOCK

    block = WORLD.getBlockAt(r['x'], r['y'], r['z'])

    block.setType(r['type'])

    if 'auto' in meta:
        startup = block.getWorld().getBlockAt(r['x'], r['y'] - 1, r['z'])
        startup.setType(Material.REDSTONE_BLOCK)

    command_block = CommandBlock.cast(block.getState())

    command_block.setCommand(meta['Command'])
    command_block.setName(meta['name'])
    command_block.update(True)

    if 'auto' in meta:
        startup.setType(Material.AIR)
        command_block.update(True)

def fill(*args, **kwargs):
    r = parseargswithpos(args, kwargs, ledger={
        'type':['type', 0, Material.COBBLESTONE],
        'length':['length', 1, 4],
        'width':['width', 1, 4],
        'height':['height', 1, 4],
    })

    width, height, length = r['width'], r['height'], r['length']

    setcommandblock(
        {
            'auto': 1,
            'Command': '/fill ~-{0} ~-1 ~-{2} ~{0} ~{1} ~{2} minecraft:{3}'.format(
                round(width / 2),
                height - 3,
                round(length / 2),
                str(r['type']).lower()
            ),
            'name': 'fill'
        },
        [ r['x'], r['y'] + 3, r['z'] ]
    )
