#############
# FORMAT:
# [0] - Dialog in order
# [1] - Target of left choice button at intersection
# [2] - Target of right choice button at intersection
#############
name = "Default"

def determine_dialog(target, progress, name="Default"):
    match target:
        case "dialog_start_2":
            dialog_start_2[0][0][1] = "Your name is "+ name +"."
            dialog_start_2[0][1][1] = "Hello, "+name+"!"
            return dialog_start_2
        case "cave_exit":
            return outside_cave_1
        case "martial_choice":
            outside_cave_2[0][0][1] = "You have chosen a Martial background."
            outside_cave_2[0][1][1] = "Let me guess. You only have one brain cell, and it only fires sometimes. But that's okay, I guess."
            return outside_cave_2
        case "bookish_choice":
            outside_cave_2[0][0][1] = "You have chosen a Bookish background."
            outside_cave_2[0][1][1] = "What are you, some kind of nerd? Do books keep you company at night? Make those lonely nights warm or what?"
            return outside_cave_2
        case "inn":
            if progress < 2:
                return inn_dialog_1
            else:
                return outside_cave_1

dialog_start = [[
    [None, """You find yourself in a dark cave."""],
    [None, """You try to remember your name."""],
    [None, "Please type into the box."],
], "dialog_start_2"]

dialog_start_2 = [[
    [None, "Your name is name."],
    [None, "Hello name!"],
    [None, "Let's get you out of this cave."],
    [None, "Please select an option."],
    [None, "Exit Cave"],
    [None, "Don't Exit Cave"]
], "cave_exit", "cave_exit"]

outside_cave_1 = [[
    [None, "Regardless of your choice, I'm taking you outside."],
    [None, "That's better. Smell that forest air!"],
    [None, "The fresh air is good for you, after all."],
    [None, "Did you really think breathing cave air for all this time was good for you?"],
    [None, "If you thought that, you would be completely wrong."],
    [None, "You feel the urge to think really hard about what kind of person you built yourself into."],
    [None, "Please select an option."],
    [None, "Martial (Physical, Melee)"],
    [None, "Bookish (Magic, Ranged)"]
], "martial_choice", "bookish_choice"]

outside_cave_2 = [[
    [None, "You have chosen Class."],
    [None, "Judgmental line!"],
    [None, "Anyway, we should find our way out of here."],
    [None, "Maybe you should just follow that road over there until you run into something."],
    [None, "Ah, here we are. Some kind of city."],
    [None, "I'll leave you to figuring out where you should be going."],
    [None, "Please select a destination."]
], "town_choices"]

inn_dialog_1 = [[
    [None, "You walk into an inn."],
    [None, "There is a very confused looking bear looking around."],
    ["N. Steen", "Well, look who we have here!"],
    ["N. Steen", "If it isn't our disgraced ruler themself."],
    ["N. Steen", "Well, I won't let you walk about on your own. I'm coming with you."],
    [None, "[Bear N. Steen has joined your party.]"],
    [None, "[Returning to town.]"]
]]

nsteen_neutral = [[
    ["N. Steen", "Hey, how's it going?"],
    ["inn"]
]]