# pylint: disable=consider-using-f-string
# pylint: disable=unspecified-encoding
import os
import json

# pylint: disable=import-error
from mcapi import asynchronous, yell  # type: ignore

from org.bukkit.event.world import ChunkLoadEvent  # type: ignore

# pylint: enable=import-error

from minisurvival import CONFIG
from minisurvival.utils.functions import get_blocks_in_chunk, max_height_of_chunk


@asynchronous()
def on_chunkload(e):
    # type: (ChunkLoadEvent) -> None

    """
    This event is used to fetch blocks from currently loaded chunks.

    It is not used in the minisurvival minigame.
    """

    chunk = e.getChunk()
    world = e.getWorld()
    snapshot_chunk = chunk.getChunkSnapshot()
    worldname = snapshot_chunk.getWorldName()

    if not os.path.exists(CONFIG.CHUNKDATA_DIR):
        raise FileNotFoundError("Chunkdata directory not found")

    if worldname not in CONFIG.MAPGEN_WORLDS:
        return

    min_y = world.getMinHeight()
    chunk_x, chunk_z = snapshot_chunk.getX(), snapshot_chunk.getZ()

    print("Minigame Mapgen: Chunk x: {} z: {} loaded".format(chunk_x, chunk_z))

    max_y = max_height_of_chunk(snapshot_chunk)
    chunk_blocks = get_blocks_in_chunk(snapshot_chunk, min_y)

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
