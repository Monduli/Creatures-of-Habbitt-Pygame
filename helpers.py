import pygame
from classes import *
import random

def retrieve_background(choice):
    folder = "images/"
    if choice == "cave":
        background = pygame.image.load(folder + "cave.png")
        background = pygame.transform.scale(background,(1600,900))
        return background
    elif choice == "forest":
        background = pygame.image.load(folder + "forest.png")
        background = pygame.transform.scale(background,(1600,900))
        return background
    elif choice == "village":
        background = pygame.image.load(folder + "village.jpg")
        background = pygame.transform.scale(background,(1600,900))
        return background
    
def retrieve_character(choice):
    folder = "images/"
    if choice == "N. Steen":
        character = pygame.image.load(folder + "bear.png")
        #character = pygame.transform.scale(character,(1600,900))
        return character

def drawText(surface, text, color, rect, font, aa=False, bkg=None, center=False, input=False):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 0
    image = None

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        text_rect = image.get_rect()
        
        if center == True:
            text_rect.center = rect.center
            surface.blit(image, (text_rect.left, y+10))
        else:
            surface.blit(image, (rect.left+20, y+10))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    if input == True:
        return image
    return text

def get_dungeon(dungeon):
    if dungeon == "cave":
        return [
            Enemy("Gobble", 10, 5, 5, 5, 5),
            Enemy("Goobble", 10, 5, 5, 5, 5),
            Enemy("Gabble", 10, 5, 5, 5, 5)
        ]

def turn_order(group):
    turns = []
    for character in group:
        roll = random.randint(0, character.get_dex())
        turns.append((character, roll, "p"))
    turns = sorted(turns, key=lambda turn:turn[1], reverse=True)
    return turns

def find_and_remove_from_turn(turns, character):
    for nest in turns:
        if nest[0] == character:
            turns.remove(nest)
            return
        
def add_party_member(name):
    if name == "nsteen":
        nsteen = Paladin([15, 10, 10, 10, 10, 10])
        nsteen.set_name("N. Steen")
        #rabby = Bookish([10,10,10,15,10,10])
        #rabby.set_name("Radish")
        return nsteen
    if name == "radish":
        radish = Bookish([15, 10, 10, 10, 10, 10])
        radish.set_name("Radish")
        return radish
    if name == "toffee":
        toffee = Martial([20, 20, 20, 20, 20, 20])
        toffee.set_name("Toffee")
        return toffee
    if name == "grapefart":
        grapefart = Ranger([20, 20, 20, 20, 20, 20])
        grapefart.set_name("Grapefart")
        return grapefart
    
def fill_party():
    nsteen = Paladin([15, 10, 10, 10, 10, 10])
    nsteen.set_name("N. Steen")
    #rabby = Bookish([10,10,10,15,10,10])
    #rabby.set_name("Radish")
    radish = Bookish([15, 10, 10, 10, 10, 10])
    radish.set_name("Radish")
    toffee = Martial([20, 20, 20, 20, 20, 20])
    toffee.set_name("Toffee")
    grapefart = Ranger([20, 20, 20, 20, 20, 20])
    grapefart.set_name("Grapefart")
    party = [nsteen, radish, toffee, grapefart]
    for char in party:
        char.print_stats()
    return party

def drawStyleRect(surface, x, y):
    for i in range(4):
        pygame.draw.rect(surface, (255,255,255), (x-i,y-i,500,100), 1)