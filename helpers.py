import pygame
from classes import *
import random
import varname
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

width = 1600
height = 900

def retrieve_background(choice):
    background = None
    folder = "images/"
    if choice == "cave":
        background = pygame.image.load(folder + "cave.png")
        background = pygame.transform.scale(background,(1600,900))
    elif choice == "forest":
        background = pygame.image.load(folder + "forest.png")
        background = pygame.transform.scale(background,(1600,900))
    elif choice == "village":
        background = pygame.image.load(folder + "village.jpg")
        background = pygame.transform.scale(background,(1600,900))
    elif choice == "map":
        background = pygame.image.load(folder + "map1.png")
        background = pygame.transform.scale(background,(1600,900))
    elif choice == "villageinn":
        background = pygame.image.load(folder + "villagemenuinn.png")
        background = pygame.transform.scale(background,(1600,900))
    elif choice == "villageinnnight":
        background = pygame.image.load(folder + "villagemenuinnnight.png")
        background = pygame.transform.scale(background,(1600,900))
    elif choice == "tavern":
        background = pygame.image.load(folder + "tavern.png")
        background = pygame.transform.scale(background,(1600,900))
    if background != None:
        return background
    return Exception()

def retrieve_character(choice, mc):
    char_name = mc.get_name()
    folder = "images/"
    if choice == "N. Steen" or choice == "Mysterious Bear":
        return pygame.image.load(folder + "bear.png")
    if choice == char_name:
        return pygame.image.load(mc.get_portrait())
    if choice == "Vizier":
        return pygame.image.load(folder + "vizier_port.png")
    if choice == "Guard":
        return pygame.image.load(folder + "guard.png")
    
def remove_portrait(name, slots):
    if name == "VIZGONE":
        for x in range(0,3):
            if slots[x] == "Vizier":
                slots[x] = 0
    elif name == "GUARDGONE":
        for x in range(0,3):
            if slots[x] == "Guard":
                slots[x] = 0
    elif name == "MYSTBEARGONE":
        for x in range(0,3):
            if slots[x] == "Mysterious Bear":
                slots[x] = 0
    return slots

def circle_fade_out(screen, counter_x, counter_y, fade):
    fade = pygame.transform.scale(fade,(12800 - counter_x,7200 - counter_y))
    screen.blit(fade, (-5600+counter_x/2, -3150+counter_y/2))
    pygame.display.flip()

def circle_fade_in(screen, counter_x, counter_y, fade):
    fade = pygame.transform.scale(fade,(0 + counter_x,0 + counter_y))
    screen.blit(fade, (7200-counter_x/2, 4050-counter_y/2))
    pygame.display.flip()

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
            Enemy("Gobble", 10, 5, 5, 5, 5, 100),
            Enemy("Goobble", 10, 5, 5, 5, 5, 100),
            Enemy("Gabble", 10, 5, 5, 5, 5, 100)
        ], 300]


def turn_order(group):
    turns = []
    for character in group:
        roll = random.randint(0, character.get_quickness())
        turns.append((character, roll, "p"))
    turns = sorted(turns, key=lambda turn:turn[1], reverse=True)
    return turns


def find_and_remove_from_turn(turns, character):
    for nest in turns:
        if nest[0] == character:
            turns.remove(nest)
            return turns


def add_party_member(name, char=None):
    if name == "nsteen":
        nsteen = BearKnight([15, 15, 10, 10, 10, 10])
        nsteen.set_name("N. Steen")
        return nsteen
    if name == "radish":
        radish = Bookish([15, 15, 10, 10, 10, 10])
        radish.set_name("Radish")
        return radish
    if name == "toffee":
        toffee = Martial([15, 15, 20, 20, 20, 20])
        toffee.set_name("Toffee")
        return toffee
    if name == "grapefart":
        grapefart = Merchant([15, 15, 10, 10, 10, 10])
        grapefart.set_name("Grapefart")
        return grapefart
    if name == "maincharacter":
        return char


def fill_party():
    mc = create_default_main_character()
    nsteen = BearKnight([15, 10, 10, 5, 5, 0])
    nsteen.set_name("N. Steen")
    nsteen.set_portrait_dungeon("bear")
    radish = Bookish([15, 10, 10, 5, 5, 0])
    radish.set_name("Radish")
    radish.set_portrait("rabbit_portrait_100.png")
    cinna = Cleric([15, 10, 10, 5, 5, 0])
    cinna.set_name("Cinna")
    cinna.set_portrait("cinna_portrait_100.png")
    party = [mc, nsteen, radish, cinna]
    for char in party:
        char.print_stats()
    return party

def create_default_main_character():
    char = MainCharacter([10,10,10,10,10,10])
    char.set_name("Dog")
    char.set_portrait("dogdude_port_100.png")
    char.set_portrait_dungeon("dogdude")
    return char

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
        portrait = pygame.transform.scale(portrait,(96,96))
        return portrait
    if character in ["Goblin_Stand"]:
        portrait = pygame.image.load("images/goblin_stand.png")
        portrait = pygame.transform.scale(portrait,(96,96))
        return portrait
    if character in ["Goobble"]:
        portrait = pygame.image.load("images/goobble.png")
        portrait = pygame.transform.scale(portrait,(96,96))
        return portrait
    if character in ["Gabble"]:
        portrait = pygame.image.load("images/gabble.png")
        portrait = pygame.transform.scale(portrait,(96,96))
        return portrait
    if character in ["dogdude"]:
        portrait = pygame.image.load("images/dogdude.png")
        portrait = pygame.transform.scale(portrait,(60,120))
        return portrait
    
def get_portrait_2(character):
    if character == "N. Steen":
        return "images/bear_portrait_100.png"
    if character == "Radish":
        return "images/rabbit_portrait_100.png"
    if character == "Toffee":
        return "images/toffee_portrait_100.png"
    if character == "Grapefart":
        return "images/grapefart_portrait_100.png"
    if character == "Cinna":
        return "images/cinna_portrait_100.png"
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

def debug_timing(message, timer):
    print(message + ": " + str(timer - pygame.time.get_ticks()))
    return pygame.time.get_ticks()

bitmap_tex = None
def blit_image(display, x, y, img, r, g, b):
    global bitmap_tex

    # get texture data
    w,h = img.get_size()
    raw_data = img.get_buffer().raw
    data = np.fromstring(raw_data, np.uint8)

    # create texture object
    if bitmap_tex == None:
      bitmap_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, bitmap_tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_BGRA,GL_UNSIGNED_BYTE,data)

    # save and set model view and projection matrix
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display[0], 0, display[1], -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # enable blending
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    # draw textured quad
    glColor3f(r,g,b)

    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(x, y)
    glTexCoord2f(1, 1)
    glVertex2f(x+w, y)
    glTexCoord2f(1, 0)
    glVertex2f(x+w, y+h)
    glTexCoord2f(0, 0)
    glVertex2f(x, y+h)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # restore matrices
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    # disable blending
    glDisable(GL_BLEND)

def rect_ogl(color, left, right, bot, top, debug=0):
        shape_color(color)
        vertices = np.array([
            [left, bot],
            [left, top],
            [right, top],
            [right, bot]
        ], dtype=np.float32)
        for vertex_pair in vertices:
            glVertex2f(vertex_pair[0], vertex_pair[1])
            if debug == 1:
                print("Drew triangle at vertices " + str(vertex_pair[0]) + " and " + str(vertex_pair[1]) + ".")

def draw_outline(color, left, right, bot, top, debug=0):
        shape_color(color)
        vertices = np.array([
            [left, bot],
            [left, top],
            [right, top],
            [right, bot],
        ], dtype=np.float32)
        glBegin(GL_LINES)
        for vertex_pair in vertices:
            glVertex2f(vertex_pair[0], vertex_pair[1])
        glEnd()

def shape_color(color):
        if color == "BLUE":
            glColor3f(0.0, 0.0, 1.0)
        elif color == "RED":
            glColor3f(1.0, 0.0, 0.0)
        elif color == "GREEN":
            glColor3f(0.0, 1.0, 0.0)
        elif color == "BLACK":
            glColor3f(0.0, 0.0, 0.0)
        elif color == "PINK":
            glColor3f(222.0, 49.0, 99.0)
        elif color == "WHITE":
            glColor3f(255.0, 255.0, 255.0)
        else:
            Exception("Wrong format")

def gl_text(font, rect_color, right, left, bot, top, text, x_adjust, y_adjust):
    glBegin(GL_QUADS)
    rect_ogl(rect_color, left, right, bot, top)
    glEnd()
    drawText_gl(rect_color, font, left, bot, text, x_adjust, y_adjust)

def gl_text_wrap(font, display, rect_color, left, right, bot, top, text, x_adjust, y_adjust, level):
    glBegin(GL_QUADS)
    rect_ogl(rect_color, left, right, bot, top)
    glEnd()
    drawTextWrap(rect_color, font, display, text, rect_color, left, top, x_adjust, y_adjust, level)

def drawText_gl(rect_color, font, x, y, text, x_adjust, y_adjust):                                                
    textSurface = font.render(text, True, (255, 255, 255, 255), rect_color)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    new_x = ((x+1)/2)*width/x_adjust
    new_y = ((y+1)/2)*height/y_adjust
    glWindowPos2d(new_x, new_y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def drawTextWrap(rect_color, font, surface, text, color, x, y, x_adjust, y_adjust, level, bkg=None, aa=False, center=False):
    rect = pygame.Rect(x,y,600,100)
    y = rect.top
    lineSpacing = 0
    image = None
    new_x = ((x+1)/2)*width/x_adjust
    new_y = ((y+1)/2)*height/y_adjust #- (self.level*100)

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width-80 and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        textSurface = font.render(text[:i], True, (255, 255, 255, 0), rect_color)
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        text_rect = textSurface.get_rect()
        
        if center == True:
            glWindowPos2d(new_x, new_y)
            glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
        else:
            glWindowPos2d(new_x,new_y)
            glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
        new_y -= fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]
        level += 1

    if input == True:
        return image
    if text == "":
        level = 0
    return text

def blit_bg(i, bg="cave.png", move=True):
    background = pygame.image.load("images/" + bg).convert_alpha()
    background = pygame.transform.scale(background,(1600,900))
    if move == True:
        blit_image([width, height], width+i, 0, background, 1, 1, 1)
        blit_image([width, height], i, 0, background, 1, 1, 1)
        if (i == -width):
            blit_image([width, height], width+i, 0, background, 1, 1, 1)
            i=0
        i-=1
        return i
    else: blit_image([width, height], 0, 0, background, 1, 1, 1)


def cgls(value, length):
    return ((value/length) * 2) - 1

def drawCircleGL(x, y, z, radius, numSides):
    numVertices = numSides + 2
    doublePi = 2.0 * math.pi

    vertex_list = [x, y, z]
    for i in range(1, numVertices):
        vertex_list.append(x + (radius * math.cos(i * doublePi / numSides)))
        vertex_list.append(y + (radius * math.sin(i * doublePi / numSides)))
        vertex_list.append(z)
    allCircleVertices = np.array([vertex_list], dtype='f')

    vboc = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vboc)
    glBufferData(GL_ARRAY_BUFFER, allCircleVertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 3*sizeof(ctypes.c_float), ctypes.c_void_p(0))
    glDrawArrays(GL_TRIANGLE_FAN, 0, numVertices)

if __name__ == "__main__":
    print("This is the helper file. Do not run this directly.")