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

screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
pygame.display.set_caption("Creatures of Habbitt v.01")

color_passive = pygame.Color('black')

background = retrieve_background("cave")

PUZZLE_COLUMNS = 10
PUZZLE_ROWS = 9
SHAPE_WIDTH = 100
SHAPE_HEIGHT = 100
MARGIN = 2

# Amount of time before enemy makes a decision
TIME = 5000

RED = loadify("images/tabs/red_gem_new.png")
BLUE = loadify("images/tabs/blue_gem_new.png")
PURPLE = loadify("images/tabs/purple_gem_new.png")
GREEN = loadify("images/tabs/green_gem_new.png")
ORANGE = loadify("images/tabs/orange_gem_new.png")
PINK = loadify("images/tabs/pink_gem_new.png")
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
FONT_SIZE = 36
TEXT_OFFSET = MARGIN + 5
SHAPES_LIST = [RED, BLUE, PURPLE, GREEN, ORANGE, PINK]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MINIMUM_MATCH = 3

FPS = 120
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
        shapes = 'red blue purple green orange pink'
        self.shapes = []
        self.type_shape = []
        for shape in shapes.split():
            to_add = loadify('images/tabs/{}_gem_new.png'.format(shape))
            to_add = pygame.transform.scale(to_add, (100, 100))
            self.shapes.append(to_add)
            self.type_shape.append(shape)
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
        self.wait = 0
        self.boom_played = 0
        self.boom_sound = pygame.mixer.Sound("audio/sfx/boom.wav")
        global in_curr_match
        in_curr_match = []
        

    def randomize(self):
        """
        replace whole board
        """
        for i in range(self.size):
            c = random.randint(0, 5)
            self.board[i] = Cell(self.shapes[c], self.type_shape[self.shapes.index(self.shapes[c])], i)
        #row = self.board
        #print("["+row[0].shape+"]["+row[1].shape+"]["+row[2].shape+"]["+row[3].shape+"]["+row[4].shape+"]["+row[5].shape+"]["+row[6].shape+"]["+row[7].shape+"]["+row[8].shape+"]["+row[9].shape+"]")
        #print("["+row[10].shape+"]["+row[11].shape+"]["+row[12].shape+"]["+row[13].shape+"]["+row[14].shape+"]["+row[15].shape+"]["+row[16].shape+"]["+row[17].shape+"]["+row[18].shape+"]["+row[19].shape+"]")
        #print("["+row[20].shape+"]["+row[21].shape+"]["+row[22].shape+"]["+row[23].shape+"]["+row[24].shape+"]["+row[25].shape+"]["+row[26].shape+"]["+row[27].shape+"]["+row[28].shape+"]["+row[29].shape+"]")

    def pos(self, i, j):
        assert(0 <= i < self.w)
        assert(0 <= j < self.h)
        return j * self.w + i
    
    def busy(self):
        if self.wait > 0 and not (self.refill or self.matches):
            if self.wait == 1:
                print("Wait diminished")
            self.wait -= 1
            return True
        return self.refill or self.matches
    
    def tick(self, dt, display):
        if self.refill or self.matches:
            self.wait = 1000
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
            self.refill = list(self.refill_columns())
        self.explosion_time = 0
        self.matches = self.find_matches()

    def draw(self, display):
        #display.blit(self.background, (0,0))
        for i, c in enumerate(self.board):
            x = MARGIN + SHAPE_WIDTH * (i % self.w)
            y = MARGIN + SHAPE_HEIGHT * (i // self.w - c.offset)
            #rectangle = pygame.Rect(x, WINDOW_HEIGHT - y -100, SHAPE_WIDTH, SHAPE_HEIGHT)
            if c.x == None or self.busy():
                c.x = x
            if c.y == None or self.busy():
                c.y = y
            rectangle = pygame.Rect(x, y, SHAPE_WIDTH, SHAPE_HEIGHT)
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
        match_list = list(matches())
        self.send_matches_to_game(match_list)
        return match_list
    
    def send_matches_to_game(self, match_list):
        global curr_match
        global in_curr_match
        current_matches = match_list
        if len(current_matches) > 0:
            for x in current_matches:
                if x[0] not in in_curr_match:
                    curr_match.append(self.board[x[0]].shape)
                in_curr_match.append(x[0])
    
    def update_matches(self, image, display):
        for match in self.matches:
            #circle = loadify("images/circle.png")
            for position in match:
                # TODO: Make circle that expands outward (with transparency) with every match
                #circle = pygame.transform.scale(circle, (50, 50))
                self.board[position].image = image
                self.board[position].shape = None
                if self.boom_played == 0:
                    self.boom_sound.play()
                    self.boom_played = 1
                #for x in range(0, 100):
                    # drawStyleCircle(display, self.board[match[0]].x, self.board[match[0]].y, circle_width)
                    #circle = pygame.transform.scale(circle, (50+x, 50+x))
                    #self.board[position].image = image
                    #pygame.display.update()

    def refill_columns(self):
        self.boom_played = 0
        for i in range(self.w):
            target = self.size - i - 1
            for pos in range(target, -1, -self.w):
                if self.board[pos].image != self.blank:
                    c = self.board[target]
                    c.image = self.board[pos].image
                    c.shape = self.type_shape[self.shapes.index(c.image)]
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
                c.shape = self.type_shape[self.shapes.index(c.image)]
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
    
class MatchGame(object):

    def __init__(self, screen):
        #pygame.init()
        self.clock = pygame.time.Clock()
        #self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
        #                                       pygame.RESIZABLE)
        self.display = screen
        self.board = Board(PUZZLE_COLUMNS, PUZZLE_ROWS, background)
        self.font = pygame.font.Font('font/VCR.001.ttf', FONT_SIZE)
        self.party_text = []
        self.enemy_text = []
        self.i = 0
        self.spread = []
        self.level = 0
        for x in range(2, 1102, 100):
            self.spread.append(x)
        self.fullscreen = 0
        self.removed = 0
        self.counter_x = 0
        self.counter_y = 0
        self.fade_out = 0
        self.fade_image = pygame.image.load("images/circlefade.png")
        self.end_fade = 0
        self.start_fade = 0
        self.state = "PLAY"
        self.return_to_crawl = 0
        self.enemy_active = None
        self.mc_name = None

        # the length of the currently playing victory line
        self.talking_length = 0
        self.talking_timer = 0
        self.talking = 0

        self.debug = 0
 

    def start(self):
        self.board.randomize()
        self.cursor = [0,0]
        self.swap_time = 1

    def quit(self):
        pygame.quit()
        sys.exit()

    def play(self, party, enemies, display=screen, need_fade=0):
        self.start()
        self.end_fade = need_fade
        if display != screen:
            self.display = display
        self.mc_name = party[0].get_name()

        #gluPerspective(45, (1600/900), 0.1, 50.0)
        #glTranslatef(0.0, 0.0, -5)
        # Set all party member HPs to max before beginning.
        for member in party:
            member.set_chp(member.get_hp())

        self.party = party
        # The list of enemies in this particular dungeon.
        if self.debug == 1:
            print(enemies)
        self.enemy = enemies

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
        if len(self.enemy_turns) > 0:
            self.enemy_active = self.enemy_turns[self.enemy_current][0]

        # Governs the current matches that exist on the board.
        global curr_match
        
        # Determines which portrait will flash red when damage is taken.
        self.flash_red = False

        # Timer for enemy attacks.
        timer = pygame.time.get_ticks()

        # Timer for going through text.
        text_timer = pygame.time.get_ticks()

        # The current active party member (object).
        self.player_active = party_turns[party_current][0]

        # Set text to whose turn it is
        if self.player_active != None:
            self.party_text.append("It is " + self.player_active.get_name() + "'s turn.")
        if self.enemy_active != None:
            self.enemy_text.append("It is " + self.enemy_active.get_name() + "'s turn.")

        # These hold the current text to update the status text boxes with.
        if len(self.party_text) > 0:
            self.p_text = self.party_text[0]
        if len(self.enemy_text) > 0:
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
        wait_timer = 0

        # Determines if there are matches on the board, for randomization.
        global matches
        matches = True

        character_swap_timing = 0
        time_to_swap = 0
        character_swap_timer = None

        in_curr_match_timer = 0
        check = None

        while matches:
            if len(self.board.find_matches()) > 0:
                self.board.randomize()
            else:
                matches = False

        curr_character = party_current

        while True:
            if curr_character != party_current:
                print("Character swapped")
                curr_character = party_current
            if check != self.p_text:
                print(self.party_text)
                check = self.p_text
            party_turns = turn_order(self.party)
            next_turn = 0
            if self.enemy_active not in self.enemy and len(self.enemy) > 0:
                self.enemy_active = self.enemy[0]
                self.e_text = "It is " + self.enemy_active.get_name() + "'s turn."
            if self.debug == 1:
                print("START: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()
            if self.debug == 1:
                print("Debug: Starting new loop.")
            if now != "skip":
                before = pygame.time.get_ticks() - now
                if turn > 1 and before > 1000 and self.debug==1:
                    print("Loop time: " + str(before))
            now = pygame.time.get_ticks()
            self.debug = 0

            if self.state == "WIN":
                self.talking_length = self.play_victory_line() * 1000
                self.talking_timer = pygame.time.get_ticks()
                self.talking = 2
                self.party_text = ["Your party was victorious!"]
                self.p_text = self.party_text[0]
                xp = 0
                for foe in enemies:
                    print(foe.get_xp())
                    xp += foe.get_xp()
                xp_string = "Your party receives XP experience points!"
                replaced_xp = xp_string.replace("XP", str(xp))
                self.enemy_text = [replaced_xp]
                self.e_text = self.enemy_text[0]
                wait_timer = pygame.time.get_ticks()
                self.state = "WAITING"

            if self.state == "WAITING" and now - wait_timer > 4000:
                self.start_fade = 1
                self.counter_x = 0
                self.state = "WAITING 2"

            self.draw_gl_scene(party_current)

            if self.return_to_crawl == 1:
                return "WIN"
            #return_rect = self.draw(self.party, self.enemy, self.player_active, self.p_text, self.e_text, self.flash_red)
            if self.debug == 1:
                print("DRAW: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()
            self.flash_red = False
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
            self.swap_time += dt

            if self.debug == 1:
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
                # Fixed - Sometimes after swapping you can drag and drop random gems
                # FIXED! - Gems are dropped onto xy coords of mouse not where original gem was
                # Fixed - When gem is "swapped", original gem does swap with something, but it's not the correct gem
                ##
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.board.busy() and self.state == "PLAY":
                    #if return_rect.collidepoint(event.pos):
                    #    return "RAN"
                    if event.button == 1:
                       pos = pygame.mouse.get_pos()
                       for cell in self.board.board:            
                            if cell.rect.collidepoint(pos):
                                if self.debug == 1:
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
                                    if self.debug == 1:
                                        print(str(cell_x) + " < " + str(pos[0]) + " < " + str(cell_x+100))
                                        print(str(cell_y) + " < " + str(pos[1]) + " < " + str(cell_y+100))
                                        print(cell_x < pos[0] < cell_x+100 and cell_y < pos[1] < cell_y+100)
                                    if cell_x < pos[0] < cell_x+100 and cell_y < pos[1] < cell_y+100:
                                        # check if in x,y of picked up cell (can't just put tokens wherever)
                                        if self.debug == 1:
                                            print("Colliding with rect at " + str(pos))
                                        new_i = cell.get_i()
                                        if new_i in possible_matches:
                                            if self.timing == 1:
                                                debug_timing("MATCH_TIMER BEGIN", match_timer)
                                                match_timer = pygame.time.get_ticks()
                                            # check if occupied square is a match
                                            if self.debug == 1:
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
            
            if curr_match != [] and self.debug == 1:
                print(curr_match)
            # If any matches are made by the player  
            # TODO: Make it not change party members in the middle of a combo 
            if self.state == "PLAY":   
                while len(curr_match) > 0:
                    character_swap_timing = 1
                    for item in curr_match:
                        if self.debug == 1:
                            print("Debug: curr_match: " + curr_match[0])
                        if len(self.party_text) > 1:
                            self.party_text.remove(self.party_text[0])
                        in_curr_match_timer = pygame.time.get_ticks()
                        result = self.process_action(curr_match[0], party, self.enemy, self.player_active, self.enemy_active, party_turns, self.enemy_turns)
                        curr_match.remove(curr_match[0])
                        if result == "WIN":
                            self.state = "WIN"
                
                if len(curr_match) == 0 and now - in_curr_match_timer > 1000:
                    global in_curr_match
                    in_curr_match = []
                        
                if not self.board.busy() and character_swap_timing == 1:
                    character_swap_timer = pygame.time.get_ticks()
                    time_to_swap = 1
                    character_swap_timing = 0

                # if matches have been made previously and the board isn't processing them
                if character_swap_timer != None and self.board.wait == 0:
                    if (pygame.time.get_ticks() - character_swap_timer > 3000 and time_to_swap == 1) or self.removed != 0:
                        if self.debug == 1:
                            print("Changing party member")
                        if party_current+1 < len(party_turns):
                            party_current += 1
                        else:
                            party_current = 0
                        self.player_active = party_turns[party_current][0]
                        self.party_text.append("It is " + self.player_active.get_name() + "'s turn.")
                        curr_match = []
                        character_swap_timer = None
                        time_to_swap = 0
                        self.removed = 0

                if now - timer > 5000:
                    flash = self.enemy_attack(self.enemy, self.player_active, self.enemy_active)
                    if flash != 0:
                        self.flash_red = self.party.index(self.player_active)
                    timer = now
                    self.e_text = self.enemy_text[0]
        
                # update the box text with what's going on
                if self.debug == 1:
                    print("Debug: Updating textboxes")
                if len(self.party_text) > 0: 
                    self.p_text = self.party_text[0]
                else:
                    self.p_text = ""
            
                if self.debug == 1:
                    print("UPDATE TEXT: " + str(self.debug_timer - pygame.time.get_ticks()))
                    self.debug_timer = pygame.time.get_ticks()
                if now - text_timer > 1000:
                    if self.party_text[0][0:5] == "It is" and len(self.party_text) > 1:
                        self.party_text.remove(self.party_text[0])
                    text_timer = pygame.time.get_ticks()
                if now - text_timer < 2000:
                    if now - text_timer > 1000 and hold == 0:
                        if len(self.enemy_text) > 1:
                            self.enemy_text.remove(self.enemy_text[0])
                            self.e_text = self.enemy_text[0]
                            hold = 1
                else:
                    if len(self.enemy_text) > 1:
                        self.enemy_text.remove(self.e_text)
                        self.e_text = self.enemy_text[0]
                        text_timer = pygame.time.get_ticks()
                        hold = 0

                if self.debug == 1:
                    print("Debug: Checking for 'It is'")
                if len(self.party_text) > 0:
                    if self.party_text[0][0:5] == "It is" and len(self.party_text) > 1:
                        self.party_text.remove(self.party_text[0])
                        text_timer = pygame.time.get_ticks()

                if len(self.enemy_text) > 0:    
                    if self.enemy_text[0][0:5] == "It is" and len(self.enemy_text) > 1:
                        self.enemy_text.remove(self.enemy_text[0])
                        self.e_text = self.enemy_text[0]
                        text_timer = pygame.time.get_ticks()

                if self.debug == 1:
                    print("IT IS: " + str(self.debug_timer - pygame.time.get_ticks()))
                    self.debug_timer = pygame.time.get_ticks()

                if pygame.time.get_ticks() - text_timer > 2000:
                    if len(self.party_text) == 1:
                        if self.party_text[0][0:5] != "It is" and len(self.party_text) > 1:
                            self.party_text = ["It is " + party_turns[party_current][0].get_name() + "'s turn."]

            if self.timing == 1:
                print("TICK START: " + str(self.debug_timer - pygame.time.get_ticks()))
                self.debug_timer = pygame.time.get_ticks()

            self.board.tick(dt, self.display)

            if self.debug == 1:
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
            if self.fullscreen == 0:
                self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                              pygame.DOUBLEBUF|pygame.OPENGL|pygame.FULLSCREEN)
                self.fullscreen = 1
            else:
                self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
                self.fullscreen = 0
        elif key == K_t:
            to_print = []
            for x in range(len(self.board.board)+1):
                if len(to_print) < 10:
                    to_print.append(self.board.board[x].shape)
                elif len(to_print) >= 10 or x+1 >= 89:
                    print(to_print)
                    to_print = []
                    if x+1 < 90:
                        to_print.append(self.board.board[x].shape)

    def swap(self, i, j):
        self.swap_time = 0.0
        self.board.swap(i, j)
    
    def update_box(self):
        gl_text_wrap(self.font, self.display, "BLACK", .28, 1, -.7, -.45, self.e_text, .98, 2.1, self.level)
        gl_text_wrap(self.font, self.display, "BLACK", .28, 1, -.2, -.45, self.p_text, .98, 1.4, self.level)
        # color left right bot top text x_adjust y_adjust

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
            if len(enemy) == 0:
                return
            else:
                enemy_active = enemy[0]
        if action == "red":
            # do physical damage
            return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
        elif action == "purple":
            # deal magic damage
            return self.purple_attack(player_active, enemy_active, enemy)
        elif action == "green":
            # heal active party member
            return self.green_heal(player_active, party)
        elif action == "orange":
            return self.orange_buff(player_active, party)
            # should grant support points
        elif action == "blue":
            return self.blue_debuff(player_active, enemy)
            # should buff the user
        elif action == "pink":
            return self.pink_support(player_active, party)
            # should debuff the enemy
        return update_text
          
    def red_attack(self, player_active, enemy_active, enemy, enemy_turns):
        att = player_active.get_physical_attack()
        gua = enemy_active.get_guard()
        dmg = att - gua
        if dmg < 0:
            dmg = 0
        enemy_active.set_chp(enemy_active.get_chp() - dmg)
        update_text = player_active.get_name() + " physically attacked " + enemy_active.get_name() + " for " + str(dmg) + " damage!"
        self.party_text.append(update_text)
        if enemy_active.get_chp() <= 0:
            update_text = enemy_active.get_name() + " has fallen!"
            self.party_text.append(update_text)
            enemy_turns = find_and_remove_from_turn(enemy_turns, enemy_active)
            enemy.remove(enemy_active)
            if len(enemy) == 0:
                return "WIN"
            
    def pink_support(self, player_active, party):
        sup_num = 10 * player_active.get_chutzpah()
        choices = []
        name = player_active.get_name()
        for player in party:
            if player.get_name() != name:
                choices.append(player)
        target = random.choice(choices)
        update_text = player_active.get_name() + " received " + str(sup_num) + " support points with " + target.get_name() + "!"
        target.add_support_points(player_active.get_name(), sup_num, self.mc_name)
        player_active.add_support_points(target.get_name(), sup_num, self.mc_name)
        self.party_text.append(update_text) 

    def blue_debuff(self, player_active, enemy):
        debuff_num = 10
        debuff_type = "Attack"
        name = player_active.get_name()
        target = random.choice(enemy)
        update_text = name + " debuffed " + target.get_name() + " with -" + str(debuff_num) + " " + debuff_type + "!"
        self.party_text.append(update_text)
    
    def orange_buff(self, player_active, party):
        buff_num = 10
        buff_type = "Attack"
        target = random.choice(party)
        update_text = player_active.get_name() + " buffed " + target.get_name() + " with +" + str(buff_num) + " " + buff_type + "!"
        self.party_text.append(update_text)

    def purple_attack(self, player_active, enemy_active, enemy):
        att = player_active.get_magic_attack()
        gua = enemy_active.get_magical_guard()
        dmg = att - gua
        if dmg < 0:
            dmg = 0
        enemy_active.set_chp(enemy_active.get_chp() - dmg)
        update_text = player_active.get_name() + " magically attacked " + enemy_active.get_name() + " for " + str(dmg) + " damage!"
        self.party_text.append(update_text)
        if enemy_active.get_chp() <= 0:
            update_text = enemy_active.get_name() + " has fallen!"
            self.enemy_text.append(update_text)
            self.enemy_turns = find_and_remove_from_turn(self.enemy_turns, enemy_active)
            enemy.remove(enemy_active)
            if self.debug == 1:
                print(self.enemy_turns)
                print(enemy)
            if len(enemy) == 0:
                update_text = player_active.get_name() + "'s party is victorious!"
                self.party_text.append(update_text)
                return "WIN"
            
    def green_heal(self, player_active, party):
        heal = player_active.get_healing()
        if player_active.get_chp() >= player_active.get_hp():
            heal_target = None
            for player in party:
                if player.get_chp() < player.get_hp():
                    if player.get_chp() + heal > player.get_hp():
                        player.set_chp(player.get_hp())
                    else:
                        player.set_chp(player.get_chp() + heal)
                    heal_target = player
                    break
            if heal_target != None:
                update_text = player_active.get_name() + " healed " + heal_target.get_name() + " for " + str(heal) + " points."
            else:
                update_text = player_active.get_name() + " tried to heal, but the party was at full health already."
        elif player_active.get_hp() < player_active.get_chp() + heal:
            player_active.set_chp(player_active.get_hp())
            update_text = player_active.get_name() + " healed for " + str(heal) + " points."
        else:
            player_active.set_chp(player_active.get_chp() + heal)
            update_text = player_active.get_name() + " healed for " + str(heal) + " points."
        self.party_text.append(update_text)

    def enemy_attack(self, enemy, player_active, enemy_active):
        # enemy goes
        party = self.party
        e_attack = enemy_active.get_attack()
        p_defense = player_active.get_physical_guard()
        attacker = enemy_active
        target = player_active
        if e_attack > p_defense:
            dmg = e_attack - p_defense
        else:
            dmg = 1
        target.set_chp(target.get_chp() - (dmg))
        enemy_text = attacker.get_name() + " attacked " + target.get_name() + " for " + str(dmg) + " damage!"
        self.enemy_text.append(enemy_text)
        if target.get_chp() == 0:
            update_text = target.get_name() + " has fallen!"
            self.party_text.append(update_text)
            self.party.remove(target)
            self.removed = target
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
                self.state = self.enemy_attack(party, self.enemy, target, enemy_active)
                flash_red = party.index(target)
                if self.state == "DEAD":
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

    def draw_gl_scene(self, party_current, xp=None, update_text=None):
        #glLoadIdentity()
        #glTranslatef(0.0,0.0,-10.0)

        party = self.party
        enemy_current = self.enemy_current
        enemy = self.enemy

        color_black = "BLACK"
        color_0, color_1, color_2, color_3 = color_black, color_black, color_black, color_black

        # draw highlight rectangles
        if self.party_turns[party_current][0] == self.party[0]:
            color_0 = "BLUE"
        else: color_0 = color_black
        if len(self.party) > 1:
            if self.party_turns[party_current][0] == self.party[1]:
                color_1 = "BLUE"
            else: color_1 = color_black
        if len(self.party) > 2:
            if self.party_turns[party_current][0] == self.party[2]:
                color_2 = "BLUE"
            else: color_2 = color_black
        if len(self.party) > 3:
            if self.party_turns[party_current][0] == self.party[3]:
                color_3 = "BLUE"
            else: color_3 = color_black

        if self.flash_red != False:
            if self.flash_red == 0:
                color_0 = "RED"
            if self.flash_red == 1:
                color_1 = "RED"
            if self.flash_red == 2:
                color_2 = "RED"
            if self.flash_red == 3:
                color_3 = "RED"

        """screen.blit(background, (width+self.i,0))
        screen.blit(background, (self.i, 0))
        if (self.i == -width):
            screen.blit(background, (width+self.i, 0))
            self.i=0
        self.i-=1
        self.board.draw(self.display)
        color_return = BLACK"""

        self.i = blit_bg(self.i)
        self.board.draw(self.display)

        shape_color("BLACK")
            # party 1
        if len(party) > 0:
            gl_text(self.font, color_0, 1, .4, .9, 1, party[0].get_name(), .99, .99)
            gl_text(self.font, color_0, 1, .4, .8, .9, "HP: " + str(party[0].get_chp()) + "/" + str(party[0].get_hp()), .99, .99)
            # party 2
        if len(party) > 1:
            gl_text(self.font, color_1, 1, .4, .7, .8, party[1].get_name(), .99, .99)
            gl_text(self.font, color_1, 1, .4, .6, .7, "HP: " + str(party[1].get_chp()) + "/" + str(party[1].get_hp()), .99, .99)
            # party 3
        if len(party) > 2:
            gl_text(self.font, color_2, 1, .4, .5, .6, party[2].get_name(), .99, .99)
            gl_text(self.font, color_2, 1, .4, .4, .5, "HP: " + str(party[2].get_chp()) + "/" + str(party[2].get_hp()), .99, .99)
            # party 4
        if len(party) > 3:
            gl_text(self.font, color_3, 1, .4, .3, .4, party[3].get_name(), .99, .99)
            gl_text(self.font, color_3, 1, .4, .2, .3, "HP: " + str(party[3].get_chp()) + "/" + str(party[3].get_hp()), .99, .99)
            # enemy 1
        if len(enemy) > 0:
            gl_text(self.font, "BLACK", 1, .64, -.7, -.9, enemy[0].get_name(), .995, 1.4)
            if enemy[0].get_hp() > 999:
                gl_text(self.font, "BLACK", 1, .64, -.8, -9, "HP: " + str(enemy[0].get_chp()), .995, 2)  
            else:
                gl_text(self.font, "BLACK", 1, .64, -.8, -9, "HP: " + str(enemy[0].get_chp()) + "/" + str(enemy[0].get_hp()), .995, 2)
        else:
            gl_text(self.font, "BLACK", 1, .28, -.7, -.9, "No Enemy Remains", .995, 1.4)
            gl_text(self.font, "BLACK", 1, .28, -.8, -9, "HP: 0/0", .995, 2)
        # return (DOESN'T WORK)
        gl_text(self.font, "BLACK", .28, 1, -.9, -1, "RETURN", 1.3, 6)

        glBegin(GL_QUADS)
        #party_port_1 = rect_ogl("GREEN", .27, .4, .8, 1)
        #party_port_2 = rect_ogl("RED", .27, .4, .6, .8)
        #party_port_3 = rect_ogl("BLUE", .27, .4, .4, .6)
        #party_port_4 = rect_ogl("GREEN", .27, .4, .2, .4)

        # enemies
        #enemy_port_1 = rect_ogl("GREEN", .52, .64, -.9, -.7)
        #enemy_port_2 = rect_ogl("RED", .4, .52, -.9, -.7)
        #enemy_port_3 = rect_ogl("BLUE", .28, .4, -.9, -.7)

        # return button
        #return_button = rect_ogl("BLACK", .28, 1, -.9, -1)

        #text_enemy = rect_ogl("BLACK", .28, 1, -.7, -.45)
        #text_party = rect_ogl("BLACK", .28, 1, -.45, -.2)

        #ability_1 = rect_ogl("RED", .28, .64, 0, .2)
        #ability_2 = rect_ogl("BLUE", .64, 1, 0, .2)
        #ability_3 = rect_ogl("GREEN", .28, .64, -.2, 0)
        #ability_4 = rect_ogl("PINK", .64, 1, -.2, 0)

        glEnd()

        # ability rectangles for clicking
        ability_1_rect = pygame.Rect(width-600,height-500,300,75)
        ability_2_rect = pygame.Rect(width-300,height-500,300,75)
        ability_3_rect = pygame.Rect(width-600,height-425,300,75)
        ability_4_rect = pygame.Rect(width-300,height-425,300,75)
        
        # blit images - NEED TO SHRINK PORTRAITS TO 100x100
        if len(party) > 0:    
            #if self.talking == 1:
                #blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-580,height-90, self.current_talking_portrait(), 1, 1, 1)
            #else:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-580,height-90, party[0].get_portrait().convert_alpha(), 1, 1, 1)
        if len(party) > 1:    
            #if self.talking == 2:
            #    blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-580,height-90, self.current_talking_portrait("nsteen"), 1, 1, 1)
            #else:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-570,height-180, party[1].get_portrait().convert_alpha(), 1, 1, 1)
        if len(party) > 2:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-570,height-270, party[2].get_portrait().convert_alpha(), 1, 1, 1)
        if len(party) > 3:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-570,height-360, party[3].get_portrait().convert_alpha(), 1, 1, 1)

        if len(enemy) > 0:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-386,height-857, get_portrait(enemy[0].get_name()).convert_alpha(), 1, 1, 1)
        if len(enemy) > 1:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-482,height-857, get_portrait(enemy[1].get_name()).convert_alpha(), 1, 1, 1)
        if len(enemy) > 2:
            blit_image([WINDOW_WIDTH, WINDOW_HEIGHT], width-578,height-857, get_portrait(enemy[2].get_name()).convert_alpha(), 1, 1, 1)   

        self.update_box()     

        if self.end_fade == 1:
            blit_image([width, height], 0-self.counter_x, 0, pygame.image.load("images/black_pass.png").convert_alpha(), 1, 1, 1)
            self.counter_x += 100
            if self.counter_x >= 1700:
                self.end_fade = 0

        if self.start_fade == 1:
            blit_image([width, height], width-self.counter_x, 0, pygame.image.load("images/black_pass.png").convert_alpha(), 1, 1, 1)
            if self.counter_x < 200:
                self.counter_x += 50
            elif self.counter_x < 500:
                self.counter_x += 75
            else:
                self.counter_x += 100
            if self.counter_x >= 1700:
                self.start_fade = 0
                self.return_to_crawl = 1

        pygame.display.flip()

        return 
    
    def process_fade(self):
        go = 1
        while go == 1:
            print("Fading in")
            self.counter_x += 256
            self.counter_y += 144
            self.crawler_fade_in()
            if self.counter_x >= 12800 or self.counter_y >= 7200:
                self.counter_x = 0
                self.counter_y = 0
                go = 0

    def crawler_fade_in(self):
        fade = pygame.transform.scale(fade,(0 + self.counter_x,0 + self.counter_y))
        blit_image((1600,900), 7200-self.counter_x/2, 4050-self.counter_y/2, fade, 1,1,1)
        pygame.display.flip()

    def scoot(self, counter_x):
        transfer = 1
        black_pass = pygame.image.load("images/black_pass.png")
        while transfer == 1:
            blit_image((1600,900), width-counter_x, height, black_pass, 1,1,1)
            counter_x += 1
            if counter_x >= 1600:
                transfer = 0

    def play_victory_line(self):
        clip = random.randint(0,1)
        to_load = "audio/voice/nsteen/victoryline_" + str(clip) + ".wav"
        victory_line = pygame.mixer.Sound(to_load)
        #victory_line.play()
        return victory_line.get_length()
    
    # TODO: Implementing talking portrait while victory line is being spoken!
    def current_talking_portrait(self):
        if self.talking_timer % 200 == 0:
            pass

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
    party = fill_party()
    state = MatchGame(screen).play(party, get_dungeon("cave")[0])
    print("Your final result was: " + state)