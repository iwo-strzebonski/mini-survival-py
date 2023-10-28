from mcapi import add_command, yell
from minisurvival.commands import prepare_minigame

# pylint: disable=import-error
from org.bukkit import Material
# pylint: enable=import-error

add_command('minigame:prepare', prepare_minigame)
