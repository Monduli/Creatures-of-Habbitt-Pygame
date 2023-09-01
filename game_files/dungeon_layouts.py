#####
# Creatures of Habbitt - Dungeons Layout File
# Author: Dan
# Holds the layouts of the dungeons in crawler mode.
#####
# dungeon format:
# first is the room to be loaded
# second number is the room to go to from the left exit
# third number is the room to go to from the top exit
# fourth number is the room to go to from the right exit
#####

from helpers import *

def get_dungeon(dungeon_name):
    """
    The function "get_dungeon_layout" returns the layout and enemies of a specified dungeon.
    
    :param dungeon_name: The parameter `dungeon_name` is a string that represents the name of the
    dungeon
    :return: a list containing the layout of the specified dungeon and the enemies present in that
    dungeon.
    """
    if dungeon_name == "cave":
        return [cave, cave_enemies]
    if dungeon_name == "cavetiled":
        return [cave_tiled, cave_enemies]

cave = [
            ["testroom.png", 1, 2, 1, None], 
            ["testroom2.png", 0, 3, 0, None],
            ["testroom3.png", None, None, None, 0], 
            ["testroom4.png", None, "END", None, 1]
            ]

cave_enemies = [
    [
    [None], None
    ],[
    [Enemy("Gobble", 10, 5, 5, 5, 5, 100),
    Enemy("Goobble", 10, 5, 5, 5, 5, 100),
    Enemy("Gabble", 10, 5, 5, 5, 5, 100)],
    #enemy portrait for dungeon
    "Goblin_Stand"
    ],[
    [Enemy("Bazongle", 20000, 10000, 100, 100, 100, 100),],
    "Bazongle_Stand"
    ],[
    [None], None
    ]
]

cave_tiled = [
    "cave1.tmx",
    [
        "cave1.tmx", 
        [900, 839, "exit"],
        [0, 0, "cave2.tmx"]
    ]
]


if __name__ == "__main__":
    print("This is a database file. Do not run this directly.")