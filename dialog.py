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
            dialog_start_2[0][0] = "Your name is "+ name +"."
            dialog_start_2[0][1] = "Hello, "+name+"!"
            return dialog_start_2
        case "cave_exit":
            return outside_cave_1
        case "martial_choice":
            outside_cave_2[0][0] = "You have chosen a Martial background."
            outside_cave_2[0][1] = "Let me guess. You only have one brain cell, and it only fires sometimes. But that's okay, I guess."
            return outside_cave_2
        case "bookish_choice":
            outside_cave_2[0][0] = "You have chosen a Bookish background."
            outside_cave_2[0][1] = "What are you, some kind of nerd? Do books keep you company at night? Make those lonely nights warm or what?"
            return outside_cave_2
        case "inn":
            if progress < 2:
                return inn_dialog_1
            else:
                return outside_cave_1

dialog_start = [[
    """Dan's game version 0.0""",
    """You find yourself in a dark cave.""",
    """You try to remember your name.""",
    "Please type into the box.",
], "dialog_start_2"]

dialog_start_2 = [[
    "Your name is name.",
    "Hello name!",
    "Let's get you out of this cave.",
    "Please select an option.",
    "Exit Cave",
    "Don't Exit Cave"
], "cave_exit", "cave_exit"]

outside_cave_1 = [[
    "Regardless of your choice, I'm taking you outside.",
    "That's better. Smell that forest air!",
    "The fresh air is good for you, after all.",
    "Did you really think breathing cave air for all this time was good for you?",
    "If you thought that, you would be completely wrong.",
    "You feel the urge to think really hard about what kind of person you built yourself into.",
    "Please select an option.",
    "Martial (Physical, Melee)",
    "Bookish (Magic, Ranged)"
], "martial_choice", "bookish_choice"]

outside_cave_2 = [[
    "You have chosen Class.",
    "Judgmental line!",
    "Anyway, we should find our way out of here.",
    "Maybe you should just follow that road over there until you run into something.",
    "Ah, here we are. Some kind of city.",
    "I'll leave you to figuring out where you should be going.",
    "Please select a destination."
], "town_choices"]

inn_dialog_1 = [[
    "You walk into an inn.",
    "There is only woman standing at the bar, and the rest of the inn is deserted.",
    "Well, look who we have here!",
    "[Returning to town.]"
]]