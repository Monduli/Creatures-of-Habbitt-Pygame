# dungeon format:
# first is the room to be loaded
# second number is the room to go to from the left exit
# third number is the room to go to from the top exit
# fourth number is the room to go to from the right exit

def get_dungeon_layout(dungeon_name):
    if dungeon_name == "cave":
        return cave

cave = [
            ["testroom.png", 1, 2, 3], 
            ["testroom.png", 4, 5, 6],
            ["testroom.png", 0, 2, 3], 
            ["testroom.png", 4, 5, 6],
            ["testroom.png", 0, 2, 3], 
            ["testroom.png", 4, 5, 6]
            ]