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
    [Enemy("Bazongle", 20000, 100, 100, 100, 100, 100),],
    "Bazongle_Stand"
    ],[
    [None], None
    ]
]

if __name__ == "__main__":
    print("This is a database file. Do not run this directly.")