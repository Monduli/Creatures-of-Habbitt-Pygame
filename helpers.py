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
    folder = "images/backgrounds/"
    if choice == "cave":
        background = "cave.png"
    elif choice == "forest":
        background = "forest.png"
    elif choice == "village":
        background = "village.jpg"
    elif choice == "map":
        background = "map1.png"
    elif choice == "villageinn":
        background = "villagemenuinn.png"
    elif choice == "villageinnnight":
        background = "villagemenuinnnight.png"
    elif choice == "tavern":
        background = "tavern.png"
    elif choice == "outside_castle_wall":
        background = "outside_castle_wall.png"
    elif choice == "hill":
        background = "hill.png"
    elif choice == "royalbedroom":
        background = "royalbedroom.png"
    elif choice == "stat_menu":
        background = "menu_bg.png"
    elif choice == "options_menu":
        background = "options_menu_bg.png"
    if background != None:
        return background
    return Exception()

def retrieve_character(choice, characters, portrait=False):
    main_character_name = characters[0].get_name()
    folder = "images/"
    if not portrait:
        if choice == "N. Steen" or choice == "Mysterious Bear":
            return characters[1].get_dialog_picture()
        if choice == main_character_name:
            return characters[0].get_dialog_picture()
        if choice == "Vizier":
            return pygame.image.load(folder + "vizier_port.png").convert_alpha()
        if choice == "Guard":
            return pygame.image.load(folder + "guard.png").convert_alpha()
        if choice == "Hippo" or "Henrietta":
            return pygame.image.load(folder + "hippo.png").convert_alpha()
    else:
        if choice == "N. Steen" or choice == "Mysterious Bear":
            return characters[1].get_portrait_dialog()
        if choice == main_character_name:
            return characters[0].get_portrait_dialog()
        if choice == "Vizier":
            return pygame.image.load(folder + "fox_port.png").convert_alpha()
        if choice == "Guard":
            return pygame.image.load(folder + "pig_port.png").convert_alpha()
        if choice == "Hippo" or "Henrietta":
            return pygame.image.load(folder + "hippo_port.png").convert_alpha()
    
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
            if slots[x] == "Mysterious Bear" or slots[x] == "N. Steen":
                slots[x] = 0
    elif name == "HENRIETTAGONE":
        for x in range(0,3):
            if slots[x] == "Henrietta" or slots[x] == "Hippo":
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
            Enemy("Gobble", 10, 5, 5, 5, 5, 1000)
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
        nsteen = BearNSteen([15, 15, 10, 10, 10, 10])
        nsteen.set_name("N. Steen")
        return nsteen
    if name == "radish":
        radish = Radish([15, 15, 10, 10, 10, 10])
        radish.set_name("Radish")
        return radish
    if name == "toffee":
        toffee = Martial([15, 15, 20, 20, 20, 20])
        toffee.set_name("Toffee")
        return toffee
    if name == "grapefart":
        grapefart = Grapefart([15, 15, 10, 10, 10, 10])
        grapefart.set_name("Grapefart")
        return grapefart
    if name == "maincharacter":
        return char

def fill_party():
    mc = create_default_main_character()
    nsteen = BearNSteen([15, 10, 10, 5, 5, 0])
    radish = Radish([15, 10, 10, 5, 5, 0])
    grapefart = Grapefart([15, 10, 10, 5, 5, 0])
    party = [mc, nsteen, radish, grapefart]
    for char in party:
        char.print_stats()
    return party

def boost_party(party):
    #mc.boost(9998, mc.stat_spread)
    for char in party:
        level = char.get_level()
        to_boost = 9999 - level
        char.boost(to_boost, char.stat_spread)
    return party

def add_all_characters(party, rom_characters, character_names, npc_characters, npc_names, characters):
    radish = Radish("S")
    grapefart = Grapefart("S")
    lambaste = Lambaste("S")
    sunny = SunnySpider("S")
    hollow = Hollow("S")
    dane = Dane("S")
    rayna = Rayna("S")

    radish.set_recruited(True)
    grapefart.set_recruited(True)
    lambaste.set_recruited(True)
    sunny.set_recruited(True)
    hollow.set_recruited(True)
    dane.set_recruited(True)
    rayna.set_recruited(True)

    party[2] = radish
    party[3] = grapefart

    rom_characters[2] = party[2]
    rom_characters[3] = party[3]
    rom_characters[4] = lambaste
    rom_characters[5] = sunny
    rom_characters[9] = hollow
    character_names[2] = "Radish"
    character_names[3] = "Grapefart"
    character_names[4] = "Lam'baste"
    character_names[5] = "Sunny"
    character_names[10] = "Hollow"

    # generate 2 npc characters, add to npc and name lists
    npc_characters[2] = dane
    npc_characters[3] = rayna
    npc_names[2] = "Dane"
    npc_names[3] = "Rayna"

    characters[2] = radish
    characters[3] = grapefart
    characters[4] = lambaste
    characters[5] = sunny
    characters[9] = hollow
    characters[13] = dane
    characters[14] = rayna

    return party, rom_characters, character_names, npc_characters, npc_names, characters

def create_default_main_character():
    char = MainCharacter([10,10,10,10,10,10])
    char.set_name("Dog")
    char.set_portrait("dogdude_port_100.png")
    char.set_portrait_dungeon("dogdude")
    char.set_portrait_dialog("dogdude_portrait")
    char.set_stats_picture("dogdude_port")
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
    if character in ["Bazongle_Stand"]:
        portrait = pygame.image.load("images/bazongle.png")
        portrait = pygame.transform.scale(portrait,(96,96))
        return portrait
    if character in ["Bazongle"]:
        portrait = pygame.image.load("images/bazongle_port.png")
        portrait = pygame.transform.scale(portrait,(96,96))
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
def blit_image(display_wh, x, y, img, r, g, b):
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
    glOrtho(0, display_wh[0], 0, display_wh[1], -1, 1)
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

def blits_images(blit_sequence, display_wh):
    for z in blit_sequence:
        x = z[1].left
        y = z[1].bottom
        blit_image(display_wh, x, y, z[0], 1,1,1)
    return blit_sequence

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
            glColor3f(c_c(227), c_c(28), c_c(121))
        elif color == "WHITE":
            glColor3f(255.0, 255.0, 255.0)
        elif color == "GRAY":
            glColor3f(47.0, 79.0, 79.0)
        else:
            Exception("Wrong format")

def c_c(c):
    # color conversion for rgb format
    return c/255


def gl_text(font, rect_color, right, left, bot, top, text, x_adjust, y_adjust):
    glBegin(GL_QUADS)
    rect_ogl(rect_color, left, right, bot, top)
    glEnd()
    drawText_gl_internal(rect_color, font, left, bot, text, x_adjust, y_adjust)

def gl_text_name(font, rect_color, right, left, bot, top, text, x_adjust, y_adjust, black_text=False):
    glBegin(GL_QUADS)
    rect_ogl(rect_color, left, right, bot, top)
    glEnd()
    if black_text == True:
        text_color = (0,0,0, 255) 
    else:
        text_color = (255, 255, 255, 255)
    drawText_gl_internal(rect_color, font, left - ((left-right)/2), bot, text, x_adjust, y_adjust, text_color, True)

def gl_text_wrap(font, display, rect_color, left, right, bot, top, text, x_adjust, y_adjust, level):
    glBegin(GL_QUADS)
    rect_ogl(rect_color, left, right, bot, top)
    glEnd()
    rect_width = abs(reverse_cgls(right, width) - reverse_cgls(left, width))
    rect_height = abs(reverse_cgls(bot, height) - reverse_cgls(top, height))
    drawTextWrap_internal(rect_color, font, display, text, rect_color, left, top, x_adjust, y_adjust, level, rect_width, rect_height)

def drawText_gl_internal(rect_color, font, x, y, text, x_adjust, y_adjust, text_color=(255, 255, 255, 255), center=False):                                                
    textSurface = font.render(text, True, text_color, rect_color)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    if center == True:
        new_x = ((x+1)/2)*width/x_adjust - (textSurface.get_width() / 2)
    else:
        new_x = ((x+1)/2)*width/x_adjust
    new_y = ((y+1)/2)*height/y_adjust
    glWindowPos2d(new_x, new_y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def drawTextWrap_internal(rect_color, font, surface, text, color, x, y, x_adjust, y_adjust, level, r_w, r_h, bkg=None, aa=False, center=False):
    if rect_color == "PINK":
        rect_color = (227, 28, 121)
    rect = pygame.Rect(x, y, r_w, r_h)
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

def gl_text_wrap_dialog(font, rect_color, left, right, bot, top, text, x_adjust, y_adjust, level):
    glBegin(GL_QUADS)
    rect_ogl(rect_color, left, right, bot, top)
    glEnd()
    rect_width = reverse_cgls(right, width) - reverse_cgls(left, width)
    rect_height = reverse_cgls(bot, height) - reverse_cgls(top, height)
    drawTextWrap_dialog_internal(rect_color, font, text, left, top, x_adjust, y_adjust, level, rect_width, rect_height)

def drawTextWrap_dialog_internal(rect_color, font, text, x, y, x_adjust, y_adjust, level, rect_width, rect_height, bkg=None, aa=False, center=False):
    rect = pygame.Rect(x,y,rect_width,rect_height)
    y = rect.top
    lineSpacing = 0
    image = None
    #if center == True:
    #    new_x = ((x+1)/2)*width/x_adjust - (textSurface.get_width() / 2)
    #else:
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
    if isinstance(bg, str):
        background = pygame.image.load("images/backgrounds/" + bg).convert_alpha()
        background = pygame.transform.scale(background,(1600,900))
    else:
        background = bg
    if move == True:
        blit_image([width, height], width+i, 0, background, 1, 1, 1)
        blit_image([width, height], i, 0, background, 1, 1, 1)
        if (i == -width):
            blit_image([width, height], width+i, 0, background, 1, 1, 1)
            i=0
        i-=1
        return i
    else: 
        blit_image([width, height], 0, 0, background, 1, 1, 1)
        return i


def cgls(value, length):
    return ((value/length) * 2) - 1

def reverse_cgls(value, length):
    return (value + 1) / 2 * length
    

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

def character_full_name(char_name):
    if char_name == "N. Steen":
        return "Bear N. Steen"
    elif char_name == "Grapefart":
        return "Gilbert Grapefart"
    elif char_name == "Rayna":
        return "Rayna Raven"
    else:
        return char_name
    
def add_char(char):
    if char == "dane":
        dane = Dane([15, 10, 10, 10, 10, 10])
        return dane
    if char == "rayna":
        rayna = Rayna([15, 10, 10, 10, 10, 10])
        return rayna
    
def which_num_party_member(m_n, mc_name):
        # bonds list:
            # [0] - Main Character (M/F)
            # [1] - Bear N. Steen (M)
            # [2] - Radish Rabbit (F)
            # [3] - Gil Grapefart (M)
            # [4] - Lam'baste Lamb (F)
            # [5] - Sunny Spider (F)
            # [6] - Oscar Lion (M)
            # [7] - Hans Horse (M)
            # [8] - Sidney Shark (F)
            # [9] - None
            # [10] - Hollow
            # [11] - Henrietta
            # [12] - Grilla
            # [13] - Dane
            # [14] - Rayna
            # [15] - None
            # [16] - None
            # [17] - None
            # [18] - None
            # [19] - None
            # [20] - None
            # [21] - None
        if m_n == mc_name:
            return 0
        if m_n == "N. Steen":
            return 1
        if m_n == "Radish":
            return 2
        if m_n == "Grapefart":
            return 3
        if m_n == "Lam'baste":
            return 4
        if m_n == "Sunny":
            return 5
        if m_n == "Oscar":
            return 6
        if m_n == "Hans":
            return 7
        if m_n == "Sidney":
            return 8
        if m_n == "TBH":
            return 9
        if m_n == "Hollow":
            return 10
        if m_n == "Henrietta":
            return 11
        if m_n == "Grilla":
            return 12
        if m_n == "Dane":
            return 13
        if m_n == "Rayna":
            return 14
        if m_n == "TBH":
            return 15
        if m_n == "TBH":
            return 16

if __name__ == "__main__":
    print("This is the helper file. Do not run this directly.")