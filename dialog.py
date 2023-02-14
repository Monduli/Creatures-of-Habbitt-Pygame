#############
# FORMAT:
# [0] - Dialog in order
# [1] - Target of left choice button at intersection
# [2] - Target of right choice button at intersection
#############
name = "Default"

def determine_dialog(target, name="Default"):
    match target:
        case "dialog_start_2":
            dialog_start_2[0][0] = "Your name is "+ name +"."
            dialog_start_2[0][1] = "Hello, "+name+"!"
            return dialog_start_2

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
    "Stick Around"
], "cave_exit", "meander"]

dialog_right = [[
    "You chose to go right.",
    "There is nothing here."
]]