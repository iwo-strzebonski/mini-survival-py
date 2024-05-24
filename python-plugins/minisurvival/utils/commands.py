# pylint: disable=consider-using-f-string
# pylint: disable=unspecified-encoding

import json
import os
import shutil
from time import time

# pylint: disable=import-error
from mcapi import yell, asynchronous, lookingat, player, location, WORLD  # type: ignore
from org.bukkit.entity import Entity  # type: ignore

# pylint: enable=import-error

from minisurvival import CONFIG
from minisurvival.utils.requests import request
from minisurvival.utils.functions import (
    get_blocks_in_chunk,
    max_height_of_chunk,
    get_world_with_params,
)
from minisurvival.models import MinisurvivalBox


@asynchronous()
def prepare_minigame(caller, params):
    # type: (Entity, list[str]) -> None

    """
    This command is used to prepare the minigame for the players.
    """

    players = [
        p for p in (player(p) for p in set(params)) if p is not None and p.isOnline()
    ]

    if len(players) == 0:
        yell("Usage: /minigame:prepare <player> [player] [player] ...")
        yell("Also check if usernames are correct.")
        return

    yell("Preparing minigame for {} players".format(len(params)))

    position = lookingat(caller)

    box = MinisurvivalBox(position, players)

    box.prepare()


@asynchronous()
def read_chunks(caller, params):
    # type: (Entity, list[str]) -> None
    """
    This command is used to get the chunk at the player's location.

    It is not used in the minisurvival minigame.
    """

    if len(params) != 1:
        yell("Usage: /minigame:read_chunk <radius>")
        return

    radius = 0

    try:
        radius = int(params[0])
    except ValueError:
        yell("Usage: /minigame:read_chunk <radius>")
        return

    world = caller.getWorld()
    min_y = world.getMinHeight()
    loc = location(caller)
    pos_x, pos_z = loc.getBlockX(), loc.getBlockZ()
    worldname = world.getName()

    for x in range(-radius, radius + 1):
        for z in range(-radius, radius + 1):
            chunk = world.getChunkAt(int(pos_x / 16) + x, int(pos_z / 16) + z, True)

            snapshot_chunk = chunk.getChunkSnapshot()
            chunk_x, chunk_z = chunk.getX(), chunk.getZ()
            max_y = max_height_of_chunk(snapshot_chunk)

            chunk_blocks = get_blocks_in_chunk(snapshot_chunk, min_y)

            yell("Chunk x: {} z: {} loaded".format(chunk_x, chunk_z))

            with open(
                os.path.join(
                    CONFIG.CHUNKDATA_DIR,
                    "{}_chunk_{}_{}.json".format(worldname, chunk_x, chunk_z),
                ),
                "w",
            ) as f:
                f.write(
                    json.dumps(
                        {
                            "worldname": worldname,
                            "chunk_x": chunk_x,
                            "chunk_z": chunk_z,
                            "min_y": min_y,
                            "max_y": max_y,
                            "chunk_blocks": chunk_blocks,
                        }
                    )
                )

    zip_path = os.path.join(
        CONFIG.CHUNKDATA_DIR, "{}-{}.zip".format(worldname, str(time()))
    )

    shutil.make_archive(
        zip_path.replace(".zip", ""),
        "zip",
        CONFIG.CHUNKDATA_DIR,
    )

    with open(zip_path, "rb") as zip_file:
        print("Uploading zip file...")

        data = zip_file.read()

        print("Zip file size: {}".format(len(data)))

        request(
            "http://localhost:5000/upload-chunks",
            method="POST",
            headers={
                "Content-Disposition": 'attachment; filename="{}"'.format(
                    os.path.basename(zip_path)
                ),
                "Content-Type": "application/zip",
            },
            data=data,
        )

    print("Uploaded zip file. Cleaaning up...")
    shutil.rmtree(CONFIG.CHUNKDATA_DIR)
    os.mkdir(CONFIG.CHUNKDATA_DIR)


@asynchronous()
def start_chunkgen(caller, params):
    world = None

    try:
        world = get_world_with_params(caller, params)
    except ValueError as e:
        yell(str(e))
        yell("Usage: /minigame:start_chunkgen [world]")
        return

    worldname = world.getName()

    if worldname in CONFIG.MAPGEN_WORLDS:
        yell("Chunk generation is already for this world!")
        return

    yell("Starting chunk generation for {} world".format(worldname))

    CONFIG.MAPGEN_WORLDS.append(worldname)


@asynchronous()
def stop_chunkgen(caller, params):
    world = None

    if len(params) > 1:
        yell("Usage: /minigame:start_chunkgen [world]")
        return

    if len(params) == 1:
        world = caller.getServer().getWorld(params[0])

        if world is None:
            yell("World {} not found".format(params[0]))
            return
    else:
        try:
            world = caller.getWorld()
        except AttributeError:
            world = WORLD

    worldname = world.getName()

    if worldname not in CONFIG.MAPGEN_WORLDS:
        yell("Chunk generation is not running for this world!")
        return

    yell("Stopping chunk generation for {} world".format(world.getName()))

    CONFIG.MAPGEN_WORLDS.remove(worldname)
