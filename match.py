####
# HUGE thanks to user Gareth Rees on StackExchange for this match 3 template.
# https://codereview.stackexchange.com/questions/15873/a-small-bejeweled-like-game-in-pygame
####


import pygame, random, time, sys
from pygame.locals import *
from helpers import *
import itertools
import os
from classes import *

size = width, height = 1600, 900
black = 0, 0, 0
speed = [3, 0]

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

color_passive = pygame.Color('black')

background = retrieve_background("cave")

PUZZLE_COLUMNS = 10
PUZZLE_ROWS = 9
SHAPE_WIDTH = 100
SHAPE_HEIGHT = 100
MARGIN = 2

RED = pygame.image.load("images/red_gem.png")
BLUE = pygame.image.load("images/blue_gem.png")
PURPLE = pygame.image.load("images/purple_gem.png")
GREEN = pygame.image.load("images/green_gem.png")
ORANGE = pygame.image.load("images/orange_gem.png")
YELLOW = pygame.image.load("images/yellow_gem.png")
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
FONT_SIZE = 36
TEXT_OFFSET = MARGIN + 5
SHAPES_LIST = [RED, BLUE, PURPLE, GREEN, ORANGE, YELLOW]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MINIMUM_MATCH = 3

FPS = 30
EXPLOSION_SPEED = 15
REFILL_SPEED = 10

class Cell(object):
    """
    A cell on the board
    'image' - a 'Surface' object containing the sprite to draw
    'offset' - vertical offset in pixels for drawing the cell
    """
    def __init__(self, image, shape):
        self.offset = 0.0
        self.image = image
        self.shape = shape

    def tick(self, dt):
        self.offset = max(0.0, self.offset - dt * REFILL_SPEED)

class Board(object):
    """
    Board of cells
    'w' - width, in cells
    'h' - height, in cells
    'size' - total number of cells
    'board' - list of cells
    'matches' -- list of matches, each being a list of exploding cells
    'refill' -- list of cells that are moving up to refill the board
    """

    def __init__(self, width, height, background):
        self.explosion = [pygame.image.load('images/explosion{}.png'.format(i)) for i in range(1, 1)]
        shapes = 'red blue purple green orange yellow'
        self.shapes = []
        self.type_shape = []
        for shape in shapes.split():
            self.shapes.append(pygame.image.load('images/{}_gem.png'.format(shape)))
            self.type_shape.append(shape)
        for shape in self.shapes:
            shape = pygame.transform.scale(shape,(50,50))
        self.background = background
        self.blank = pygame.image.load("images/blank.png")
        self.w = width
        self.h = height
        self.size = width*height
        self.board = [Cell(self.blank, None) for _ in range(self.size)]
        self.matches = []
        self.refill = []
        global curr_match
        curr_match = []
        

    def randomize(self):
        """
        replace whole board
        """
        for i in range(self.size):
            c = random.randint(0, 5)
            self.board[i] = Cell(self.shapes[c], self.type_shape[c])

    def pos(self, i, j):
        assert(0 <= i < self.w)
        assert(0 <= j < self.h)
        return j * self.w + i
    
    def busy(self):
        return self.refill or self.matches
    
    def tick(self, dt):
        if self.refill:
            for c in self.refill:
                c.tick(dt)
            self.refill = [c for c in self.refill if c.offset > 0]
            if self.refill:
                return
        elif self.matches:
            self.explosion_time += dt
            f = int(self.explosion_time * EXPLOSION_SPEED)
            if f < len (self.explosion):
                self.update_matches(self.explosion[f])
                return
            self.update_matches(self.blank)
            self.refill = list(self.refill_columns())
        self.explosion_time = 0
        self.matches = self.find_matches()

    def draw(self, display):
        display.blit(self.background, (0,0))
        for i, c in enumerate(self.board):
            display.blit(c.image,
                        (MARGIN + SHAPE_WIDTH * (i % self.w),
                        MARGIN + SHAPE_HEIGHT * (i // self.w - c.offset)))
            
    def swap(self, cursor):
        i = self.pos(*cursor)
        b = self.board
        b[i], b[i+1] = b[i+1], b[i]
        self.matches = self.find_matches()

    def find_matches(self):
        def lines():
            for j in range(self.h):
                yield range(j * self.w, (j+1) * self.w)
            for i in range(self.w):
                yield range(i, self.size, self.w)
        def key(i):
            return self.board[i].image
        def matches():
            for line in lines():
                for _, group in itertools.groupby(line, key):
                    match = list(group)
                    if len(match) >= MINIMUM_MATCH:
                        yield match
        return list(matches())
    
    def update_matches(self,image):
        for match in self.matches:
            for position in match:
                global curr_match
                curr_match.append(self.board[position])
                self.board[position].image = image

    def refill_columns(self):
        for i in range(self.w):
            target = self.size - i - 1
            for pos in range(target, -1, -self.w):
                if self.board[pos].image != self.blank:
                    c = self.board[target]
                    c.image = self.board[pos].image
                    c.offset = (target - pos) // self.w
                    target -= self.w
                    yield c
            offset = 1 + (target - pos) // self.w
            for pos in range(target, -1, -self.w):
                c = self.board[pos]
                ran = random.randint(0, 5)
                c.image = self.shapes[ran]
                c.shape = self.type_shape[ran]
                c.offset = offset
                yield c

def get_portrait(character):
    if character == "N. Steen":
        portrait = pygame.image.load("images/bear_portrait.png")
        portrait = pygame.transform.scale(portrait,(100,100))
        return portrait
    if character == "Radish":
        portrait = pygame.image.load("images/rabbit_portrait.png")
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
    
class Game(object):

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                               pygame.RESIZABLE)
        self.board = Board(PUZZLE_COLUMNS, PUZZLE_ROWS, background)
        self.font = pygame.font.Font('font/VCR.001.ttf', FONT_SIZE)

    def start(self):
        self.board.randomize()
        self.cursor = [0,0]
        self.swap_time = 1

    def quit(self):
        pygame.quit()
        sys.exit()

    def play(self, party, dungeon):
        self.start()
        for member in party:
            member.set_chp(member.get_hp())
        enemy = dungeon
        turns = turn_order(party, enemy)
        current = 0
        global curr_match
        matches = True
        while matches:
            if len(self.board.find_matches()) > 0:
                self.board.randomize()
            else:
                matches = False
        while True:
            active = turns[current]
            update_text = "It is " + active[0].get_name() + "'s turn."
            return_rect = self.draw(party, enemy, active, update_text)
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
            self.swap_time += dt
            if active[2] == "p":
                for event in pygame.event.get():
                    if event.type == KEYUP:
                        self.input(event.key)
                    elif event.type == QUIT:
                        self.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if return_rect.collidepoint(event.pos):
                            return "RAN"
            if active[2] == "p":
                if len(curr_match) > 0:
                    state = self.process_action(curr_match[0], party, enemy, active)
                    if state == "WIN":
                        return "WIN"
                    if current+1 < len(turns)-1:
                        current += 1
                    else:
                        current = 0
            elif active[2] == "e":
                state = self.enemy_attack(party, enemy, active)
                if state == "DEAD":
                    return "DEAD"
                if current+1 < len(turns )-1:
                        current += 1
                else:
                    current = 0
            curr_match = []
            self.board.tick(dt)
    
    def input(self, key):
        if key == K_q:
            self.quit()
        elif key == K_RIGHT and self.cursor[0] < self.board.w - 2:
            self.cursor[0] += 1
        elif key == K_LEFT and self.cursor[0] > 0:
            self.cursor[0] -= 1
        elif key == K_DOWN and self.cursor[1] < self.board.h - 1:
            self.cursor[1] += 1
        elif key == K_UP and self.cursor[1] > 0:
            self.cursor[1] -= 1
        elif key == K_SPACE and not self.board.busy():
            self.swap()

    def swap(self):
        self.swap_time = 0.0
        self.board.swap(self.cursor)

    def draw(self, party, enemy, active, update_text=None):
        self.board.draw(self.display)
        color_return = BLACK
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

        if return_rect.collidepoint(pygame.mouse.get_pos()):
            color_return = pygame.Color(200,0,0)

        pygame.draw.rect(screen, color_return, return_rect)
        pygame.draw.rect(screen, color_passive, party_1_rect)
        pygame.draw.rect(screen, color_passive, party_1_hp_rect)
        #pygame.draw.rect(screen, color_passive, party_1_portrait_rect)
        if len(party) > 1:
            pass
            pygame.draw.rect(screen, color_passive, party_2_rect)
            pygame.draw.rect(screen, color_passive, party_2_hp_rect)
            #pygame.draw.rect(screen, color_passive, party_2_portrait_rect)
        if len(party) > 2:
            pass
            pygame.draw.rect(screen, color_passive, party_3_rect)
            pygame.draw.rect(screen, color_passive, party_3_hp_rect)
            #pygame.draw.rect(screen, color_passive, party_3_portrait_rect)
        if len(party) > 3:
            pass
            pygame.draw.rect(screen, color_passive, party_4_rect)
            pygame.draw.rect(screen, color_passive, party_4_hp_rect)
            #pygame.draw.rect(screen, color_passive, party_4_portrait_rect)

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
            drawText(self.display, party[2].get_name(), WHITE, party_3_rect, self.font, center=True)
            drawText(self.display, "HEALTH: " + str(party[2].get_chp()) + "/" + str(party[2].get_hp()), WHITE, party_3_hp_rect, self.font, center=True)
        
        if len(party) > 3:
            drawText(self.display, party[3].get_name(), WHITE, party_4_rect, self.font, center=True)
            drawText(self.display, "HEALTH: " + str(party[3].get_chp()) + "/" + str(party[3].get_hp()), WHITE, party_4_hp_rect, self.font, center=True)

        # Enemies
        enemy_1_rect = pygame.Rect(width-300,height-150,300,50)
        enemy_1_hp_rect = pygame.Rect(width-300,height-100,300,50)
        enemy_1_portrait_rect = pygame.Rect(width-400,height-150,100,100)

        next_rect = pygame.Rect(width-500,height-300,100,100)
        enemy_2_rect = pygame.Rect(width-300,height-300,300,50)
        enemy_2_hp_rect = pygame.Rect(width-300,height-250,300,50)
        enemy_2_portrait_rect = pygame.Rect(width-500,height-150,100,100)
        enemy_3_portrait_rect = pygame.Rect(width-600,height-150,100,100)

        pygame.draw.rect(screen, color_passive, enemy_1_rect)
        pygame.draw.rect(screen, color_passive, enemy_1_hp_rect)
        #pygame.draw.rect(screen, color_passive, enemy_1_portrait_rect)

        port_e1 = get_portrait(enemy[0].get_name())
        self.display.blit(port_e1, enemy_1_portrait_rect)
        drawText(self.display, enemy[0].get_name(), WHITE, enemy_1_rect, self.font, center=True)
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

        drawText(self.display, "Return", WHITE, return_rect, self.font, center=True)  
        if update_text != None:    
            self.update_box(update_text)
        pygame.display.update()
        return return_rect
    
    def update_box(self, text):
        box = pygame.Rect(width-600,height-350,600,200)
        pygame.draw.rect(screen, color_passive, box)
        drawText(self.display, text, WHITE, box, self.font, center=True)

    def draw_time(self):
        s = int(self.swap_time)
        text = self.font.render('Move Timer: {}:{:02}'.format(s/60, s%60), True, WHITE)
        self.display.blit(text, (TEXT_OFFSET, WINDOW_HEIGHT - (FONT_SIZE * 2)))

    def draw_cursor(self):
        topLeft = (MARGIN + self.cursor[0] * SHAPE_WIDTH,
                MARGIN + self.cursor[1] * SHAPE_HEIGHT)
        topRight = (topLeft[0] + SHAPE_WIDTH * 2, topLeft[1])
        bottomLeft = (topLeft[0], topLeft[1] + SHAPE_HEIGHT)
        bottomRight = (topRight[0], topRight[1] + SHAPE_HEIGHT)
        pygame.draw.lines(self.display, WHITE, True,
                        [topLeft, topRight, bottomRight, bottomLeft], 3)
        
    def process_action(self, item, party, enemy, active):
        action = item.shape
        if action == "red":
            # do physical damage
            att = party[0].get_str()
            gua = enemy[0].get_guard()
            dmg = att - gua
            if dmg < 0:
                dmg = 0
            enemy[0].set_chp(enemy[0].get_chp() - dmg)
            update_text = active[0].get_name() + " attacked " + enemy[0].get_name() + " for " + str(dmg) + " damage!"
            self.draw(party, enemy, active, update_text)
            self.pyg_wait(3)
            if enemy[0].get_chp() <= 0:
                enemy.remove(enemy[0])
                if len(enemy) == 0:
                    return "WIN"
        elif action == "blue":
            # deal magic damage
            att = party[0].get_magic()
            gua = enemy[0].get_guard()
            dmg = att - gua
            if dmg < 0:
                dmg = 0
            enemy[0].set_chp(enemy[0].get_chp() - dmg)
            update_text = active[0].get_name() + " attacked " + enemy[0].get_name() + " for " + str(dmg) + " damage!"
            self.draw(party, enemy, active, update_text)
            self.pyg_wait(3)
            if enemy[0].get_chp() <= 0:
                update_text = enemy[0].get_name() + " has fallen!"
                self.draw(party, enemy, active, update_text)
                self.pyg_wait(3)
                enemy.remove(enemy[0])
                if len(enemy) == 0:
                    update_text = active[0].get_name() + "'s party is victorious!"
                    return "WIN"
        elif action == "green":
            # heal active party member
            heal = party[0].get_magic()
            if party[0].get_hp() < party[0].get_chp() + heal:
                party[0].set_chp(party[0].get_hp())
            else:
                party[0].set_chp(party[0].get_chp() + heal)
            update_text = active[0].get_name() + " healed for " + str(heal) + " damage."
            self.draw(party, enemy, active, update_text)
            self.pyg_wait(3)
        elif action == "orange":
            pass
            # grant support points with this unit
        elif action == "purple":
            pass
            # grant support points with next in line?
        elif action == "yellow":
            pass
            # recover action points

    def enemy_attack(self, party, enemy, active):
        # enemy goes
        self.pyg_wait(3)
        e_attack = enemy[0].get_attack()
        p_defense = party[0].get_defense()
        if e_attack > p_defense:
            dmg = e_attack - p_defense
            party[0].set_chp(party[0].get_chp() - (dmg))
            update_text = active[0].get_name() + " attacked " + party[0].get_name() + " for " + str(dmg) + " damage!"
            self.draw(party, enemy, active, update_text)
            self.pyg_wait(3)
            if party[0].get_chp() == 0:
                update_text = party[0].get_name() + " has fallen!"
                self.draw(party, enemy, active, update_text)
                self.pyg_wait(3)
            for member in party:
                if member.get_chp() <= 0:
                    continue
                else:
                    return
            update_text = "Your whole party has been defeated."
            self.draw(party, enemy, active, update_text)
            self.pyg_wait(3)
            return "DEAD"
        
    def pyg_wait(self, seconds):
        last = pygame.time.get_ticks()
        ahead = 0
        while ahead == 0:
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
            self.swap_time += dt
            self.board.tick(dt)
            pygame.display.update()
            now = pygame.time.get_ticks()
            if now - last > (seconds * 300):
                ahead = 1

if __name__ == '__main__':
    party = []
    nsteen = Paladin([15, 10, 10, 10, 10, 10])
    nsteen.set_name("N. Steen")
    #rabby = Bookish([10,10,10,15,10,10])
    #rabby.set_name("Radish")
    party.append(nsteen)
    Game().play(party, get_dungeon("cave"))