import sys, pygame, os
import dialog as dia
import classes
from helpers import *
import match
from classes import *
import crawler
import pickle

class MainGame():
    def __init__(self):
        pygame.init()
        size = width, height = 1600, 900
        self.progress = 1
        self.advance = 0
        self.exit_next = 0
        self.background_move = True
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
        self.party = []
        self.counter_x = 0
        self.counter_y = 0
        self.fade_image = pygame.image.load("images/black_pass.png").convert_alpha()
        self.i = 0
        self.font = pygame.font.Font("font/VCR.001.ttf", 32)
        self.level = 0
        self.debug = 0
        self.nsteen = BearKnight([15, 10, 10, 5, 5, 0])
        self.move_to_crawl = 0
        self.fade_over = 0
        self.save_object = None

    def start_screen(self):
        #### SETUP ####
        pygame.display.set_caption("Creatures of Habbitt v.01")
        
        black = 0, 0, 0
        speed = [3, 0]

        clock = pygame.time.Clock()

        color_passive = "BLACK"
        
        self.background = retrieve_background("villageinnnight")
        
        title_rect = pygame.Rect(width-1100,height-800,500,50)
        start_rect = pygame.Rect(width-900,height-450,200,50)
        town_start_rect = pygame.Rect(width-900,height-375,200,50)
        load_rect = pygame.Rect(width-900,height-300,200,50)
        options_rect = pygame.Rect(width-900,height-225,200,50)
        exit_rect = pygame.Rect(width-850,height-150,100,50)

        i = 0

        while True:
            self.screen.fill(black)
            color_start, color_town_start, color_options, color_exit, color_load = color_passive, color_passive, color_passive, color_passive, color_passive
            color_exit = "BLACK"

            for event in pygame.event.get():                  
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        return "new_game"
                    if town_start_rect.collidepoint(event.pos):
                        return "dialog skip"
                    if load_rect.collidepoint(event.pos) and os.path.isfile("save.txt"):
                        return "load"
                    if exit_rect.collidepoint(event.pos):
                        return "exit"

            if start_rect.collidepoint(pygame.mouse.get_pos()):
                color_start = "RED"
            if town_start_rect.collidepoint(pygame.mouse.get_pos()):
                color_town_start = "RED"
            if load_rect.collidepoint(pygame.mouse.get_pos()):
                color_load = "RED"
            if options_rect.collidepoint(pygame.mouse.get_pos()):
                color_options = "RED"
            if exit_rect.collidepoint(pygame.mouse.get_pos()):
                color_exit = "RED"

            if not os.path.isfile("save.txt"):
                color_load = "GRAY"

            self.gl_draw_start_screen(color_passive, color_start, color_town_start, color_load, color_options, color_exit)
            clock.tick(60)

    def gl_draw_start_screen(self, cp, c1, c2, c3, c4, c5):
        self.i = blit_bg(self.i, self.background, self.background_move)

        #gl_text(self.font, "BLACK",  cgls(width-500, width), cgls(width-1100, width), cgls(height-150, height), cgls(height-100, height), "Creatures of Habbitt v.01", .88, .982)
        blit_image((width, height), width-1200, height-450, pygame.image.load("images/logo.png").convert_alpha(), 1,1,1)
        gl_text_name(self.font, c1, cgls(width-700, width), cgls(width-900, width), cgls(height-500, height), cgls(height-450, height), "New Game", 1, .965)
        gl_text_name(self.font, c2, cgls(width-675, width), cgls(width-925, width), cgls(height-575, height), cgls(height-525, height), "Skip Intro", 1, .96)
        gl_text_name(self.font, c3, cgls(width-700, width), cgls(width-900, width), cgls(height-650, height), cgls(height-600, height), "Load", 1, .95)
        gl_text_name(self.font, c4, cgls(width-700, width), cgls(width-900, width), cgls(height-725, height), cgls(height-675, height), "Options", 1, .925)
        gl_text_name(self.font, c5, cgls(width-700, width), cgls(width-900, width), cgls(height-800, height), cgls(height-750, height), "Exit", 1, .89)

        pygame.display.flip()

    def in_dialog(self, skip=False, progress=1):

        #### SETUP ####
        size = width, height = 1600, 900
        speed = [3, 0]
        black = 0, 0, 0

        clock = pygame.time.Clock()

        if self.background == None:
            self.background = retrieve_background("cave")

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)
        self.user_text = [[[None, "[Character creation]"]
        ], "intro_3_quick"]

        self.advance = 0

        dialog_rect = pygame.Rect(width-1550,height-250, 1500, 200)
        name_rect = pygame.Rect(width-1550, height-320, 300, 50)
        color_passive = pygame.Color('black')

        remove = ["VIZGONE", "GUARDGONE", "MYSTBEARGONE", "HENRIETTAGONE"]

        i = 0
        global party
        party = []
        self.slots = [0, 0, 0]

        curr_text = self.user_text[0][self.advance][1]
        if curr_text in ["inn"]:
            choice = self.inn_menu(self.screen, self.progress, retrieve_background("tavern"))

        if skip != False:
            self.dialog = dia.Dialog("Player")
            if skip == "To Town":
                self.user_text = self.dialog.intro_skip_to_town
            else:
                self.user_text = self.dialog.intro_1_quick

        while True:            
            self.pick_dialog()            
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)
            
            if self.move_to_crawl == 1:
                self.fade_over = 0
                state = self.load_dungeon(self.user_text[1])
                if state == "FINISHED":
                    self.progress = self.user_text[3]
                self.user_text = self.dialog.process_state(self.user_text[1], state)
                self.move_to_crawl = 0
                self.advance = 0
            elif self.fade_over == 1:
                self.who_is_on_the_screen()
                gl_text_wrap_dialog(self.font, "BLACK", cgls(width-1550, width), cgls(width-50, width), cgls(height-650, height), cgls(height-850, height), "Loading dungeon...", .7, 2.15, self.level)
                self.fade_out()
                pygame.display.flip()
                clock.tick(60)
            else:
                self.who_is_on_the_screen()

                speaking_name = self.user_text[0][self.advance][0]
                if speaking_name != None:
                    if speaking_name in remove:
                        self.slots = remove_portrait(speaking_name, self.slots)
                    else:
                        #gl_text_name(self.font, "BLACK", cgls(width-1250, width), cgls(width-1550, width), cgls(height-630, height), cgls(height-580, height), speaking_name, 1, .95) #.8, .95
                        #if speaking_name == self.slots[0]:
                        #    gl_text_name(self.font, "BLACK", cgls(width-800, width), cgls(width-1100, width), cgls(height-630, height), cgls(height-580, height), speaking_name, 1, .95) #.8, .95
                        #elif speaking_name == self.slots[1] or self.special_cases_slots_2(speaking_name):
                        #    gl_text_name(self.font, "BLACK", cgls(width-650, width), cgls(width-950, width), cgls(height-630, height), cgls(height-580, height), speaking_name, 1, .95) #.8, .95
                        #elif speaking_name == self.slots[2] or self.special_cases_slots_3(speaking_name):
                        #    gl_text_name(self.font, "BLACK", cgls(width-800, width), cgls(width-500, width), cgls(height-630, height), cgls(height-580, height), speaking_name, 1, .95) #.8, .95
                        
                        # Arg 1 is the name of the character to be portraited, Arg 2 is always main character
                        character = retrieve_character(speaking_name, self.characters)
                        # self.slots[0] is left, self.slots[1] is middle, self.slots[2] is right
                        if self.slots[0] == 0 and self.slots[1] != speaking_name and self.slots[2] != speaking_name:
                            self.slots[0] = speaking_name
                        elif self.slots[2] == 0 and self.slots[0] != speaking_name and self.slots[1] != speaking_name:
                            self.slots[2] = speaking_name
                        elif self.slots[1] == 0 and self.slots[0] != speaking_name and self.slots[2] != speaking_name:
                            self.slots[1] = speaking_name

                # (width-1550,height-250,1500,200)
                #glBegin(GL_QUADS)
                #rect_ogl("BLACK", cgls(width-1550, width), cgls(width-50, width), cgls(height-650, height), cgls(height-850, height))
                #glEnd()
                if speaking_name == None:
                    gl_text_wrap_dialog(self.font, "BLACK", cgls(width-1550, width), cgls(width-50, width), cgls(height-650, height), -.999999, self.user_text[0][self.advance][1], .7, 2.15, self.level)
                else:
                    gl_text_wrap_dialog(self.font, "BLACK", cgls(width-1250, width), cgls(width-50, width), cgls(height-650, height), -.999999, self.user_text[0][self.advance][1], .9, 2.15, self.level)
                    char_port = retrieve_character(speaking_name, self.characters, True)
                    char_port = pygame.transform.scale(char_port, (200, 266))
                    glBegin(GL_QUADS)
                    rect_ogl("BLACK", cgls(width-1550, width), cgls(width-1250, width), cgls(height-650, height), -.999999)
                    glEnd()
                    blit_image((width, height), width-1505, height-835, char_port, 1, 1, 1)
                    gl_text_name(self.font, "BLACK", cgls(width-1300, width), cgls(width-1500, width), cgls(height-875, height), cgls(height-850, height), speaking_name, 1, 1) #.8, .95

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if dialog_rect.collidepoint(event.pos):
                            if 0 <= self.advance+1 < len(self.user_text[0]):
                                self.advance += 1
                                fade_out = 1
                            else:
                                self.pick_dialog()

                pygame.display.flip()
                clock.tick(60)

    def who_is_on_the_screen(self):
        if self.slots != [0,0,0] and self.debug == 1:
            print(self.slots)    
        if self.slots[0] != 0:
            character = retrieve_character(self.slots[0], self.characters)
            blit_image((width, height), width-1500, 100, character, 1,1,1)
        if self.slots[1] != 0:
            character = retrieve_character(self.slots[1], self.characters)
            if self.slots[1] == "N. Steen" or self.slots[1] == "Mysterious Bear":
                blit_image((width, height), width/2-300, -75, character, 1,1,1)
            elif (self.slots[1] == "Hippo" or self.slots[1] == "Henrietta") and self.slots[2] == "N. Steen":
                blit_image((width, height), width/2-400, 100, character, 1,1,1)
            elif (self.slots[1] == "Hippo" or self.slots[1] == "Henrietta"):
                blit_image((width, height), width/2-300, 100, character, 1,1,1)
            elif self.slots[2] == "Guard":
                blit_image((width, height), width - (width/2/2)-300, 100, character, 1,1,1)
            else:
                blit_image((width, height), width/2-150, 100, character, 1,1,1)
        if self.slots[2] != 0:
            character = retrieve_character(self.slots[2], self.characters)
            if self.slots[2] == "N. Steen" or self.slots[2] == "Mysterious Bear" or self.slots[2] == "Henrietta":
                blit_image((width, height), width - (width/2/2)-350, -75, character, 1,1,1)
            elif self.slots[2] == "Guard":
                blit_image((width, height), width - (width/2/2)-300, 100, character, 1,1,1)
            elif self.slots[2] == "Vizier":
                blit_image((width, height), width - (width/2/2)-100, 100, character, 1,1,1)
            else:
                blit_image((width, height), width - (width/2/2), 100, character, 1,1,1)
        if self.slots[1] != 0 and self.slots[2] == 0:
            self.slots[2] = self.slots[1]
            self.slots[1] = 0

    def special_cases_slots_2(self, speaking_name):
        if speaking_name == "Henrietta" and self.slots[1] == "Hippo":
            return True
        else:
            return False
        
    def special_cases_slots_3(self, speaking_name):
        if speaking_name == "N. Steen" and self.slots[1] == "Mysterious Bear":
            return True
        else:
            return False

    def fade_out(self):
        blit_image([width, height], width-self.counter_x, 0, pygame.image.load("images/black_pass.png").convert_alpha(), 1, 1, 1)
        print(self.counter_x)
        if self.counter_x < 200:
            self.counter_x += 50
        elif self.counter_x < 500:
            self.counter_x += 75
        else:
            self.counter_x += 100
        if self.counter_x >= 1700:
            self.fade_over = 0
            self.move_to_crawl = 1

    def dialog_options(self, screen, text_left, text_right, target_left, target_right):
        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)

        color_passive = pygame.Color('black')

        left_rect = pygame.Rect(width-1550,height-250,700,50)
        right_rect = pygame.Rect(width-750,height-250,700,50)

        i = 0

        while True:
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)
            color_left = "BLACK"
            color_right = "BLACK"

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if left_rect.collidepoint(event.pos):
                        return target_left
                    if right_rect.collidepoint(event.pos):
                        return target_right
                
            if left_rect.collidepoint(pygame.mouse.get_pos()):
                color_left = "RED"
            if right_rect.collidepoint(pygame.mouse.get_pos()):
                color_right = "RED"

            gl_text_name(self.font, color_left, cgls(width-1550, width), cgls(width-850, width), cgls(height-650, height), cgls(height-700, height), text_left, 1, 1.17)
            gl_text_name(self.font, color_right, cgls(width-750, width), cgls(width-50, width), cgls(height-650, height), cgls(height-700, height), text_right, 1, 1.17)

            pygame.display.flip()
            clock.tick(60)       

    def pick_dialog(self):
        self.background, self.background_move = self.determine_background(self.user_text[0][self.advance][1], self.background, self.background_move)
        if self.exit_next == 1:
            sys.exit()
        elif self.user_text[0][self.advance][1] == "[Character creation]":
            self.main_character = self.character_creator()
            self.party.append(self.main_character)
            self.nsteen.set_name("N. Steen")
            self.nsteen.set_portrait_dungeon("bear")
            self.party.append(self.nsteen)
            self.dialog = dia.Dialog(self.main_character.get_name())
            self.user_text = self.dialog.determine_dialog(self.user_text[1], self.progress, self.char_name)
            self.advance = 0
            self.characters = [self.main_character, self.nsteen]
            return
        elif self.user_text[0][self.advance][1] == "[Dungeon CAVE]":
            self.fade_over = 1
        elif self.user_text[0][self.advance][1] == "[Bear N. Steen has joined your party.]":
            self.party.append(add_party_member("nsteen"))
        elif self.user_text[0][self.advance][1] in ["Please select a destination.", "[Returning to town.]", "To Town"]:
            self.village_choices()
            self.slots = [0, 0, 0]
        elif self.user_text[0][self.advance][1] == "[You leave him to his devices.]" or self.user_text[0][self.advance][1] == "[You leave her to her devices.]":
            self.slots = [0, 0, 0]
            choice = self.inn_menu(self.screen, self.progress, self.background)
            self.user_text = self.dialog.determine_dialog(choice, self.progress, self.char_name)
            self.advance = 0
        elif self.user_text[0][self.advance][1] == "SELECTION":
            left_option = self.user_text[0][self.advance+1][1]
            right_option = self.user_text[0][self.advance+2][1]
            left_target = self.user_text[1]
            right_target = self.user_text[2]
            choice = self.dialog_options(self.screen, left_option, right_option, left_target, right_target)
            proceed = self.sort_options(choice)
            self.user_text = self.dialog.determine_dialog(choice, self.progress, self.char_name)
            self.advance = 0
            self.slots = [0, 0, 0]
        elif self.user_text[0][self.advance][1] == "Please type into the box.":
            array = self.input_box(self.user_text[1], self.background)
            temp = self.user_text[1]
            self.user_text, name = array[0], array[1]
            global name_global
            name_global = name
            self.sort_options(temp)
            self.advance = 0
            self.slots = [0, 0, 0]
        else:
            pass

    def village_choices(self):
        self.background, self.background_move = self.determine_background("Habbitt", self.background, self.background_move)
        if self.progress == 1:
            options = ["Inn", "???", "inn", None, "Save", "Add Party", "save", "party_debug", "Venture Out", "leave"]
            choice = self.town_options(self.screen, options, self.background)
            if choice == "party_debug":
                self.party = fill_party()
                self.user_text = [[[None, "Added party members."], [None, "[Returning to town.]"]]]
                self.advance = 0
            elif choice == "inn":
                self.user_text = [[[None, "There is currently no one to run the inn."], [None, "[Returning to town.]"]]]
                self.advance = 0
            elif choice == "leave":
                self.user_text = [[[None, "You shouldn't go out alone. Maybe someone in the inn can help you?"], [None, "[Returning to town.]"]]]
                self.advance = 0
            elif choice == "save":
                self.user_text = self.save_game()
                self.advance = 0
        elif self.progress == 2:
            options = ["Inn", "Smithy", "inn", "blacksmith", "Fill Party", "Save", "party_debug", "save", "Venture Out", "leave",]
            choice = self.town_options(self.screen, options, self.background)
            if choice == "party_debug":
                self.party = fill_party()
                self.user_text = [[[None, "Added party members."], [None, "[Returning to town.]"]]]
                self.advance = 0
            if choice == "blacksmith":
                self.user_text = [[[None, "There is no one to run the blacksmith, so it remains closed."], [None, "[Returning to town.]"]]]
                self.advance = 0
            elif choice == "inn":
                choice = self.inn_menu(self.screen, self.progress, retrieve_background("tavern"))
                self.user_text = self.dialog.determine_dialog(choice, self.progress, self.char_name)
                self.advance = 0
            elif choice == "save":
                self.user_text = self.save_game()
                self.advance = 0
            elif choice == "leave":
                if len(self.party) > 0:
                # Should go to location menu
                    state = self.location_menu()
                    if state == "FINISHED":
                        self.user_text = [[[None, "Your party finished exploring the dungeon."],[None, "[Returning to town.]"]]]
                    elif state == "DEAD":
                        self.user_text = [[[None, "Your party was wiped out..."],[None, "[Returning to town.]"]]]
                    elif state == "RAN" or "LEFT":
                        self.user_text = [[[None, "[Returning to town.]"]]]
                    self.advance = 0

    def save_game(self):
        if not os.path.isfile("save.txt"):
            file = open('save.txt', 'x')
            file.close()
        file = open('save.txt', 'wb')
        self.data = [self.progress, self.party]
        pickle.dump(self.data, file)
        file.close()
        return [[[None, "Your data has been saved."], [None, "[Returning to town.]"]]]

    def town_options(self, screen, options, background):

        text_top_left, text_top_right, target_top_left, target_top_right = options[0], options[1], options[2], options[3]
        text_bot_left, text_bot_right, target_bot_left, target_bot_right = options[4], options[5], options[6], options[7]
        text_leave, target_leave = options[8], options[9]
        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)

        color_passive = "BLACK"

        party_rect = pygame.Rect(width-300,height-900,300,50)
        top_left_rect = pygame.Rect(width-1550,height-350,700,50)
        top_right_rect = pygame.Rect(width-750,height-350,700,50)
        bot_left_rect = pygame.Rect(width-1550,height-250,700,50)
        bot_right_rect = pygame.Rect(width-750,height-250,700,50)
        leave_rect = pygame.Rect(width-750,height-150,700,50)

        self.background, self.background_move = self.determine_background("Habbitt", self.background, self.background_move)

        while True:
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)
            color_top_left = color_passive
            color_top_right = color_passive
            color_bot_left = color_passive
            color_bot_right = color_passive
            color_leave = color_passive
            color_party = color_passive

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if top_left_rect.collidepoint(event.pos):
                        return target_top_left
                    if top_right_rect.collidepoint(event.pos):
                        return target_top_right
                    if bot_left_rect.collidepoint(event.pos):
                        return target_bot_left
                    if bot_right_rect.collidepoint(event.pos):
                        return target_bot_right
                    if leave_rect.collidepoint(event.pos):
                        return target_leave
                    if party_rect.collidepoint(event.pos):
                        self.stats_menu()

            if top_left_rect.collidepoint(pygame.mouse.get_pos()):
                color_top_left = "RED"
            if top_right_rect.collidepoint(pygame.mouse.get_pos()):
                color_top_right = "RED"
            if bot_left_rect.collidepoint(pygame.mouse.get_pos()):
                color_bot_left = "RED"
            if bot_right_rect.collidepoint(pygame.mouse.get_pos()):
                color_bot_right = "RED"
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = "RED"
            if party_rect.collidepoint(pygame.mouse.get_pos()):
                color_party = "RED"
                

            gl_text_name(self.font, color_top_left, cgls(width-1550, width), cgls(width-850, width), cgls(height-550, height), cgls(height-600, height), text_top_left, 1, 1.115)
            gl_text_name(self.font, color_top_right, cgls(width-750, width), cgls(width-50, width), cgls(height-550, height), cgls(height-600, height), text_top_right, 1, 1.115)
            gl_text_name(self.font, color_bot_left, cgls(width-1550, width), cgls(width-850, width), cgls(height-650, height), cgls(height-700, height), text_bot_left, 1, 1.17)
            gl_text_name(self.font, color_bot_right, cgls(width-750, width), cgls(width-50, width), cgls(height-650, height), cgls(height-700, height), text_bot_right, 1, 1.17)
            gl_text_name(self.font, color_leave, cgls(width-750, width), cgls(width-50, width), cgls(height-750, height), cgls(height-800, height), text_leave, 1, 1.31)
            gl_text_name(self.font, color_party, cgls(width-300, width), cgls(width-0, width), cgls(height-50, height), cgls(height, height), "Party", 1, .99)


            pygame.display.flip()
            clock.tick(60)

    def inn_menu(self, screen, progress, background):
        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0

        color_passive = "BLACK"

        character1_rect = pygame.Rect(width-1550,height-550,700,50)
        character2_rect = pygame.Rect(width-750,height-550,700,50)
        character3_rect = pygame.Rect(width-1550,height-450,700,50)
        character4_rect = pygame.Rect(width-750,height-450,700,50)
        character5_rect = pygame.Rect(width-1550,height-350,700,50)
        character6_rect = pygame.Rect(width-750,height-350,700,50)
        character7_rect = pygame.Rect(width-1550,height-250,700,50)
        character8_rect = pygame.Rect(width-750,height-250,700,50)
        next_rect = pygame.Rect(width-1550,height-150,700,50)
        leave_rect = pygame.Rect(width-750,height-150,700,50)
        self.slots[0] = self.main_character.get_name()

        self.background = retrieve_background("tavern")

        while True:
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)
            color_c1 = color_passive
            color_c2 = color_passive
            color_c3 = color_passive
            color_c4 = color_passive
            color_c5 = color_passive
            color_c6 = color_passive
            color_c7 = color_passive
            color_c8 = color_passive
            color_next = color_passive
            color_leave = color_passive

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if character1_rect.collidepoint(event.pos):
                        return "nsteen"
                    if character2_rect.collidepoint(event.pos):
                        if self.progress >= 3:
                            return "radish"
                    if character3_rect.collidepoint(event.pos):
                        if self.progress >= 3:
                            return "radish"
                    if character4_rect.collidepoint(event.pos):
                        if self.progress >= 3:
                            return "radish"
                    if character5_rect.collidepoint(event.pos):
                        if self.progress >= 3:
                            return "radish"
                    if character6_rect.collidepoint(event.pos):
                        if self.progress >= 3:
                            return "radish"
                    if character7_rect.collidepoint(event.pos):
                        if self.progress >= 3:
                            return "radish"
                    if character8_rect.collidepoint(event.pos):
                        if self.progress >= 3:
                            return "radish"
                    if leave_rect.collidepoint(event.pos):
                        return "town"
                    if next_rect.collidepoint(event.pos):
                        pass

            if character1_rect.collidepoint(pygame.mouse.get_pos()):
                color_c1 = "RED"
            if character2_rect.collidepoint(pygame.mouse.get_pos()):
                color_c2 = "RED"
            if character3_rect.collidepoint(pygame.mouse.get_pos()):
                color_c3 = "RED"
            if character4_rect.collidepoint(pygame.mouse.get_pos()):
                color_c4 = "RED"
            if character5_rect.collidepoint(pygame.mouse.get_pos()):
                color_c5 = "RED"
            if character6_rect.collidepoint(pygame.mouse.get_pos()):
                color_c6 = "RED"
            if character7_rect.collidepoint(pygame.mouse.get_pos()):
                color_c7 = "RED"
            if character8_rect.collidepoint(pygame.mouse.get_pos()):
                color_c8 = "RED"
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = "RED"
            if next_rect.collidepoint(pygame.mouse.get_pos()):
                color_next = "RED"

            names = []
            names = ["???" for x in range(0,8)]

            names[0] = "Bear N. Steen"

            if self.in_party("Radish"):
                names[1] = "Radish Rabbit"

            if self.in_party("Grapefart"):
                names[2] = "Gil Grapefart"

            if self.in_party("Cinna"):
                names[6] = "Cinnamon Bun"

            bulk_adjust_y = 1.07

            gl_text_name(self.font, color_c1, cgls(width-1550, width), cgls(width-850, width), cgls(height-350, height), cgls(height-400, height), names[0], 1,  bulk_adjust_y)
            gl_text_name(self.font, color_c2, cgls(width-750, width), cgls(width-50, width), cgls(height-350, height), cgls(height-400, height), names[1], 1,  bulk_adjust_y)
            gl_text_name(self.font, color_c3, cgls(width-1550, width), cgls(width-850, width), cgls(height-450, height), cgls(height-500, height), names[2], 1,  bulk_adjust_y+.01)
            gl_text_name(self.font, color_c4, cgls(width-750, width), cgls(width-50, width), cgls(height-450, height), cgls(height-500, height), names[3], 1,  bulk_adjust_y+.01)
            gl_text_name(self.font, color_c5, cgls(width-1550, width), cgls(width-850, width), cgls(height-550, height), cgls(height-600, height), names[4], 1, 1.115)
            gl_text_name(self.font, color_c6, cgls(width-750, width), cgls(width-50, width), cgls(height-550, height), cgls(height-600, height), names[5], 1, 1.115)
            gl_text_name(self.font, color_c7, cgls(width-1550, width), cgls(width-850, width), cgls(height-650, height), cgls(height-700, height), names[6], 1, 1.17)
            gl_text_name(self.font, color_c8, cgls(width-750, width), cgls(width-50, width), cgls(height-650, height), cgls(height-700, height), names[7], 1, 1.17)
            gl_text_name(self.font, color_next, cgls(width-1550, width), cgls(width-850, width), cgls(height-750, height), cgls(height-800, height), "Next", 1, 1.31)
            gl_text_name(self.font, color_leave, cgls(width-750, width), cgls(width-50, width), cgls(height-750, height), cgls(height-800, height), "Leave", 1, 1.31)

            pygame.display.flip()
            clock.tick(60)


    def location_menu(self):
        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0
        progress = self.progress

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)

        color_passive = "BLACK"
        page = 1
        self.background, self.background_move = self.determine_background("map", self.background, self.background_move)

        dungeon_1_rect = pygame.Rect(width-1550,height-550,700,50)
        dungeon_2_rect = pygame.Rect(width-750,height-550,700,50)
        dungeon_3_rect = pygame.Rect(width-1550,height-450,700,50)
        dungeon_4_rect = pygame.Rect(width-750,height-450,700,50)
        dungeon_5_rect = pygame.Rect(width-1550,height-350,700,50)
        dungeon_6_rect = pygame.Rect(width-750,height-350,700,50)
        dungeon_7_rect = pygame.Rect(width-1550,height-250,700,50)
        dungeon_8_rect = pygame.Rect(width-750,height-250,700,50)
        next_rect = pygame.Rect(width-1550,height-150,700,50)
        leave_rect = pygame.Rect(width-750,height-150,700,50)

        while True:
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)
            colors = ["BLACK" for x in range(0,8)]
            color_c1, color_c2, color_c3, color_c4, color_c5, color_c6, color_c7, color_c8, color_next, color_leave = colors[0], colors[1], colors[2], colors[3], colors[4], colors[5], colors[6], colors[7], color_passive, color_passive

            if page == 1:
                dungeon_1 = "Cave"
                dungeon_2 = self.process_map(1, "Temple")
                dungeon_3 = self.process_map(2, "Grassland")
                dungeon_4 = self.process_map(3, "Forest")
                dungeon_5 = self.process_map(4, "Lava")
                dungeon_6 = self.process_map(5, "Ice")
                dungeon_7 = self.process_map(6, "Sea")
                dungeon_8 = self.process_map(7, "Cosmos")
            else:
                dungeon_1 = "Error"
                dungeon_2 = "Error"
                dungeon_3 = "Error"
                dungeon_4 = "Error"
                dungeon_5 = "Error"
                dungeon_6 = "Error"
                dungeon_7 = "Error"
                dungeon_8 = "Error"
            dungeons = [dungeon_1, dungeon_2, dungeon_3, dungeon_4, dungeon_5, dungeon_6, dungeon_7, dungeon_8]

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if dungeon_1_rect.collidepoint(event.pos):
                        return self.load_dungeon("cave")
                    if dungeon_2_rect.collidepoint(event.pos) and self.progress > 1:
                        return self.load_dungeon("Temple")
                    if dungeon_3_rect.collidepoint(event.pos) and self.progress > 2:
                        return self.load_dungeon("Grasslands")
                    if dungeon_4_rect.collidepoint(event.pos) and self.progress > 3:
                        return self.load_dungeon("Forest")
                    if leave_rect.collidepoint(event.pos):
                        return "LEFT"

            if dungeon_1_rect.collidepoint(pygame.mouse.get_pos()):
                color_c1 = "RED"
            if dungeon_2_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 1:
                color_c2 = "RED"
            if dungeon_3_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 2:
                color_c3 = "RED"
            if dungeon_4_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 3:
                color_c4 = "RED"
            if dungeon_5_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 4:
                color_c5 = "RED"
            if dungeon_6_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 5:
                color_c6 = "RED"
            if dungeon_7_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 6:
                color_c7 = "RED"
            if dungeon_8_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 7:
                color_c8 = "RED"
            if next_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 7:
                color_next = "RED"
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = "RED"

            bulk_adjust_y = 1.07

            gl_text_name(self.font, color_c1, cgls(width-1550, width), cgls(width-850, width), cgls(height-350, height), cgls(height-400, height), dungeons[0], 1,  bulk_adjust_y)
            gl_text_name(self.font, color_c2, cgls(width-750, width), cgls(width-50, width), cgls(height-350, height), cgls(height-400, height), dungeons[1], 1,  bulk_adjust_y)
            gl_text_name(self.font, color_c3, cgls(width-1550, width), cgls(width-850, width), cgls(height-450, height), cgls(height-500, height), dungeons[2], 1,  bulk_adjust_y+.01)
            gl_text_name(self.font, color_c4, cgls(width-750, width), cgls(width-50, width), cgls(height-450, height), cgls(height-500, height), dungeons[3], 1,  bulk_adjust_y+.01)
            gl_text_name(self.font, color_c5, cgls(width-1550, width), cgls(width-850, width), cgls(height-550, height), cgls(height-600, height), dungeons[4], 1, 1.115)
            gl_text_name(self.font, color_c6, cgls(width-750, width), cgls(width-50, width), cgls(height-550, height), cgls(height-600, height), dungeons[5], 1, 1.115)
            gl_text_name(self.font, color_c7, cgls(width-1550, width), cgls(width-850, width), cgls(height-650, height), cgls(height-700, height), dungeons[6], 1, 1.17)
            gl_text_name(self.font, color_c8, cgls(width-750, width), cgls(width-50, width), cgls(height-650, height), cgls(height-700, height), dungeons[7], 1, 1.17)
            gl_text_name(self.font, color_next, cgls(width-1550, width), cgls(width-850, width), cgls(height-750, height), cgls(height-800, height), "Next", 1, 1.31)
            gl_text_name(self.font, color_leave, cgls(width-750, width), cgls(width-50, width), cgls(height-750, height), cgls(height-800, height), "Leave", 1, 1.31)

            pygame.display.flip()
            clock.tick(60)

    def character_creator(self):
        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)

        color_passive = pygame.Color('black')

        i = 0

        input_text = ''
        
        # create rectangle
        input_rect = pygame.Rect(width-750, height/2/2, 200, 50)
        input_rect.center = (width/2, height/2/2*3)
        left_rect = pygame.Rect(width-1050, height/2, 100, 100)
        right_rect = pygame.Rect(width-650, height/2, 100, 100)

        color_active = pygame.Color('red')

        color = color_passive

        poss_images = ["dogdude", "batdude"]
        curr_image = 0
        
        active = False
        
        while True:
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)

            if len(input_text) > 16:
                input_text = input_text[:14]

            image1 = pygame.image.load("images/" + poss_images[curr_image] + ".png").convert_alpha()
            blit_image((width, height), width-900, height/2/2, image1, 1,1,1)

            image2 = pygame.image.load("images/leftarrow.png")
            blit_image((width, height), width-1050, height/2-(height/8), image2, 1,1,1)
            image3 = pygame.image.load("images/rightarrow.png")
            blit_image((width, height), width-650, height/2-(height/8), image3, 1,1,1)

            for event in pygame.event.get():
            # if user types QUIT then the self.screen will close
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if left_rect.collidepoint(event.pos):
                        if curr_image-1 >= 0:
                            curr_image -= 1
                        else:
                            curr_image = len(poss_images) - 1
                    if right_rect.collidepoint(event.pos):
                        if curr_image+1 < len(poss_images):
                            curr_image += 1
                        else:
                            curr_image = 0
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
        
                if event.type == pygame.KEYDOWN:
        
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
        
                        # get text input from 0 to -1 i.e. end.
                        input_text = input_text[:-1]
        
                    # Unicode standard is used for string
                    # formation
                    else:
                        input_text += event.unicode
                    
                    if event.key == pygame.K_RETURN:
                        char = MainCharacter([10,10,10,10,10,10])
                        char.set_name(input_text[:-1])
                        char.set_dialog_picture(poss_images[curr_image] + "_port.png")
                        char.set_portrait(poss_images[curr_image] + "_port_100.png")
                        char.set_portrait_dungeon(poss_images[curr_image])
                        char.set_portrait_dialog(poss_images[curr_image] + "_portrait")
                        self.char_name = input_text[:-1]
                        return char
        
            if active:
                color = color_active
            else:
                color = color_passive
                
            # draw rectangle and argument passed which should
            # be on self.screen
            glBegin(GL_QUADS)
            #pygame.draw.rect(self.screen, color, input_rect)
            # width-750, height/2/2, 200, 50
            rect_ogl("BLACK", cgls(width-950, width), cgls(width-650, width), cgls(height/2/2-25, height), cgls(height/2/2-75, height))
            glEnd()
        
            rect = gl_text_name(self.font, "BLACK", cgls(width-650, width), cgls(width-950, width), cgls(height/2/2-75, height), cgls(height/2/2-25, height), input_text, 1, .93)
            
            # set width of textfield so that text cannot get
            # outside of user's text input
            if rect != None:
                input_rect.w = max(100, rect.get_width()+10)
                input_rect.center = (width/2, height/2/2*3)
            
            # display.flip() will update only a portion of the
            # self.screen to updated, not full area
            pygame.display.flip()
            
            # clock.tick(60) means that for every second at most
            # 60 frames should be passed.
            clock.tick(60)

    def stats_menu(self):
        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)

        color_passive = "BLACK"

        i = 0

        input_text = ''
        
        # create rectangle
        back_rect = pygame.Rect(width/2+100, height-100, 200, 50)
        left_rect = pygame.Rect(width-1400, height/2+65, 100, 100)
        right_rect = pygame.Rect(width-950, height/2+65, 100, 100)

        color_active = pygame.Color('red')

        color = color_passive

        party_member_pics = []
        for member in self.party:
            party_member_pics.append(member.get_dialog_picture())
        current_member = 0
        
        active = False
        self.background, self.background_move = self.determine_background("stat_menu", self.background, self.background_move)
        
        while True:
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)
            color_back = "BLACK"

            if back_rect.collidepoint(pygame.mouse.get_pos()):
                color_back = "RED"

            char_name = self.party[current_member].get_name()

            image1 = party_member_pics[current_member]
            blit_image((width, height), width-1280, height/2/2-50, image1, 1,1,1)

            image2 = pygame.image.load("images/leftarrow.png")
            blit_image((width, height), width-1400, height/2-(height/8)-50, image2, 1,1,1)
            image3 = pygame.image.load("images/rightarrow.png")
            blit_image((width, height), width-950, height/2-(height/8)-50, image3, 1,1,1)

            gl_text_name(self.font, "BLACK", cgls(width-1300, width), cgls(width-950, width), cgls(height/2/2-125, height), cgls(height/2/2-75, height), char_name, 1, .93)
            gl_text_name(self.font, color_back, cgls(width/2+100, width), cgls(width/2-100, width), cgls(height-800, height), cgls(height-850, height), "Back", 1, 1)

            for event in pygame.event.get():
            # if user types QUIT then the self.screen will close
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if left_rect.collidepoint(event.pos):
                        if current_member-1 >= 0:
                            current_member -= 1
                        else:
                            current_member = len(party_member_pics) - 1
                    if right_rect.collidepoint(event.pos):
                        if current_member+1 < len(party_member_pics):
                            current_member += 1
                        else:
                            current_member = 0
                    if back_rect.collidepoint(event.pos):
                        return

            if active:
                color = color_active
            else:
                color = color_passive
                

            #glBegin(GL_QUADS)
            #rect_ogl("BLACK", cgls(width-950, width), cgls(width-650, width), cgls(height/2/2-25, height), cgls(height/2/2-75, height))
            #glEnd()
        
            
            
            pygame.display.flip()

            clock.tick(60)

    def load_dungeon(self, dungeon):
        state = crawler.Crawler(self.screen).play(self.party, get_dungeon(dungeon), "cave", True)
        self.counter_x = 1600
        self.main_menu_fade("Habbitt", False)
        return state

    def sort_options(self, choice):
        if choice == "martial_choice":
            prof = classes.Martial([12,10,10,10,10,10])
            prof.set_name(name_global) 
            return ["class", prof]
        elif choice == "bookish_choice":
            prof = classes.Bookish([10,10,10,12,10,10])
            prof.set_name(name_global)
            return ["class", prof]
        
    def fade(self, fade_image, counter_x, counter_y):
        fade_out = 1
        while fade_out != 0:
            if fade_out == 1:
                print("Fading out | counter_x == " + str(counter_x) + " | counter_y == " + str(counter_y))
                counter_x += 256
                counter_y += 144
                circle_fade_out(self.screen, counter_x, counter_y, fade_image)
                if counter_x >= 12800 or counter_y >= 7200:
                    fade_out = 2
                    counter_x = 0
                    counter_y = 0
            elif fade_out == 2:
                print("Fading in")
                counter_x += 256
                counter_y += 144
                circle_fade_in(self.screen, counter_x, counter_y, fade_image)
                if counter_x >= 6400 or counter_y >= 3600:
                    fade_out = 0
                    counter_x = 0
                    counter_y = 0

    def determine_background(self, dialog, bg, move):
        if dialog == "Regardless of your choice, I'm taking you outside.":
            return retrieve_background("forest"), True
        elif dialog == "Maybe you should just follow that road over there until you run into something." or dialog == "To Town":
            return retrieve_background("villageinn"), False
        elif dialog == "Ah, yes. Here we are! Welcome to Habbitt." or dialog == "To Town" or dialog == "You cross what feels like an endless number of hills until you come upon a single building in a clearing.":
            return retrieve_background("villageinnnight"), False
        elif dialog == "After a short time of severe jostling, you are deposited out the back door of the castle.":
            return retrieve_background("outside_castle_wall"), False
        elif dialog == "The two of you climb up a hill and he turns back to look at you.":
            return retrieve_background("hill"), False
        elif dialog == "Habbitt":
            return retrieve_background("villageinnnight"), False
        elif dialog == "map":
            return retrieve_background("map"), False
        elif dialog == "stat_menu":
            return retrieve_background("stat_menu"), True
        elif dialog == "The three of you arrive at Habbitt, in front of the familiar inn.":
            return retrieve_background("villageinnnight"), False
        else:
            return bg, move
        
    def process_map(self, pnum, map_name):
        if self.progress > pnum:
            return map_name
        else:
            return "???"

    def in_party(self, name):
        global party
        for member in party:
            if member.get_name() == name:
                return True
        return False

    def controller(self):
        while True:
            option = self.start_screen()
            #self.fade(self.fade_image, self.counter_x, self.counter_y)
            if option == "new_game":
                self.progress = 1
                self.main_menu_fade("Start_quick")
                self.in_dialog()
            elif option == "dialog skip":
                name_global = "Dan"
                self.progress = 2
                self.main_menu_fade("Habbitt")
                self.in_dialog("To Town", 0)
            elif option == "load":
                #check if load file exists
                if os.path.isfile("save.txt"):
                    #load file
                    file = open('save.txt', 'rb')
                    self.data = pickle.load(file)
                    file.close()
                    #place player in location associated with progress (usually town)
                    self.main_menu_fade("Habbitt")
                    self.in_dialog("To Town", self.progress)
                else:
                    print("Save file does not exist.")
            elif option == "exit":
                sys.exit()

    def main_menu_fade(self, skip, new_fade=True):
        if new_fade == True:
            self.counter_x = 0
        while True:
            self.i = blit_bg(self.i, self.background, self.background_move)
            blit_image([width, height], 1600-self.counter_x, 0, self.fade_image, 1, 1, 1)
            blit_image([width, height], -1600+self.counter_x, 0, self.fade_image, 1, 1, 1)
            self.counter_x+= 100
            if self.counter_x == 1600:
                if skip == "Habbitt":
                    self.background = retrieve_background("villageinnnight")
                elif skip == "Start":
                    self.background = retrieve_background("royalbedroom")
                elif skip == "Start_quick":
                    self.background = retrieve_background("cave")
                else:
                    self.background = retrieve_background("villageinnnight")
            if self.counter_x == 3200:
                return
            pygame.display.flip()

    def blit_bg_camera(self, bg="cave.png", move=True):
        background = pygame.image.load("images/" + bg).convert_alpha()
        background = pygame.transform.scale(background,(1600,900))
        blit_image([width, height], 0, 0, background, 1, 1, 1)
        

    """def draw_start_screen(font, color_start, color_town_start, color_options, color_exit):
        gl_text(font, "BLACK", cgls(1100, width), cgls(600, width), cgls(750, height), cgls(800, height), "Creatures of Habbitt", 1, 1)
        gl_text(font, color_start, cgls(900, width), cgls(700, width), cgls(500, height), cgls(550, height), "Start", 1, 1)
        gl_text(font, color_town_start, width-900, width-700, height-425, height-475, "Skip to Town", 1, 1)
        gl_text(font, color_options, width-900, width-700, height-350, height-400, "Options", 1, 1)
        gl_text(font, color_exit, width-850, width-750, height-200, height-250, "Exit", 1, 1)"""

if __name__ == "__main__":
    MainGame().controller()



