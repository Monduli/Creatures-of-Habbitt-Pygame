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

FPS = 120
EXPLOSION_SPEED = 15
REFILL_SPEED = 10

class Cell(object):
    """
    A cell on the board
    'image' - a 'Surface' object containing the sprite to draw
    'offset' - vertical offset in pixels for drawing the cell
    """
    def __init__(self, image):
        self.offset = 0.0
        self.image = image

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
        self.shapes = [pygame.image.load('images/{}_gem.png'.format(shape)) for shape in shapes.split()]
        for shape in self.shapes:
            shape = pygame.transform.scale(shape,(50,50))
        self.background = background
        self.blank = pygame.image.load("images/blank.png")
        self.w = width
        self.h = height
        self.size = width*height
        self.board = [Cell(self.blank) for _ in range(self.size)]
        self.matches = []
        self.refill = []
        

    def randomize(self):
        """
        replace whole board
        """
        for i in range(self.size):
            self.board[i] = Cell(random.choice(self.shapes))

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
                c.image = random.choice(self.shapes)
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

    def play(self, party):
        self.start()
        while True:
            gobble = Enemy("Gobble", 10, 5, 5)
            enemy = [gobble]

            return_rect = self.draw(party, enemy)
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
            self.swap_time += dt
            for event in pygame.event.get():
                if event.type == KEYUP:
                    self.input(event.key)
                elif event.type == QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if return_rect.collidepoint(event.pos):
                        return
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

    def draw(self, party, enemy):
        self.board.draw(self.display)
        color_return = BLACK
        #self.draw_time()
        self.draw_cursor()
        return_rect = pygame.Rect(width-600,height-50,300,50)
        party_1_rect = pygame.Rect(width-300,height-900,300,50)
        party_1_hp_rect = pygame.Rect(width-300,height-850,300,50)
        party_1_portrait_rect = pygame.Rect(width-400,height-900,100,100)
        party_2_rect = pygame.Rect(width-300,height-750,300,50)
        party_2_hp_rect = pygame.Rect(width-300,height-700,300,50)
        party_2_portrait_rect = pygame.Rect(width-400,height-750,100,100)
        party_3_rect = pygame.Rect(width-300,height-600,300,50)
        party_3_hp_rect = pygame.Rect(width-300,height-550,300,50)
        party_3_portrait_rect = pygame.Rect(width-400,height-600,100,100)
        party_4_rect = pygame.Rect(width-300,height-450,300,50)
        party_4_hp_rect = pygame.Rect(width-300,height-400,300,50)
        party_4_portrait_rect = pygame.Rect(width-400,height-450,100,100)

        if return_rect.collidepoint(pygame.mouse.get_pos()):
            color_return = pygame.Color(200,0,0)

        pygame.draw.rect(screen, color_return, return_rect)
        pygame.draw.rect(screen, color_passive, party_1_rect)
        pygame.draw.rect(screen, color_passive, party_1_hp_rect)
        pygame.draw.rect(screen, color_passive, party_1_portrait_rect)
        if len(party) > 1:
            pygame.draw.rect(screen, color_passive, party_2_rect)
            pygame.draw.rect(screen, color_passive, party_2_hp_rect)
            pygame.draw.rect(screen, color_passive, party_2_portrait_rect)
        if len(party) > 2:
            pygame.draw.rect(screen, color_passive, party_3_rect)
            pygame.draw.rect(screen, color_passive, party_3_hp_rect)
            pygame.draw.rect(screen, color_passive, party_3_portrait_rect)
        if len(party) > 3:
            pygame.draw.rect(screen, color_passive, party_4_rect)
            pygame.draw.rect(screen, color_passive, party_4_hp_rect)
            pygame.draw.rect(screen, color_passive, party_4_portrait_rect)

        port1 = get_portrait(party[0].get_name())
        self.display.blit(port1, party_1_portrait_rect)

        drawText(self.display, party[0].get_name(), WHITE, party_1_rect, self.font, center=True)
        drawText(self.display, "HEALTH: " + str(party[0].get_current_hp()) + "/" + str(party[0].get_hp()), WHITE, party_1_hp_rect, self.font, center=True)
        
        if len(party) > 1:
            port2 = get_portrait(party[1].get_name())
            self.display.blit(port2, party_2_portrait_rect)
            drawText(self.display, party[1].get_name(), WHITE, party_2_rect, self.font, center=True)
            drawText(self.display, "HEALTH: " + str(party[1].get_current_hp()) + "/" + str(party[1].get_hp()), WHITE, party_2_hp_rect, self.font, center=True)
        
        if len(party) > 2:
            drawText(self.display, party[2].get_name(), WHITE, party_3_rect, self.font, center=True)
            drawText(self.display, "HEALTH: " + str(party[2].get_current_hp()) + "/" + str(party[2].get_hp()), WHITE, party_3_hp_rect, self.font, center=True)
        
        if len(party) > 3:
            drawText(self.display, party[3].get_name(), WHITE, party_4_rect, self.font, center=True)
            drawText(self.display, "HEALTH: " + str(party[3].get_current_hp()) + "/" + str(party[3].get_hp()), WHITE, party_4_hp_rect, self.font, center=True)

        # Enemies
        enemy_1_rect = pygame.Rect(width-300,height-100,300,50)
        enemy_1_hp_rect = pygame.Rect(width-300,height-50,300,50)
        enemy_1_portrait_rect = pygame.Rect(width-300,height-50,300,50)

        pygame.draw.rect(screen, color_passive, enemy_1_rect)
        pygame.draw.rect(screen, color_passive, enemy_1_hp_rect)
        pygame.draw.rect(screen, color_passive, enemy_1_portrait_rect)

        drawText(self.display, enemy[0].get_name(), WHITE, enemy_1_rect, self.font, center=True)
        drawText(self.display, "HEALTH: " + str(enemy[0].get_chp()) + "/" + str(enemy[0].get_hp()), WHITE, enemy_1_hp_rect, self.font, center=True) 

        drawText(self.display, "Return", WHITE, return_rect, self.font, center=True)  
            
        pygame.display.update()
        return return_rect

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
        
        
if __name__ == '__main__':
    Game().play()