"""Utility functions for the minisurvival plugin.
"""

# pylint: disable=consider-using-f-string

# pylint: disable=import-error
from mcapi import WORLD, SERVER, parseargswithpos, synchronous  # type: ignore
from org.bukkit import Bukkit, Material, Location  # type: ignore
from org.bukkit.block import CommandBlock  # type: ignore

# pylint: enable=import-error


@synchronous()
def setcommandblock(meta, *args, **kwargs):
    # type: (dict[str, str], *Location, **str) -> None

    """
    Sets a command block at the specified coordinates.

    You can use the create_meta function to create the meta dictionary.
    """

    startup = None

    r = parseargswithpos(
        args, kwargs, ledger={"type": ["type", 0, Material.COMMAND_BLOCK]}
    )

    if "auto" in meta:
        r["type"] = Material.REPEATING_COMMAND_BLOCK

    block = WORLD.getBlockAt(r["x"], r["y"], r["z"])

    block.setType(r["type"])

    if "auto" in meta:
        startup = block.getWorld().getBlockAt(r["x"], r["y"] - 1, r["z"])
        startup.setType(Material.REDSTONE_BLOCK)

    command_block = CommandBlock.cast(block.getState())

    command_block.setCommand(meta["Command"])
    command_block.setName(meta["name"])
    command_block.update(True)

    if "auto" in meta and startup is not None:
        startup.setType(Material.AIR)
        command_block.update(True)


def create_meta(width=4, height=4, length=4, material_type=Material.COBBLESTONE):
    # type: (int, int, int, Material) -> dict[str, str]

    """
    Creates a meta dictionary for a command block.
    """
    return {
        "auto": "1",
        "Command": "/fill ~-{0} ~-1 ~-{2} ~{0} ~{1} ~{2} minecraft:{3}".format(
            round(width / 2), height - 3, round(length / 2), str(material_type).lower()
        ),
        "name": "fill",
    }


@synchronous()
def dispatch_command(command):
    # type: (str) -> None

    """
    Synchronously dispatches a command.

    You can use this function to dispatch eg. the output of the `cuboid` function.
    """

    SERVER.dispatchCommand(Bukkit.getConsoleSender(), command)


def cuboid(*args, **kwargs):
    """
    Prepares a /fill command to create a cuboid.
    """

    r = parseargswithpos(
        args,
        kwargs,
        ledger={
            "type": ["type", 0, Material.COBBLESTONE],
            "length": ["length", 1, 4],
            "width": ["width", 1, 4],
            "height": ["height", 1, 4],
        },
    )

    width, height, length = r["width"], r["height"], r["length"]
    x, y, z = r["x"], r["y"], r["z"]

    cmd = "fill {1} {2} {3} {4} {5} {6} minecraft:{0}".format(
        str(r["type"]).lower(),
        int(round(x - width / 2)),
        int(round(y)),
        int(round(z - length / 2)),
        int(round(x + width / 2)),
        int(round(y + height - 1)),
        int(round(z + length / 2)),
    )

    return cmd
