####
# HUGE thanks to user Gareth Rees on StackExchange for this match 3 template.
# https://codereview.stackexchange.com/questions/15873/a-small-bejeweled-like-game-in-pygame
####


import pygame, random, time, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from helpers import *
import itertools
import os
from classes import *
import math as Math
import varname
import threading
import display_test as dis
import numpy as np

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

# Amount of time before enemy makes a decision
TIME = 5000

RED = loadify("images/tabs/red_gem.png")
BLUE = loadify("images/tabs/blue_gem.png")
PURPLE = loadify("images/tabs/purple_gem.png")
GREEN = loadify("images/tabs/green_gem.png")
ORANGE = loadify("images/tabs/orange_gem.png")
YELLOW = loadify("images/tabs/yellow_gem.png")
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
FONT_SIZE = 36
TEXT_OFFSET = MARGIN + 5
SHAPES_LIST = [RED, BLUE, PURPLE, GREEN, ORANGE, YELLOW]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MINIMUM_MATCH = 3

FPS = 60
EXPLOSION_SPEED = 5
REFILL_SPEED = 10

class Cell(object):
    """
    A cell on the board
    'image' - a 'Surface' object containing the sprite to draw
    'offset' - vertical offset in pixels for drawing the cell
    """
    def __init__(self, image, shape, location):
        self.offset = 0.0
        self.image = image
        self.shape = shape
        self.rect = None
        self.x = None
        self.y = None
        self.location = location

    def tick(self, dt):
        self.offset = max(0.0, self.offset - dt * REFILL_SPEED)

    def get_i(self):
        return self.location
    
    def set_i(self, value):
        self.location = value

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
        self.explosion = [loadify('images/explosion{}.png'.format(i)) for i in range(1, 2)]
        for explode in self.explosion:
            explode = pygame.transform.scale(explode, (50,50))
        shapes = 'red blue purple green orange yellow'
        self.shapes = []
        self.type_shape = []
        for shape in shapes.split():
            self.shapes.append(loadify('images/tabs/{}_gem_nbd.png'.format(shape)))
            self.type_shape.append(shape)
        for shape in self.shapes:
            shape = pygame.transform.scale(shape,(50,50))
        #self.background = background
        self.blank = loadify("images/blank.png")
        self.w = width
        self.h = height
        self.size = width*height
        self.board = [Cell(self.blank, None, _) for _ in range(self.size)]
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
            self.board[i] = Cell(self.shapes[c], self.type_shape[c], i)
        #row = self.board
        #print("["+row[0].shape+"]["+row[1].shape+"]["+row[2].shape+"]["+row[3].shape+"]["+row[4].shape+"]["+row[5].shape+"]["+row[6].shape+"]["+row[7].shape+"]["+row[8].shape+"]["+row[9].shape+"]")
        #print("["+row[10].shape+"]["+row[11].shape+"]["+row[12].shape+"]["+row[13].shape+"]["+row[14].shape+"]["+row[15].shape+"]["+row[16].shape+"]["+row[17].shape+"]["+row[18].shape+"]["+row[19].shape+"]")
        #print("["+row[20].shape+"]["+row[21].shape+"]["+row[22].shape+"]["+row[23].shape+"]["+row[24].shape+"]["+row[25].shape+"]["+row[26].shape+"]["+row[27].shape+"]["+row[28].shape+"]["+row[29].shape+"]")

    def pos(self, i, j):
        assert(0 <= i < self.w)
        assert(0 <= j < self.h)
        return j * self.w + i
    
    def busy(self):
        return self.refill or self.matches
    
    def tick(self, dt, display):
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
                self.update_matches(self.explosion[f], display)
                return
            self.update_matches(self.blank, display)
            print("Refilling columns")
            self.refill = list(self.refill_columns())
        self.explosion_time = 0
        self.matches = self.find_matches()

    def draw(self, display):
        #display.blit(self.background, (0,0))
        for i, c in enumerate(self.board):
            x = MARGIN + SHAPE_WIDTH * (i % self.w)
            y = MARGIN + SHAPE_HEIGHT * (i // self.w - c.offset)
            #rectangle = pygame.Rect(x, WINDOW_HEIGHT - y -100, SHAPE_WIDTH, SHAPE_HEIGHT)
            if c.x == None:
                c.x = x
            if c.y == None:
                c.y = y
            rectangle = pygame.Rect(c.x, c.y, SHAPE_WIDTH, SHAPE_HEIGHT)
            c.rect = rectangle
            #display.blit(c.image, (c.x,c.y))
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], c.x, 800 - c.y + c.offset, c.image, 1, 1, 1)
            
    def swap_old(self, cursor):
        i = self.pos(*cursor)
        b = self.board
        b[i], b[i+1] = b[i+1], b[i]
        self.matches = self.find_matches()

    def swap(self, i, j):
        b = self.board
        b[i], b[j] = b[j], b[i]
        b[i].set_i(i)
        b[j].set_i(j)
        for cell_num in range(len(self.board)):
            self.board[cell_num].set_i(cell_num)
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
    
    def update_matches(self, image, display):
        for match in self.matches:
            global curr_match
            curr_match.append(self.board[match[0]].shape)
            #circle = loadify("images/circle.png")
            for position in match:
                # TODO: Make circle that expands outward (with transparency) with every match
                #circle = pygame.transform.scale(circle, (50, 50))
                self.board[position].image = image
                #for x in range(0, 100):
                    # drawStyleCircle(display, self.board[match[0]].x, self.board[match[0]].y, circle_width)
                    #circle = pygame.transform.scale(circle, (50+x, 50+x))
                    #self.board[position].image = image
                    #pygame.display.update()

    def refill_columns(self):
        for i in range(self.w):
            target = self.size - i - 1
            for pos in range(target, -1, -self.w):
                if self.board[pos].image != self.blank:
                    c = self.board[target]
                    c.image = self.board[pos].image
                    c.offset = (target - pos) // self.w
                    c.y = c.y + c.offset
                    if c.offset == 0:
                        c.set_i(target)
                    target -= self.w
                    yield c
            offset = 1 + (target - pos) // self.w
            for pos in range(target, -1, -self.w):
                c = self.board[pos]
                ran = random.randint(0, 5)
                c.image = self.shapes[ran]
                c.shape = self.type_shape[ran]
                c.set_i(pos)
                c.offset = offset
                yield c

    """
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
    """
    
class Game(object):

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        #self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
        #                                       pygame.RESIZABLE)
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
        pygame.display.set_caption("Creatures of Habbitt v.01")
        self.board = Board(PUZZLE_COLUMNS, PUZZLE_ROWS, background)
        self.font = pygame.font.Font('font/VCR.001.ttf', FONT_SIZE)
        
        self.party_text = []
        self.enemy_text = []
        self.i = 0
        self.spread = []
        for x in range(2, 1102, 100):
            self.spread.append(x)

    def start(self):
        self.board.randomize()
        self.cursor = [0,0]
        self.swap_time = 1

    def quit(self):
        pygame.quit()
        sys.exit()

    def play(self, party, dungeon):
        self.start()
        blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], 0,0, pygame.image.load("images/loading.png").convert_alpha(), 1, 1, 1)

        #gluPerspective(45, (1600/900), 0.1, 50.0)
        #glTranslatef(0.0, 0.0, -5)
        # Set all party member HPs to max before beginning.
        for member in party:
            member.set_chp(member.get_hp())

        self.party = party
        # The list of enemies in this particular dungeon.
        self.enemy = dungeon[0]
        exp = dungeon[1]

        # The turn order for the party.
        party_turns = turn_order(party)
        self.party_turns = party_turns

        # The turn order for the enemy squad.
        self.enemy_turns = turn_order(self.enemy)

        # The index of the current party member.
        party_current = 0

        # The index of the current turn enemy.
        self.enemy_current = 0

        # The enemy whose turn it is.
        self.enemy_active = self.enemy_turns[self.enemy_current][0]

        # Governs the current matches that exist on the board.
        global curr_match
        
        # Determines if there are matches on the board, for randomization.
        matches = True

        # Determines which portrait will flash red when damage is taken.
        self.flash_red = False

        # Timer for enemy attacks.
        timer = pygame.time.get_ticks()

        # Timer for going through text.
        text_timer = pygame.time.get_ticks()

        # The current active party member (object).
        self.player_active = party_turns[party_current][0]

        # Set text to whose turn it is
        self.party_text.append("It is " + self.player_active.get_name() + "'s turn.")
        self.enemy_text.append("It is " + self.enemy_active.get_name() + "'s turn.")

        # These hold the current text to update the status text boxes with.
        self.p_text = self.party_text[0]
        self.e_text = self.enemy_text[0]
        cell_to_drag = None
        cell_dragging = False

        hold = 0
        reset = 0
        turn = 0

        #self.event = threading.Event()
        #enemy_thread = threading.Thread(target=self.enemy_thread, args=())
        #enemy_thread.start()

        #player_thread = threading.Thread(target=self.thread_process_action, args=())
        #player_thread.start()

        #draw_thread = threading.Thread(target=self.draw_gl_scene, args=())
        #draw_thread.start()

        now = "skip"
        self.debug = 0
        debug = self.debug
        self.timing = 0
        self.debug_timer = pygame.time.get_ticks()

        while matches:
            if len(self.board.find_matches()) > 0:
                self.board.randomize()
            else:
                matches = False

        while True:
            if self.timing == 1:
                print("START: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()
            if debug == 1:
                print("Debug: Starting new loop.")
            if now != "skip":
                before = pygame.time.get_ticks() - now
                if turn > 1 and before > 1000:
                    print("Loop time: " + str(before))
            now = pygame.time.get_ticks()
            debug = 0

            self.draw_gl_scene()
            #return_rect = self.draw(self.party, self.enemy, self.player_active, self.p_text, self.e_text, self.flash_red)
            if self.timing == 1:
                print("DRAW: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()
            self.flash_red = None
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
            self.swap_time += dt

            if self.timing == 1:
                print("EVENTS: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()

            if self.timing == 1:
                match_timer = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == KEYUP:
                    self.input(event.key)
                elif event.type == QUIT:
                    #self.event.set()
                    self.quit()

                ## TODO: Current problems with drag matching:
                # - Swaps are not very visible and the board doesn't update smoothly FIX ANIMATIONS
                #
                # Fixed? - Sometimes after swapping you can drag and drop random gems
                # FIXED! - Gems are dropped onto xy coords of mouse not where original gem was
                # Fixed? - When gem is "swapped", original gem does swap with something, but it's not the correct gem
                ##
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.board.busy():
                    #if return_rect.collidepoint(event.pos):
                    #    return "RAN"
                    if event.button == 1:
                       pos = pygame.mouse.get_pos()
                       for cell in self.board.board:            
                            if cell.rect.collidepoint(pos):
                                print("Mouse pos: " + str(pos))
                                print("Rect location: " + str(cell.rect))
                                cell_dragging = True
                                cell_to_drag = cell
                                store_x = cell.x
                                store_y = cell.y
                                mouse_x, mouse_y = event.pos
                                offset_x = cell_to_drag.x - mouse_x
                                offset_y = cell_to_drag.y - mouse_y
                                # current_i = cell_to_drag.get_i()
                                cell_i = cell_to_drag.get_i()
                                possible_matches = get_possible_matches(cell_i)

                elif event.type == pygame.MOUSEBUTTONUP:
                    # print("cell_dragging: " + str(cell_dragging))
                    if event.button == 1: 
                        pos = pygame.mouse.get_pos()
                        if cell_dragging == True: 
                            if pos[0] < 1002:
                                if pos[1] < 902: 
                                    i = find_i(self.spread, pos)
                                    cell = self.board.board[i] 
                                    cell_x = cell.x
                                    cell_y = cell.y
                                    if debug == 1:
                                        print(str(cell_x) + " < " + str(pos[0]) + " < " + str(cell_x+100))
                                        print(str(cell_y) + " < " + str(pos[1]) + " < " + str(cell_y+100))
                                        print(cell_x < pos[0] < cell_x+100 and cell_y < pos[1] < cell_y+100)
                                    if cell_x < pos[0] < cell_x+100 and cell_y < pos[1] < cell_y+100:
                                        # check if in x,y of picked up cell (can't just put tokens wherever)
                                        if debug == 1:
                                            print("Colliding with rect at " + str(pos))
                                        new_i = cell.get_i()
                                        if new_i in possible_matches:
                                            if self.timing == 1:
                                                debug_timing("MATCH_TIMER BEGIN", match_timer)
                                                match_timer = pygame.time.get_ticks()
                                            # check if occupied square is a match
                                            if debug == 1:
                                                print("Cell is in possible matchable x/y coords")
                                            self.swap(new_i, cell_i)
                                            if len(self.board.find_matches()) > 0:
                                                if self.timing == 1:
                                                    print("MATCH FOUND: " + str(self.debug_timer - pygame.time.get_ticks()))
                                                    self.debug_timer = pygame.time.get_ticks()
                                                cell_dragging = False
                                                cell_to_drag.x = cell.x
                                                cell_to_drag.y = cell.y
                                                cell.x = store_x
                                                cell.y = store_y
                                                cell_to_drag = None
                                                reset = 1
                                                debug = 1
                                            else:
                                                self.swap(new_i, cell_i)
                            if reset != 1:
                                cell_dragging = False
                                cell_to_drag.x = store_x
                                cell_to_drag.y = store_y
                                cell_to_drag = None
                                reset = 0
                            reset = 0
                            if self.timing == 1:
                                debug_timing("MATCH_TIMER END", match_timer)
                                match_timer = pygame.time.get_ticks()
                            

                elif event.type == pygame.MOUSEMOTION and not self.board.busy() and cell_dragging:
                    pos = pygame.mouse.get_pos()
                    mouse_y_old = mouse_y
                    mouse_x, mouse_y = pos
                    # Move gems to unoccupied squares as dragged gem passes over them
                    #for cell in self.board.board:            
                    #    if cell.rect.collidepoint(event.pos):
                    #        new_i = cell.i
                    #        cell.i = current_i
                    #        current_i = new_i
                    cell_to_drag.x = mouse_x + offset_x
                    cell_to_drag.y = mouse_y + offset_y

            # If any matches are made by the player   
            """     
            if len(curr_match) > 0:
                for item in curr_match:
                    print(curr_match)
                    state = self.process_action(curr_match[0], party, self.enemy, self.player_active, self.enemy_active, party_turns, self.enemy_turns)
                    curr_match.remove(curr_match[0])
                    if state == "WIN":
                        self.draw(party, self.enemy, self.player_active, "Your party was victorious!", "Your enemies skulk away.", self.flash_red, xp=exp)
                        self.pyg_wait(5)
                        return "WIN"
                if len(curr_match) == 0:
                    if party_current+1 < len(party_turns):
                        party_current += 1
                    else:
                        party_current = 0
                    self.player_active = party_turns[party_current][0]
                    self.party_text.append("It is " + self.player_active.get_name() + "'s turn.")
                    curr_match = []
                    """

            # update the box text with what's going on
            if debug == 1:
                print("Debug: Updating textboxes") 
            self.p_text = self.party_text[0]
            self.e_text = self.enemy_text[0]

            if self.timing == 1:
                print("UPDATE TEXT: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()
            if now - text_timer > 1000:
                if len(self.party_text) > 1:
                    self.party_text.remove(self.p_text)
                    if self.party_text[0][0:5] == "It is" and len(self.party_text) > 1:
                        self.party_text.remove(self.party_text[0])
                    text_timer = pygame.time.get_ticks()
            if now - text_timer < 2000:
                if now - text_timer > 1000 and hold == 0:
                    if len(self.enemy_text) > 1:
                        self.enemy_text.remove(self.e_text)
                        hold = 1
            else:
                if len(self.enemy_text) > 1:
                    self.enemy_text.remove(self.e_text)
                    text_timer = pygame.time.get_ticks()
                    hold = 0

            if debug == 1:
                print("Debug: Checking for 'It is'")
            if self.party_text[0][0:5] == "It is" and len(self.party_text) > 1:
                self.party_text.remove(self.party_text[0])
                text_timer = pygame.time.get_ticks()
            if self.enemy_text[0][0:5] == "It is" and len(self.enemy_text) > 1:
                self.enemy_text.remove(self.enemy_text[0])
                text_timer = pygame.time.get_ticks()
            if debug == 1:
                print("IT IS: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()

            # Tick is where all the lag is
            if self.timing == 1:
                print("TICK START: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()
            self.board.tick(dt, self.display)
            if debug == 1:
                print("Debug: Tick complete.")
            turn += 1
            if self.timing == 1:
                print("TICK END: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()
    
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
            self.board.swap_old(self.cursor)
        elif key == K_d:
            print_rects(self.board)
        elif key == K_r:
            pygame.display.set_mode((1600, 900), pygame.FULLSCREEN)

    def swap(self, i, j):
        self.swap_time = 0.0
        self.board.swap(i, j)

    def draw_thread(self):
        dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
        self.draw(self.party, self.enemy, self.player_active, self.p_text, self.e_text, self.flash_red)
        self.board.tick(dt, self.display)
    
    # TODO
    def update_box(self, text, box):
        pygame.draw.rect(screen, color_passive, box)
        self.gl_text("WHITE", text, WHITE, box, self.font, center=True)

    """def draw_time(self):
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
     """   
    def process_action(self, item, party, enemy, player_active, enemy_active, turns, enemy_turns):
        action = item
        update_text = None
        if enemy_active not in enemy:
            enemy_active = enemy[0]
        if action == "red":
            # do physical damage
            return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
        elif action == "blue":
            # deal magic damage
            att = player_active.get_magic()
            gua = enemy_active.get_maggua()
            dmg = att - gua
            if dmg < 0:
                dmg = 0
            enemy_active.set_chp(enemy_active.get_chp() - dmg)
            update_text = player_active.get_name() + " attacked " + enemy_active.get_name() + " for " + str(dmg) + " damage!"
            self.party_text.append(update_text)
            if enemy_active.get_chp() <= 0:
                update_text = enemy_active.get_name() + " has fallen!"
                self.party_text.append(update_text)
                self.enemy_turns = find_and_remove_from_turn(self.enemy_turns, enemy_active)
                enemy.remove(enemy_active)
                print(self.enemy_turns)
                print(enemy)
                if len(enemy) == 0:
                    update_text = player_active.get_name() + "'s party is victorious!"
                    self.party_text.append(update_text)
                    return "WIN"
        elif action == "green":
            # heal active party member
            heal = player_active.get_magic()
            if player_active.get_hp() < player_active.get_chp() + heal:
                player_active.set_chp(player_active.get_hp())
            else:
                player_active.set_chp(player_active.get_chp() + heal)
            update_text = player_active.get_name() + " healed for " + str(heal) + " damage."
            self.party_text.append(update_text)
        elif action == "orange":
            return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
            # grant support points with this unit
        elif action == "purple":
            return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
            # grant support points with next in line?
        elif action == "yellow":
            return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
            # recover action points
        return update_text
    
    def thread_process_action(self):
        global curr_match
        party_current = 0
        while True:
            if self.event.is_set():
                break
            state = "COMBAT"
            enemy_turns = self.enemy_turns
            player_active = self.player_active
            enemy_active = self.enemy_active
            enemy = self.enemy
            party_turns = self.party_turns
            if len(curr_match) > 0:
                for item in curr_match:
                    print(curr_match)
                    action = item
                    update_text = None
                    if enemy_active not in self.enemy:
                        enemy_active = self.enemy[0]
                    if action == "red":
                        # do physical damage
                        return self.red_attack(self.player_active, enemy_active, self.enemy, enemy_turns)
                    elif action == "blue":
                        # deal magic damage
                        att = player_active.get_magic()
                        gua = enemy_active.get_maggua()
                        dmg = att - gua
                        if dmg < 0:
                            dmg = 0
                        enemy_active.set_chp(enemy_active.get_chp() - dmg)
                        update_text = player_active.get_name() + " attacked " + enemy_active.get_name() + " for " + str(dmg) + " damage!"
                        self.party_text.append(update_text)
                        if enemy_active.get_chp() <= 0:
                            update_text = enemy_active.get_name() + " has fallen!"
                            self.party_text.append(update_text)
                            self.enemy_turns = find_and_remove_from_turn(self.enemy_turns, enemy_active)
                            enemy.remove(enemy_active)
                            print(self.enemy_turns)
                            print(enemy)
                    elif action == "green":
                        # heal active party member
                        heal = player_active.get_magic()
                        if player_active.get_hp() < player_active.get_chp() + heal:
                            player_active.set_chp(player_active.get_hp())
                        else:
                            player_active.set_chp(player_active.get_chp() + heal)
                        update_text = player_active.get_name() + " healed for " + str(heal) + " damage."
                        self.party_text.append(update_text)
                    elif action == "orange":
                        return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
                        # grant support points with this unit
                    elif action == "purple":
                        return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
                        # grant support points with next in line?
                    elif action == "yellow":
                        return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
                        # recover action points
                    if len(enemy) == 0:
                                update_text = player_active.get_name() + "'s party is victorious!"
                                self.party_text.append(update_text)
                                state = "WIN"
                    curr_match.remove(curr_match[0])
                    if state == "WIN":
                        self.draw(party, self.enemy, self.player_active, "Your party was victorious!", "Your enemies skulk away.", flash_red, xp=exp)
                        self.pyg_wait(5)
                        return "WIN"
                if len(curr_match) == 0:
                    if party_current+1 < len(party_turns):
                        party_current += 1
                    else:
                        party_current = 0
                    self.player_active = party_turns[party_current][0]
                    self.party_text.append("It is " + self.player_active.get_name() + "'s turn.")
                    curr_match = []
            
    def red_attack(self, player_active, enemy_active, enemy, enemy_turns):
        att = player_active.get_str()
        gua = enemy_active.get_guard()
        dmg = att - gua
        if dmg < 0:
            dmg = 0
        enemy_active.set_chp(enemy_active.get_chp() - dmg)
        update_text = player_active.get_name() + " attacked " + enemy_active.get_name() + " for " + str(dmg) + " damage!"
        self.party_text.append(update_text)
        if enemy_active.get_chp() <= 0:
            update_text = enemy_active.get_name() + " has fallen!"
            self.party_text.append(update_text)
            enemy_turns = find_and_remove_from_turn(enemy_turns, enemy_active)
            print(enemy)
            enemy.remove(enemy_active)
            print(enemy_turns)
            print(enemy)
            if len(enemy) == 0:
                return "WIN"

    def enemy_attack(self, party, enemy, player_active, enemy_active):
        # enemy goes
        e_attack = enemy_active.get_attack()
        p_defense = player_active.get_defense()
        attacker = enemy_active
        target = player_active
        if e_attack > p_defense:
            dmg = e_attack - p_defense
            target.set_chp(target.get_chp() - (dmg))
            enemy_text = attacker.get_name() + " attacked " + target.get_name() + " for " + str(dmg) + " damage!"
            self.enemy_text.append(enemy_text)
            if target.get_chp() == 0:
                update_text = target.get_name() + " has fallen!"
                self.party_text.append(update_text)
            for member in party:
                if member.get_chp() <= 0:
                    continue
                else:
                    return enemy_text
            return "DEAD"
        
    def pyg_wait(self, seconds):
        last = pygame.time.get_ticks()
        ahead = 0
        while ahead == 0:
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
            self.swap_time += dt
            self.board.tick(dt, self.display)
            pygame.display.update()
            now = pygame.time.get_ticks()
            if now - last > (seconds * 300):
                ahead = 1

    def enemy_thread(self):
        timer = pygame.time.get_ticks()
        while True:
            if self.event.is_set():
                break
            now = pygame.time.get_ticks()
            if now - timer > TIME:
                print("Running enemy_thread")
                enemy_active = self.enemy_turns[self.enemy_current][0]
                target = self.player_active
                while target.get_chp() == 0:
                    i = party.index(target)
                    if i+1 < len(party):
                        target = party[i+1]
                    else:
                        target = party[0]
                state = self.enemy_attack(party, self.enemy, target, enemy_active)
                flash_red = party.index(target)
                if state == "DEAD":
                    self.draw(party, self.enemy, self.player_active, "Your party dead!", "Your party was wiped out...", flash_red)
                    self.pyg_wait(5)
                    return "DEAD"
                
                timer = pygame.time.get_ticks()
                if self.enemy_current+1 < len(self.enemy_turns)-1:
                    self.enemy_current += 1
                else:
                    self.enemy_current = 0

                self.enemy_text.append("It is " + enemy_active.get_name() + "'s turn.")
                print("Enemy thread finished running.")

    def draw_gl_scene(self, xp=None, update_text=None):
        #glLoadIdentity()
        #glTranslatef(0.0,0.0,-10.0)

        party = self.party
        enemy_current = self.enemy_current
        enemy = self.enemy
        flash_red = self.flash_red

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

        """screen.blit(background, (width+self.i,0))
        screen.blit(background, (self.i, 0))
        if (self.i == -width):
            screen.blit(background, (width+self.i, 0))
            self.i=0
        self.i-=1
        self.board.draw(self.display)
        color_return = BLACK"""

        background = pygame.image.load("images\cave.png").convert_alpha()
        blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width+self.i, 0, background, 1, 1, 1)
        blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], self.i, 0, background, 1, 1, 1)
        if (self.i == -width):
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width+self.i, 0, background, 1, 1, 1)
            self.i=0
        self.i-=1
        self.board.draw(self.display)

        #print("Drawing board")
        self.board.draw(self.display)
        #print("Finished drawing board")

        self.shape_color("BLACK")
        # party 1
        self.gl_text(color_0, .4, 1, .9, 1, party[0].get_name(), 0.88, 1.045)
        self.gl_text(color_0,.4, 1, .8, .9, "HP: " + str(party[0].get_chp()) + "/" + str(party[0].get_hp()), 0.885, 1.045)
        # party 2
        self.gl_text(color_1, .4, 1, .7, .8, party[1].get_name(), 0.86, 1.04)
        self.gl_text(color_1,.4, 1, .6, .7, "HP: " + str(party[1].get_chp()) + "/" + str(party[1].get_hp()), 0.885, 1.045)
        # party 3
        self.gl_text(color_2, .4, 1, .5, .6, party[2].get_name(), 0.86, 1.045)
        self.gl_text(color_2,.4, 1, .4, .5, "HP: " + str(party[2].get_chp()) + "/" + str(party[2].get_hp()), 0.885, 1.045)
        # party 4
        self.gl_text(color_3, .4, 1, .3, .4, party[3].get_name(), 0.882, 1.06)
        self.gl_text(color_3,.4, 1, .2, .3, "HP: " + str(party[3].get_chp()) + "/" + str(party[3].get_hp()), 0.88, 1.07)
        # enemy 1
        self.gl_text("BLACK", .64, 1, -.7, -.8, enemy[enemy_current].get_name(), .94, .9)
        self.gl_text("BLACK", .64, 1, -.8, -.9, "HP: " + str(enemy[enemy_current].get_chp()) + "/" + str(enemy[enemy_current].get_hp()), 0.965, 0.9)
        # return (DOESN'T WORK)
        self.gl_text("BLACK", .64, 1, -.9, -1, "RETURN", .94, .9)

        glBegin(GL_QUADS)
        #party_port_1 = self.rect_ogl("GREEN", .27, .4, .8, 1)
        #party_port_2 = self.rect_ogl("RED", .27, .4, .6, .8)
        #party_port_3 = self.rect_ogl("BLUE", .27, .4, .4, .6)
        #party_port_4 = self.rect_ogl("GREEN", .27, .4, .2, .4)

        # enemies
        enemy_port_1 = self.rect_ogl("GREEN", .52, .64, -.9, -.7)
        enemy_port_2 = self.rect_ogl("RED", .4, .52, -.9, -.7)
        enemy_port_3 = self.rect_ogl("BLUE", .28, .4, -.9, -.7)

        # return button
        return_button = self.rect_ogl("BLACK", .28, 1, -.9, -1)

        text_enemy = self.rect_ogl("BLACK", .28, 1, -.7, -.45)
        text_party = self.rect_ogl("BLACK", .28, 1, -.45, -.2)

        ability_1 = self.rect_ogl("RED", .28, .64, 0, .2)
        ability_2 = self.rect_ogl("BLUE", .64, 1, 0, .2)
        ability_3 = self.rect_ogl("GREEN", .28, .64, -.2, 0)
        ability_4 = self.rect_ogl("PINK", .64, 1, -.2, 0)

        glEnd()

        # draw highlight rectangles

        # ability rectangles for clicking
        ability_1_rect = pygame.Rect(width-600,height-500,300,75)
        ability_2_rect = pygame.Rect(width-300,height-500,300,75)
        ability_3_rect = pygame.Rect(width-600,height-425,300,75)
        ability_4_rect = pygame.Rect(width-300,height-425,300,75)
        
        # blit images - NEED TO SHRINK PORTRAITS TO 100x100
        blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-580,height-90, pygame.image.load(get_portrait_2(party[0].get_name())).convert_alpha(), 1, 1, 1)
        blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-570,height-180, pygame.image.load(get_portrait_2(party[1].get_name())).convert_alpha(), 1, 1, 1)
        blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-570,height-270, pygame.image.load(get_portrait_2(party[2].get_name())).convert_alpha(), 1, 1, 1)
        blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-570,height-360, pygame.image.load(get_portrait_2(party[3].get_name())).convert_alpha(), 1, 1, 1)

        if len(enemy) > 2:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-580,height-860, get_portrait(enemy[2].get_name()).convert_alpha(), 1, 1, 1)
            #print("Enemy 2 X: " + str(width-580) + ", Y: " + str(height-860))
        if len(enemy) > 1:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-480,height-860, get_portrait(enemy[1].get_name()).convert_alpha(), 1, 1, 1)
        if len(enemy) > 0:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-380,height-860, get_portrait(enemy[0].get_name()).convert_alpha(), 1, 1, 1)

        self.update_box(self.p_text, party_box)
        self.update_box(self.e_text, enemy_box)

        pygame.display.flip()

        return return_button

    def gl_text(self, color, left, right, bot, top, text, x_adjust, y_adjust):
        glBegin(GL_QUADS)
        self.rect_ogl(color, left, right, bot, top)
        glEnd()
        self.drawText(left, top, text, x_adjust, y_adjust)

    def shape_color(self, color):
        if color == "BLUE":
            glColor3f(0.0, 0.0, 1.0)
        if color == "RED":
            glColor3f(1.0, 0.0, 0.0)
        if color == "GREEN":
            glColor3f(0.0, 1.0, 0.0)
        if color == "BLACK":
            glColor3f(0.0, 0.0, 0.0)
        if color == "PINK":
            glColor3f(222.0, 49.0, 99.0)

    def rect_ogl(self, color, left, right, bot, top):
        self.shape_color(color)
        vertices = np.array([
            [left, bot],
            [left, top],
            [right, top],
            [right, bot]
        ], dtype=np.float32)
        for vertex_pair in vertices:
            glVertex2f(vertex_pair[0], vertex_pair[1])
            if self.debug == 1:
                print("Drew triangle at vertices " + str(vertex_pair[0]) + " and " + str(vertex_pair[1]) + ".")

    def drawText(self, x, y, text, x_adjust, y_adjust):                                                
        textSurface = self.font.render(text, True, (255, 255, 255, 255), (0, 0, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        new_x = ((x+1)/2)*1600/x_adjust
        new_y = ((y+1)/2)*900/y_adjust
        glWindowPos2d(new_x, new_y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

if __name__ == '__main__':
    party = fill_party()
    state = Game().play(party, get_dungeon("cave"))
    print("Your final result was: " + state)