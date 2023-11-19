# pylint: disable=consider-using-f-string

# pylint: disable=import-error
from mcapi import yell, asynchronous, lookingat, player  # type: ignore
from org.bukkit.entity import Entity  # type: ignore

# pylint: enable=import-error

from minisurvival.models import MinisurvivalBox


@asynchronous()
def prepare_minigame(caller, params):
    # type: (Entity, list[str]) -> None
    # players = filter(lambda p: p is not None, (player(p) for p in set(params)))
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
