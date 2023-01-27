from classes import *
import random
import time

def sleep():
    time.sleep(1)

def manual_entry(attribute):
    while True:
        print("Please type in the character's " + attribute + " value.")
        a = input()
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
    character.set_dex(li[0])
    character.set_con(li[0])
    character.set_int(li[0])
    character.set_wis(li[0])
    character.set_cha(li[0])

def generation():
    print("Welcome to my character generator.")
    sleep()

    print("Please enter your character's name.")
    name = input()
    print("Your character's name is " + name + ". Welcome to the world, " + name + "!")
    sleep()

    class_select = None
    valid_choices = ["Fighter", "fighter", "F", "f", "Paladin", "paladin", "P", "p"]
    fighters = ["Fighter", "fighter", "F", "f"]
    paladins = ["Paladin", "paladin", "P", "p"]
    while class_select not in valid_choices:
        print("Please select a class for " + name + ". (Choices: Fighter, Paladin)")
        class_select = input()
        if class_select not in valid_choices:
            print("You have made an invalid selection.")
            sleep()
    print("You have chosen " + class_select + ".")
    sleep()
    if class_select in fighters:
        character = Fighter()
    elif class_select in paladins:
        character = Paladin()

    choice = None
    y_answers = ["Yes", "yes", "y", "Y"]
    n_answers = ["No", "no", "n", "N"]

    while choice not in y_answers and choice not in n_answers:
        print("Would you like me to roll stats for you? (Yes or No)")
        choice = input()
        if choice not in y_answers and choice not in n_answers:
            print("Please answer 'yes' or 'no'.")
            sleep()

    if choice in y_answers:
        loop = 0
        while loop ==  0:
            print("Choose a reroll setting:\n(Note: In the parentheses is the potential stat range.)\n1) Reroll 1s (6-19)\n2) Reroll 1s and 2s (9-18) (T'Lass Standard)\n3) Reroll nothing (3-18)")
            reroll = input()
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
                choice = input()
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
                answer = input()
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
    print("End test.")
    end = input()

if __name__ == "__main__":
    generation()

