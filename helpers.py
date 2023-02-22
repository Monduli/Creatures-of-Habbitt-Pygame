import pygame
from classes import *
import random
import varname
import math

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
        return [[
            Enemy("Gobble", 1000, 5, 5, 5, 5, 100),
            Enemy("Goobble", 10, 5, 5, 5, 5, 100),
            Enemy("Gabble", 10, 5, 5, 5, 5, 100)
        ], 300]


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
            return turns


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

def drawStyleCircle(surface, x, y, width):
    for i in range(4):
        pygame.draw.circle(surface, (255,0,0), (x-i,y-i), width/2, width)

def get_portrait(character):
    if character == "N. Steen":
        portrait = pygame.image.load("images/bear_portrait.png")
        portrait = pygame.transform.scale(portrait,(100,100))
        return portrait
    if character == "Radish":
        portrait = pygame.image.load("images/rabbit_portrait.png")
        portrait = pygame.transform.scale(portrait,(100,100))
        return portrait
    if character == "Toffee":
        portrait = pygame.image.load("images/toffee_portrait.png")
        portrait = pygame.transform.scale(portrait,(100,100))
        return portrait
    if character == "Grapefart":
        portrait = pygame.image.load("images/grapefart_portrait.png")
        portrait = pygame.transform.scale(portrait,(100,100))
        return portrait
    if character in ["Gobble"]:
        portrait = pygame.image.load("images/goblin.png")
        portrait = pygame.transform.scale(portrait,(100,100))
        return portrait
    if character in ["Goobble"]:
        portrait = pygame.image.load("images/goobble.png")
        portrait = pygame.transform.scale(portrait,(100,100))
        return portrait
    if character in ["Gabble"]:
        portrait = pygame.image.load("images/gabble.png")
        portrait = pygame.transform.scale(portrait,(100,100))
        return portrait
    
def debug_print(name, variable):
    print(name + ": " + str(variable))

def get_possible_matches(cell_i):
    y = cell_i % 10 
    x = math.floor(cell_i / 10) * 10
    poss = []
    for z in range(x, x+10):
        poss.append(z)
    for z in range(y, y+90, 10):
        poss.append(z)
    return poss

def find_i(spread, pos):
    x = pos[0]
    y = pos[1]
    for j in range(len(spread)-1):
        for k in range(len(spread)-1):
            check_x, check_y = spread[j], spread[k]
            check_x_high, check_y_high = spread[j+1], spread[k+1]
            if check_x <= x < check_x_high:
                if check_y <= y < check_y_high:
                    ret = j + (k*10)
                    return ret
    raise Exception(str(pos) + " is not a valid location on the board.")

def print_rects(board):
    for x in range(0, len(board.board)):
        print(board.board[x].rect)

def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha()

