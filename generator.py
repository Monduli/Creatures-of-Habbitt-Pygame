from classes import *
import random
import time

def sleep():
    time.sleep(1)

def manual_entry(attribute):
    while True:
        print("Please type in the character's " + attribute + " value.")
        a = t_input()
        try:
            a = int(a)
        except ValueError:
            print("That is not a typed number (although it may be a spelled number). Try again.")
        if a > 20 or a < 0:
            print("Attribute values cannot be less than 0 or greater than 20 during character creation.")
            sleep()
            print("Attribute numbers should be between 9 and 18 with T'Lass Standard Rules.")
            sleep()
        else:
            return a

def t_input():
    get = input()
    if get in ["quit", "Quit", "q", "Q"]:
        quit()
    return get

def roll_values(x, y):
    s = random.randint(x, y)
    d = random.randint(x, y)
    co = random.randint(x, y)
    i = random.randint(x, y)
    w = random.randint(x, y)
    ch = random.randint(x, y)
    li = [s, d, co, i, w, ch]
    return li

def assign_stats(character, li):
    character.set_str(li[0])
    character.set_dex(li[1])
    character.set_con(li[2])
    character.set_int(li[3])
    character.set_wis(li[4])
    character.set_cha(li[5])

def select_class_generate_character(name):
    class_select = None
    valid_choices = ["Fighter", "fighter", "F", "f", "Paladin", "paladin", "P", "p"]
    fighters = ["Fighter", "fighter", "F", "f"]
    paladins = ["Paladin", "paladin", "P", "p"]
    wizards = ["Wizard", "wizard", "W", "w"]
    rangers = ["Ranger", "ranger", "R", "r"]
    while class_select not in valid_choices:
        print("Please select a class for " + name + ". (Choices: Fighter, Paladin)")
        class_select = t_input()
        if class_select not in valid_choices:
            print("You have made an invalid selection.")
            sleep()
    print("You have chosen " + class_select + ".")
    sleep()
    if class_select in fighters:
        character = Fighter()
    elif class_select in paladins:
        character = Paladin()
    elif class_select in wizards:
        character = Wizard()
    elif class_select in rangers:
        character = Ranger()
    return character

def roll_stats(character, y_answers, n_answers):
    choice = None
    while choice not in y_answers and choice not in n_answers:
        print("Would you like me to roll stats for you? (Yes or No)")
        choice = t_input()
        if choice not in y_answers and choice not in n_answers:
            print("Please answer 'yes' or 'no'.")
            sleep()

    if choice in y_answers:
        loop = 0
        while loop ==  0:
            print("Choose a reroll setting:\n(Note: In the parentheses is the potential stat range.)\n1) Reroll 1s (6-19)\n2) Reroll 1s and 2s (9-18) (T'Lass Standard)\n3) Reroll nothing (3-18)")
            reroll = t_input()
            valid_reroll = ["1", "2", "3"]
            if reroll not in valid_reroll:
                print("That is not a valid input. Please try again.")
            else:
                loop = 1
        ahead = False
        while ahead == False:
            print("Rolling numbers...")
            sleep()
            if reroll == "2":
                li = roll_values(9, 18)
                s, d, co, i, w, ch = li[0], li[1], li[2], li[3], li[4], li[5]
            elif reroll == "1":
                li = roll_values(6, 18)
                s, d, co, i, w, ch = li[0], li[1], li[2], li[3], li[4], li[5]
            else:
                li = roll_values(3, 18)
                s, d, co, i, w, ch = li[0], li[1], li[2], li[3], li[4], li[5]
            print("Here's your stats I rolled: \nSTR: " + str(s) + "\nDEX: " + str(d) + "\nCON: " + str(co) + "\nINT: " + str(i) + "\nWIS: " + str(w) + "\nCHA: " + str(ch))
            sleep()
            tree = None
            while tree == None:
                print("Are you happy with these stats?")
                choice = t_input()
                if choice in y_answers:
                    print("Great! Moving on.")
                    sleep()
                    ahead = True
                    tree = True
                elif choice in n_answers:
                    print("Alright, I will reroll them for you.")
                    sleep()
                    tree = True
                else:
                    print("Sorry, that's not a valid response. Try again.")
                    sleep()
    else:
        print("Alright. You will have to enter your numbers manually then.")
        sleep()
        ahead = 0
        while ahead == 0:
            s = manual_entry("Strength")
            d = manual_entry("Dexterity")
            co = manual_entry("Constitution")
            i = manual_entry("Intelligence")
            w = manual_entry("Wisdom")
            ch = manual_entry("Charisma")
            print("You entered:\nSTR: " + str(s) + "\nDEX: " + str(d) + "\nCON: " + str(co) + "\nINT: " + str(i) + "\nWIS: " + str(w) + "\nCHA: " + str(ch))
            sleep()
            loop = 0
            while loop == 0:
                print("Are you happy with these numbers?")
                answer = t_input()
                if answer in y_answers:
                    print("Cool. Moving on...")
                    sleep()
                    li = [s, d, co, i, w, ch]
                    loop = 1
                    ahead = 1
                elif answer in n_answers:
                    print("Alright, let's try again.")
                    sleep()
                    loop = 1
                else:
                    print("That's not a valid answer.")
                    sleep()
    
    assign_stats(character, li)

def choose_background(character, y, n):
    backgrounds = ["Acolyte", "acolyte", "Soldier", "soldier", "more", "More"]
    print("We will now select your character's background.")
    print("Your choices at present are as follows:")
    print("Acolyte")
    print("Soldier")
    sleep()
    ahead = 0
    while ahead == 0:
        print("Please select a background.")
        background = t_input()
        if background not in backgrounds:
            print("I'm afraid you've made an error in your selection.")
            sleep()
            if background == "s" or background == "S":
                print("Did you mean soldier? Please type 'soldier' or 'Soldier'.")
                sleep()
            elif background == "a" or background == "A":
                print("Did you mean acolyte? Please type 'acolyte' or 'Acolyte'.")
                sleep()
        if background == "soldier" or background == "Soldier":
            print("Great. You have chosen the soldier background.")
            sleep()
            character.set_background("Soldier")
            return character
        elif background == "acolyte" or background == "Acolyte":
            print("Great. You have chosen the acolyte background.")
            sleep()
            character.set_background("Acolyte")
            return character
        elif background == "more" or background == "More":
            print("More backgrounds will be available later on.")
            sleep()
    

def generation():
    y_answers = ["Yes", "yes", "y", "Y"]
    n_answers = ["No", "no", "n", "N"]

    print("Welcome to my character generator.")
    sleep()
    print("Please enter your character's name.")
    name = t_input()
    print("Your character's name is " + name + ". Welcome to the world, " + name + "!")
    sleep()

    character = select_class_generate_character(name)
    
    roll_stats(character, y_answers, n_answers)
    choose_background(character, y_answers, n_answers)

    print("End test.")
    end = input()

if __name__ == "__main__":
    generation()

