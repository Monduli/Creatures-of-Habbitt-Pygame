import pygame
from classes import *
import random
import varname
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

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
    
def get_portrait_2(character):
    if character == "N. Steen":
        return "images/bear_portrait_100.png"
    if character == "Radish":
        return "images/rabbit_portrait_100.png"
    if character == "Toffee":
        return "images/toffee_portrait_100.png"
    if character == "Grapefart":
        return "images/grapefart_portrait_100.png"
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

"""
def draw_old(self, party, enemy, active, p_text, e_text, flash_red, xp=None, update_text=None):
    if p_text == "Your party was victorious!":
        xp_count = 0
        while True:
            self.display.blit(background, (0,0))
            victory_rect = pygame.Rect(width-1600,height-450,1600,50)
            drawText(self.display, p_text, WHITE, victory_rect, self.font, center=True)
            xp_rect = pygame.Rect(width-1600,height-550,1600,50)
            xp_count += 1
            drawText(self.display, "XP: " + str(xp_count), WHITE, xp_rect, self.font, center=True)
            self.pyg_wait(.01)
            if xp_count == xp:
                self.pyg_wait(3)
                return "WIN"
    if e_text == "Your party was wiped out...":
        self.display.blit(background, (0,0))
        victory_rect = pygame.Rect(width-1600,height-450,1600,50)
        drawText(self.display, e_text, WHITE, victory_rect, self.font, center=True)
        return "DEAD"
    
    color_0 = color_passive
    color_1 = color_passive
    color_2 = color_passive
    color_3 = color_passive

    if flash_red != None:
        if flash_red == 0:
            color_0 = pygame.Color('Red') 
        if flash_red == 1:
            color_1 = pygame.Color('Red') 
        if flash_red == 2:
            color_2 = pygame.Color('Red') 
        if flash_red == 3:
            color_3 = pygame.Color('Red')    

    screen.blit(background, (width+self.i,0))
    screen.blit(background, (self.i, 0))
    if (self.i == -width):
        screen.blit(background, (width+self.i, 0))
        self.i=0
    self.i-=1
    self.board.draw(self.display)
    color_return = BLACK

    if self.timing == 1:
        self.debug_timer = debug_timing("DREW BACKGROUND", self.debug_timer)

    #self.draw_time()
    self.draw_cursor()
    return_rect = pygame.Rect(width-600,height-50,600,50)
    party_1_rect = pygame.Rect(width-500,height-900,500,50)
    party_1_hp_rect = pygame.Rect(width-500,height-850,500,50)
    party_1_portrait_rect = pygame.Rect(width-600,height-900,100,100)
    party_2_rect = pygame.Rect(width-500,height-800,500,50)
    party_2_hp_rect = pygame.Rect(width-500,height-750,500,50)
    party_2_portrait_rect = pygame.Rect(width-600,height-800,100,100)
    party_3_rect = pygame.Rect(width-500,height-700,500,50)
    party_3_hp_rect = pygame.Rect(width-500,height-650,500,50)
    party_3_portrait_rect = pygame.Rect(width-600,height-700,100,100)
    party_4_rect = pygame.Rect(width-500,height-600,500,50)
    party_4_hp_rect = pygame.Rect(width-500,height-550,500,50)
    party_4_portrait_rect = pygame.Rect(width-600,height-600,100,100)

    ability_1_rect = pygame.Rect(width-600,height-500,300,75)
    ability_2_rect = pygame.Rect(width-300,height-500,300,75)
    ability_3_rect = pygame.Rect(width-600,height-425,300,75)
    ability_4_rect = pygame.Rect(width-300,height-425,300,75)

    if self.timing == 1:
        self.debug_timer = debug_timing("MADE RECTS", self.debug_timer)

    pygame.draw.rect(screen, pygame.Color('red'), ability_1_rect)
    pygame.draw.rect(screen, pygame.Color('blue'), ability_2_rect)
    pygame.draw.rect(screen, pygame.Color('green'), ability_3_rect)
    pygame.draw.rect(screen, pygame.Color('purple'), ability_4_rect)

    if self.timing == 1:
        self.debug_timer = debug_timing("DREW ABILITY RECTS", self.debug_timer)

    if return_rect.collidepoint(pygame.mouse.get_pos()):
        color_return = pygame.Color(200,0,0)

    pygame.draw.rect(screen, color_return, return_rect)
    pygame.draw.rect(screen, color_0, party_1_rect)
    pygame.draw.rect(screen, color_0, party_1_hp_rect)
    #pygame.draw.rect(screen, color_passive, party_1_portrait_rect)
    if len(party) > 1:
        pass
        pygame.draw.rect(screen, color_1, party_2_rect)
        pygame.draw.rect(screen, color_1, party_2_hp_rect)
        #pygame.draw.rect(screen, color_passive, party_2_portrait_rect)
    if len(party) > 2:
        pass
        pygame.draw.rect(screen, color_2, party_3_rect)
        pygame.draw.rect(screen, color_2, party_3_hp_rect)
        #pygame.draw.rect(screen, color_passive, party_3_portrait_rect)
    if len(party) > 3:
        pass
        pygame.draw.rect(screen, color_3, party_4_rect)
        pygame.draw.rect(screen, color_3, party_4_hp_rect)
        #pygame.draw.rect(screen, color_passive, party_4_portrait_rect)

    if self.timing == 1:
        self.debug_timer = debug_timing("DREW PARTY RECTS", self.debug_timer)

    port1 = get_portrait(party[0].get_name())
    self.display.blit(port1, party_1_portrait_rect)

    drawText(self.display, party[0].get_name(), WHITE, party_1_rect, self.font, center=True)
    drawText(self.display, "HEALTH: " + str(party[0].get_chp()) + "/" + str(party[0].get_hp()), WHITE, party_1_hp_rect, self.font, center=True)
    
    if len(party) > 1:
        port2 = get_portrait(party[1].get_name())
        self.display.blit(port2, party_2_portrait_rect)
        drawText(self.display, party[1].get_name(), WHITE, party_2_rect, self.font, center=True)
        drawText(self.display, "HEALTH: " + str(party[1].get_chp()) + "/" + str(party[1].get_hp()), WHITE, party_2_hp_rect, self.font, center=True)
    
    if len(party) > 2:
        port3 = get_portrait(party[2].get_name())
        self.display.blit(port3, party_3_portrait_rect)
        drawText(self.display, party[2].get_name(), WHITE, party_3_rect, self.font, center=True)
        drawText(self.display, "HEALTH: " + str(party[2].get_chp()) + "/" + str(party[2].get_hp()), WHITE, party_3_hp_rect, self.font, center=True)
    
    if len(party) > 3:
        port4 = get_portrait(party[3].get_name())
        self.display.blit(port4, party_4_portrait_rect)
        drawText(self.display, party[3].get_name(), WHITE, party_4_rect, self.font, center=True)
        drawText(self.display, "HEALTH: " + str(party[3].get_chp()) + "/" + str(party[3].get_hp()), WHITE, party_4_hp_rect, self.font, center=True)

    if self.timing == 1:
        self.debug_timer = debug_timing("PARTY DONE", self.debug_timer)

    # Enemies
    enemy_1_rect = pygame.Rect(width-300,height-150,300,50)
    enemy_1_hp_rect = pygame.Rect(width-300,height-100,300,50)
    enemy_1_portrait_rect = pygame.Rect(width-400,height-150,100,100)

    #next_rect = pygame.Rect(width-500,height-300,100,100)
    #enemy_2_rect = pygame.Rect(width-300,height-300,300,50)
    #enemy_2_hp_rect = pygame.Rect(width-300,height-250,300,50)
    enemy_2_portrait_rect = pygame.Rect(width-500,height-150,100,100)
    enemy_3_portrait_rect = pygame.Rect(width-600,height-150,100,100)

    pygame.draw.rect(screen, color_passive, enemy_1_rect)
    pygame.draw.rect(screen, color_passive, enemy_1_hp_rect)
    #pygame.draw.rect(screen, color_passive, enemy_1_portrait_rect)

    port_e1 = get_portrait(enemy[0].get_name())
    self.display.blit(port_e1, enemy_1_portrait_rect)
    drawText(self.display, enemy[0].get_name(), WHITE, enemy_1_rect, self.font, center=True)
    if enemy[0].get_chp() > 10:
        drawText(self.display, str(enemy[0].get_chp()) + "/" + str(enemy[0].get_hp()), WHITE, enemy_1_hp_rect, self.font, center=True) 
    else:
        drawText(self.display, "HEALTH: " + str(enemy[0].get_chp()) + "/" + str(enemy[0].get_hp()), WHITE, enemy_1_hp_rect, self.font, center=True) 
    
    if len(enemy) > 1:
        #pygame.draw.rect(screen, color_passive, next_rect)
        port_e2 = get_portrait(enemy[1].get_name())
        #pygame.draw.rect(screen, color_passive, enemy_2_rect)
        #pygame.draw.rect(screen, color_passive, enemy_2_hp_rect)
        #pygame.draw.rect(screen, color_passive, enemy_2_portrait_rect)
        self.display.blit(port_e2, enemy_2_portrait_rect)
        #drawText(self.display, enemy[1].get_name(), WHITE, enemy_2_rect, self.font, center=True)
        #drawText(self.display, "HEALTH: " + str(enemy[1].get_chp()) + "/" + str(enemy[1].get_hp()), WHITE, enemy_2_hp_rect, self.font, center=True)
        #drawText(self.display, "NEXT", WHITE, next_rect, self.font, center=True)

    if len(enemy) > 2:
        #pygame.draw.rect(screen, color_passive, next_rect)
        port_e3 = get_portrait(enemy[2].get_name())
        #pygame.draw.rect(screen, color_passive, enemy_2_rect)
        #pygame.draw.rect(screen, color_passive, enemy_2_hp_rect)
        #pygame.draw.rect(screen, color_passive, enemy_3_portrait_rect)
        self.display.blit(port_e3, enemy_3_portrait_rect)
    
    if self.timing == 1:
        self.debug_timer = debug_timing("ENEMY DONE", self.debug_timer)

    drawText(self.display, "Return", WHITE, return_rect, self.font, center=True) 
    party_box = pygame.Rect(width-600,height-350,600,100) 
    enemy_box = pygame.Rect(width-600,height-250,600,100)
    self.update_box(p_text, party_box)
    self.update_box(e_text, enemy_box)

    #Highlight whose turn it is
    if party[0] == active:
        drawStyleRect(screen, width-500, height-900)
    elif party[1] == active:
        drawStyleRect(screen, width-500, height-800)
    elif party[2] == active:
        drawStyleRect(screen, width-500, height-700)
    elif party[3] == active:
        drawStyleRect(screen, width-500, height-600)

    if self.timing == 1:
        self.debug_timer = debug_timing("HIGHLIGHT DONE", self.debug_timer)

    if self.board.busy == True:
        busy_rect = pygame.Rect(width-350,height-475,200,50)
        pygame.draw.rect(screen, color_passive, busy_rect)  
        drawText(self.display, "Please Wait...", WHITE, busy_rect, self.font, center=True)

    if self.timing == 1:
        self.debug_timer = debug_timing("PLEASE WAIT", self.debug_timer) 

    #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    pygame.display.flip()
    if self.timing == 1:
        self.debug_timer = debug_timing("DRAW DONE", self.debug_timer)
    return return_rect

def update_box_old(self, text, box):
    pygame.draw.rect(screen, color_passive, box)
    self.gl_text("WHITE", text, WHITE, box, self.font, center=True)

"""

if __name__ == "__main__":
    print("This is the helper file. Do not run this directly.")