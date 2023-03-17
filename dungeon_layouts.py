# dungeon format:
# first is the room to be loaded
# second number is the room to go to from the left exit
# third number is the room to go to from the top exit
# fourth number is the room to go to from the right exit

from helpers import *

def get_dungeon_layout(dungeon_name):
    if dungeon_name == "cave":
        return [cave, cave_enemies]

cave = [
            ["testroom.png", 1, 2, 1, None], 
            ["testroom2.png", 0, None, 0, None],
            ["testroom3.png", None, None, None, 0], 
            ["testroom.png", 4, 5, 6, None],
            ["testroom.png", 0, 2, 3, None], 
            ["testroom.png", 4, 5, 6, None]
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
    [Enemy("Ultra-Gob", 500, 5, 5, 5, 5, 100),],
    "Goblin_Stand"
    ]
]