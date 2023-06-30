"""
File that contains code for screens in Creatures of Habbitt
Author: Dan Glendon
"""

import sys, pygame, os
import dialog_db as dia
from helpers import *
import match_game
from classes import *
import dungeon_crawler
import pickle
from rancher import *
from equipment_menu import EquipmentMenu

SIZE = width, height = 1600, 900

class MainGame():
    def __init__(self):
        pygame.init()

        # keeps track of where you are in the storyline
        self.progress = 1

        # keeps track of whether game is fullscreen or not
        self.full_screen = 0

        # difficulty
        # smooth, groovy, bodacious, chaos
        self.difficulty = "Smooth"

        # position in dialog
        self.advance = 0

        #
        self.exit_next = 0

        # whether the background scrolls
        self.background_move = True

        # the screen for the game, using OPENGL
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
        
        # your party members, starts with none but is filled after character creation
        self.party = [None, None, None, None]

        # fade 
        self.counter_x = 0
        self.counter_y = 0
        self.fade_image = pygame.image.load("images/black_pass.png").convert_alpha()
        self.fade_over = 0

        # position of background
        self.i = 0

        # font
        self.font = pygame.font.Font("font/VCR.001.ttf", 32)

        # level for tracking wordwrap
        self.level = 0

        # whether debug mode is on or not
        # (provides print statements that describe what is going on)
        self.debug = 0

        # nsteen's character is generated here
        self.nsteen = BearNSteen([15, 10, 10, 5, 5, 0])

        # whether to transition to dungeon crawling
        self.move_to_crawl = 0
        
        # the object that is written to save.txt
        self.save_object = None

        # colors for buttons
        self.color_passive = "BLACK" 
        self.color_active = "RED"

        # the text being shown in dialog
        self.user_text = None

        # pygame clock to keep track of frames
        self.clock = pygame.time.Clock()

        # music initialization
        pygame.mixer.init()
        self.boosted = 0
        self.music = pygame.mixer.Channel(5)
        self.habbitt_music = pygame.mixer.Sound("audio/bgm/habbittnature.wav")

        # ranch initialization
        self.ranch_game = RancherMinigame(self.screen)
        self.pets = [PetCharacter("images/rancher/illusium.png")]

        # character objects
        self.characters = [
            # Main Character
            MainCharacter([10,10,10,10,10,10]),
            # Bear N. Steen
            BearNSteen([10,10,10,10,10,10]),
            # Radish
            Radish([10,10,10,10,10,10]),
            # Grapefart
            Grapefart([10,10,10,10,10,10]),
            # Lam'baste
            BlankCharacter([10,10,10,10,10,10]),
            # Sunny
            BlankCharacter([10,10,10,10,10,10]),
            # Victor
            BlankCharacter([10,10,10,10,10,10]),
            # Donkey Hote
            BlankCharacter([10,10,10,10,10,10]),
            # Sidney
            BlankCharacter([10,10,10,10,10,10]),
            # None
            BlankCharacter([10,10,10,10,10,10]),
            # Hollow
            BlankCharacter([10,10,10,10,10,10]),
            # Henrietta
            Henrietta([10,10,10,10,10,10]),
            # Grilla
            BlankCharacter([10,10,10,10,10,10]),
            # Dane
            Dane([10,10,10,10,10,10]),
            # Rayna
            Rayna([10,10,10,10,10,10]),
            # None
            BlankCharacter([10,10,10,10,10,10]),
            # None
            BlankCharacter([10,10,10,10,10,10]),
            # None
            BlankCharacter([10,10,10,10,10,10]),
            # None
            BlankCharacter([10,10,10,10,10,10]),
            # None
            BlankCharacter([10,10,10,10,10,10]),
            # None
            BlankCharacter([10,10,10,10,10,10]),
            # None
            BlankCharacter([10,10,10,10,10,10])
            ]
        self.rom_characters, self.npc_characters = set_char_lists(self.characters)

        self.smithing_menu = EquipmentMenu("WEP")
        self.haber_menu = EquipmentMenu("ACC")

    def start_screen(self):
        """
        Controls logic for clicking actions on the start screen.
        Runs the drawing function as well.

        Returns:
            None, to return to controller
        """
        #### SETUP ####
        pygame.display.set_caption("Creatures of Habbitt v.01")
        
        black = 0, 0, 0
        speed = [3, 0]

        
        self.background, self.background_move = self.determine_background("villageinnnight", None, False)
        
        title_rect = pygame.Rect(width-width*0.6875,height-height*0.88,width*0.3125,height*0.0555555555555556)
        start_rect = pygame.Rect(width-900,height-450,200,50)
        town_start_rect = pygame.Rect(width-900,height-375,200,50)
        load_rect = pygame.Rect(width-900,height-300,200,50)
        options_rect = pygame.Rect(width-900,height-225,200,50)
        exit_rect = pygame.Rect(width-850,height-150,100,50)

        while True:
            self.screen.fill(black)
            color_start, color_town_start, color_options, color_exit, color_load = self.color_passive, self.color_passive, self.color_passive, self.color_passive, self.color_passive
            color_exit = "BLACK"

            for event in pygame.event.get():                  
                if event.type == pygame.QUIT: sys.exit()
                if event.type == KEYUP:
                    if event.key == K_r:
                        self.full_screen, self.screen, self.width, self.height = fullscreenify(self.full_screen, self.screen, width, height)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        return "new_game"
                    if town_start_rect.collidepoint(event.pos):
                        return "dialog skip"
                    if load_rect.collidepoint(event.pos) and os.path.isfile("save.txt"):
                        return "load"
                    if options_rect.collidepoint(event.pos):
                        self.options_menu()
                    if exit_rect.collidepoint(event.pos):
                        return "exit"

            if start_rect.collidepoint(pygame.mouse.get_pos()):
                color_start = self.color_active
            if town_start_rect.collidepoint(pygame.mouse.get_pos()):
                color_town_start = self.color_active
            if load_rect.collidepoint(pygame.mouse.get_pos()):
                color_load = self.color_active
            if options_rect.collidepoint(pygame.mouse.get_pos()):
                color_options = self.color_active
            if exit_rect.collidepoint(pygame.mouse.get_pos()):
                color_exit = self.color_active

            if not os.path.isfile("save.txt"):
                color_load = "GRAY"

            self.gl_draw_start_screen(self.color_passive, color_start, color_town_start, color_load, color_options, color_exit)
            self.clock.tick(60)

    def gl_draw_start_screen(self, cp, c1, c2, c3, c4, c5):
        """Draws the start screen in OpenGL.

        Args:
            cp (string): Color passive, ie BLACK
            c1 (string): color of the first button, can be BLACK or color_active
            c2 (string): color of the second button, can be BLACK or color_active
            c3 (string): color of the third button, can be BLACK or color_active
            c4 (string): color of the fourth button, can be BLACK or color_active
            c5 (string): color of the fifth button, can be BLACK or color_active
        """
        self.i = blit_bg(self.i, self.background, self.background_move)

        #gl_text(self.font, "BLACK",  cgls(width-500, width), cgls(width-1100, width), cgls(height-150, height), cgls(height-100, height), "Creatures of Habbitt v.01", .88, .982)
        blit_image((width, height), width*.25, height*.5, pygame.image.load("images/logo.png").convert_alpha(), 1,1,1)
        gl_text_name(self.font, c1, cgls(width-700, width), cgls(width-900, width), cgls(height-500, height), cgls(height-450, height), "New Game", 1, .965)
        gl_text_name(self.font, c2, cgls(width-675, width), cgls(width-925, width), cgls(height-575, height), cgls(height-525, height), "Skip Intro", 1, .96)
        gl_text_name(self.font, c3, cgls(width-700, width), cgls(width-900, width), cgls(height-650, height), cgls(height-600, height), "Load", 1, .95)
        gl_text_name(self.font, c4, cgls(width-700, width), cgls(width-900, width), cgls(height-725, height), cgls(height-675, height), "Options", 1, .925)
        gl_text_name(self.font, c5, cgls(width-700, width), cgls(width-900, width), cgls(height-800, height), cgls(height-750, height), "Exit", 1, .89)

        pygame.display.flip()

    def in_dialog(self, first=False, skip=False, progress=1, rank=False):

        #### SETUP ####
        speed = [3, 0]
        black = 0, 0, 0

        if self.background == None:
            self.background = retrieve_background("cave")

        if first == True:
            self.user_text = [[[None, "[Character creation]"]
            ], "intro_3_quick"]

        self.advance = 0

        dialog_rect = pygame.Rect(width-1550,height-250, 1500, 200)
        name_rect = pygame.Rect(width-1550, height-320, 300, 50)

        remove = ["VIZGONE", "GUARDGONE", "MYSTBEARGONE", "HENRIETTAGONE"]

        self.slots = [0, 0, 0]

        if first == True:
            curr_text = self.user_text[0][self.advance][1]
            if curr_text in ["inn"]:
                choice = self.inn_menu()

        if skip != False:
            if skip == "To Town":
                self.dialog = dia.Dialog("Dogdude")
                self.user_text = self.dialog.intro_skip_to_town
            elif skip == "Load":
                self.user_text = self.dialog.to_town
            else:
                self.user_text = self.dialog.intro_1_quick

        while True:            
            self.pick_dialog()            
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)

            if self.user_text[0][self.advance][1] == "END INN DIALOG":
                return
            
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
                self.clock.tick(60)
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
                self.clock.tick(60)

    def who_is_on_the_screen(self):
        """
        Adjusts speaking position for individual characters using a slot system
        inputs/returns: None, as it directly blits the character itself
        """
        if self.slots != [0,0,0] and self.debug == 1:
            print(self.slots)    

        # LEFT
        if self.slots[0] != 0:
            character = retrieve_character(self.slots[0], self.characters)
            blit_image((width, height), width-1500, 100, character, 1,1,1)

        # MIDDLE
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

        # RIGHT
        if self.slots[2] != 0:
            character = retrieve_character(self.slots[2], self.characters)
            if self.slots[2] == "N. Steen" or self.slots[2] == "Mysterious Bear":
                blit_image((width, height), width - (width/2/2)-350, -75, character, 1,1,1)
            elif self.slots[2] == "Henrietta":
                blit_image((width, height), width - (width/2/2)-300, 100, character, 1,1,1)
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
        if self.debug == 1:
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
        black = 0, 0, 0

        left_rect = pygame.Rect(width-1550,height-250,700,50)
        right_rect = pygame.Rect(width-750,height-250,700,50)

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
                color_left = self.color_active
            if right_rect.collidepoint(pygame.mouse.get_pos()):
                color_right = self.color_active

            gl_text_name(self.font, color_left, cgls(width-1550, width), cgls(width-850, width), cgls(height-650, height), cgls(height-700, height), text_left, 1, 1.17)
            gl_text_name(self.font, color_right, cgls(width-750, width), cgls(width-50, width), cgls(height-650, height), cgls(height-700, height), text_right, 1, 1.17)

            pygame.display.flip()
            self.clock.tick(60)       

    def pick_dialog(self):
        """
        Determines what to do with particular dialog.
        inputs: None
        return: None
        """
        # determine the background
        self.background, self.background_move = self.determine_background(self.user_text[0][self.advance][1], self.background, self.background_move)
        
        # if exit flag set, exit
        if self.exit_next == 1:
            sys.exit()

        # character creator
        elif self.user_text[0][self.advance][1] == "[Character creation]":
            # main character = result of character creator
            self.main_character = self.character_creator()

            # add mc to characters
            self.characters[0] = self.main_character

            # add mc to party
            self.party[0] = self.main_character           

            # add n steen to party by default
            self.party[1] = self.nsteen
            self.characters[1] = self.nsteen

            # set dialog MC variable to name of MC for replacement
            self.dialog = dia.Dialog(self.main_character.get_name())
            
            # find the next dialog
            self.user_text = self.dialog.determine_dialog(self.user_text[1], self.progress, self.char_name)
            self.advance = 0

            # create lists with romance characters and npcs for later use
            self.rom_characters = [self.main_character, self.nsteen, None, None, None, None, None, None, None, None, None]
            self.character_names = [self.main_character.get_name(), self.nsteen.get_name(), None, None, None, None, None, None, None, None, None]

            # create and add Henrietta as we will rescue her before returning to town the first time
            self.npc_names = ["Henrietta", None, None, None, None, None, None, None, None, None]
            henrietta = Henrietta([15, 10, 10, 10, 10, 10])
            henrietta.set_recruited(1)
            self.npc_characters = [henrietta, None, None, None, None, None, None, None, None, None]
            self.characters[11] = henrietta
        
        # start the fade if [Dungeon CAVE] is dialog
        elif self.user_text[0][self.advance][1] == "[Dungeon CAVE]":
            self.fade_over = 1

        # open town menu
        elif self.user_text[0][self.advance][1] in ["Please select a destination.", "[Returning to town.]", "To Town"]:
            self.village_choices()
            self.slots = [0, 0, 0]
            self.user_text

        # end inn dialog
        elif self.user_text[0][self.advance][1] == "[You leave him to his devices.]" or self.user_text[0][self.advance][1] == "[You leave her to her devices.]":
            self.slots = [0, 0, 0]
            choice = self.inn_menu()
            self.user_text = self.dialog.determine_dialog(choice, self.progress, self.char_name)
            self.advance = 0

        # create two buttons with selections on them 
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

        # input box (deprecated)
        elif self.user_text[0][self.advance][1] == "Please type into the box.":
            array = ["To Town", "Name"]
            temp = self.user_text[1]
            self.user_text, name = array[0], array[1]
            self.name_global = name
            self.sort_options(temp)
            self.advance = 0
            self.slots = [0, 0, 0]
        else:
            pass

    def village_choices(self):
        """
        Display choices avillage menu 
        inputs: None
        return: None
        """
        self.rom_characters, self.npc_characters = set_char_lists(self.characters)
        if not self.music.get_busy():
            self.music.play(self.habbitt_music, -1)
            self.music.set_volume(7)
        # retrieve background
        self.background, self.background_move = self.determine_background("Habbitt", self.background, self.background_move)

        # MENU:
            # Inn           || Smithy
            # Haberdasher   || Save
            #               || Venture Out
            #               || Boost Party
        # determine which menu options are available
        if self.progress > 1:
            options = ["Inn", "Smithy", "inn", "blacksmith", "Haberdashery", "Save", "haberdashery", "save", "Ranch", "ranch", "Venture Out", "leave"]
        elif self.progress == 0:
            options = ["Inn", "???", "inn", "???", "???", "Save", "???", "save", "Venture Out", "leave"]
        choice = self.town_options(options)
        # Add all current characters and then boost them to 9999
        if choice == "party_debug":
            if self.boosted == 1:
                self.user_text = [[[None, "Party has already been boosted."], [None, "[Returning to town.]"]]]
                self.advance = 0

            else:
                # give party of MC, Bear, Radish, Grapefart, lvl9999
                self.party, self.rom_characters, self.character_names, self.npc_characters, self.npc_names, self.characters = add_all_characters(
                    self.party, self.rom_characters, self.character_names, self.npc_characters, self.npc_names, self.characters)
                self.party = boost_party(self.characters)
                
                # return confirm text
                self.user_text = [[[None, "Added party members."], [None, "[Returning to town.]"]]]
                self.advance = 0
                self.boosted = 1
                self.progress = 46

        # No blacksmith to run yet
        if choice == "blacksmith":
            if self.characters[13].get_recruited() == False:
                self.user_text = [[[None, "There is no one to run the blacksmith, so it remains closed."], [None, "[Returning to town.]"]]]
                self.advance = 0
            else:
                self.smithing_menu.run(self.screen)
                self.user_text = [[[None, "[Returning to town.]"]]]
                self.advance = 0

        # No haberdashery to run yet
        if choice == "haberdashery":
            if self.characters[14].get_recruited() == False:
                self.user_text = [[[None, "There is no one to run the accessories shop, so it remains closed."], [None, "[Returning to town.]"]]]
                self.advance = 0
            else:
                self.haber_menu.run(self.screen)
                self.user_text = [[[None, "[Returning to town.]"]]]
                self.advance = 0
        
        # Inn menu loads because Henrietta is retrieved by prog2
        elif choice == "inn":
            self.music.fadeout(300)
            choice = self.inn_menu()
            self.user_text = self.dialog.determine_dialog(choice, self.progress, self.main_character.get_name())
            self.advance = 0

        # save game 
        elif choice == "save":
            self.user_text = self.load_save_choices("SAVE")
            self.advance = 0

        elif choice == "ranch":
            self.music.fadeout(300)
            self.ranch_game.run(self.pets)
            self.user_text = [[[None, "[Returning to town.]"]]]
            self.advance = 0

        # Open dungeons menu and process result
        elif choice == "leave":
            if len(self.party) > 0:
            # Should go to location menu
                self.music.fadeout(300)
                state = self.location_menu()
                if state == "FINISHED":
                    self.user_text = [[[None, "Your party finished exploring the dungeon."],[None, "[Returning to town.]"]]]
                elif state == "DEAD":
                    self.user_text = [[[None, "Your party was wiped out..."],[None, "[Returning to town.]"]]]
                elif state == "RAN" or "LEFT":
                    self.user_text = [[[None, "[Returning to town.]"]]]
                self.advance = 0

    def save_game(self, filename):
        """
        Saves game using Pickle module
        Input: None
        Returns: user_text for save game
        """
        if not os.path.isfile(filename):
            file = open(filename, 'x')
            file.close()
        file = open(filename, 'wb')
        # create data array that will be filled with character information
        data = [[] for x in range(26)]
        data[0] = [self.progress]
        for x in range(1, 22):
            c = self.characters[x-1]
            data[x] = [
                c.get_hp(), c.get_physical_guard(), c.get_magical_guard(), c.get_physical_attack(), 
                c.get_magic_attack(), c.get_quickness(), c.get_heartiness(), c.get_healing(),
                c.get_chutzpah(), c.get_willpower(), c.get_xp(), c.get_bonds(), c.get_recruited(), c.get_level(),
                c.get_all_conv_comp()
            ]
        party_save = []
        for x in range(0, len(self.party)):
            if self.party[x] != None:
                party_save.append(self.party[x].get_num())
            else:
                party_save.append(None)
        data[22] = party_save
        data[23] = self.mc_for_save
        data[24] = self.character_names
        data[25] = self.npc_names
        pickle.dump(data, file)
        file.close()
        return [[[None, "Your data has been saved."], [None, "[Returning to town.]"]]]

    def town_options(self, options):
        """
        Render options for town menu (Inn, Smithy, Boost Party, Save, Leave usually)
        Inputs: Options - a list that includes the text and targets to be rendered
        Returns: Target for intended button
        """

        # Distribute "options" input into separate variables
        text_top_left, text_top_right, target_top_left, target_top_right = options[0], options[1], options[2], options[3]
        text_bot_left, text_bot_right, target_bot_left, target_bot_right = options[4], options[5], options[6], options[7]
        text_bot_bot_left, target_bot_bot_left = options[8], options[9]
        text_leave, target_leave = options[10], options[11]

        # for screen fill
        black = 0, 0, 0

        # rectangles representing clickable space
        party_rect = pygame.Rect(width-300,height-900,300,50)
        top_left_rect = pygame.Rect(width-1550,height-350,700,50)
        top_right_rect = pygame.Rect(width-750,height-350,700,50)
        bot_left_rect = pygame.Rect(width-1550,height-250,700,50)
        bot_right_rect = pygame.Rect(width-750,height-250,700,50)
        bot_bot_left_rect = pygame.Rect(width-1550,height-150,700,50)
        leave_rect = pygame.Rect(width-750,height-150,700,50)
        debug_rect = pygame.Rect(width-500, height-75, 400, 50)

        while True:
            # pick background every loop because otherwise moving from stats screen won't return background to Habbitt
            self.background, self.background_move = self.determine_background("Habbitt", self.background, self.background_move)
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)

            # set the colors to black so we can use highlighting
            color_top_left = self.color_passive
            color_top_right = self.color_passive
            color_bot_left = self.color_passive
            color_bot_right = self.color_passive
            color_bot_bot_left = self.color_passive
            color_leave = self.color_passive
            color_party = self.color_passive
            color_boost = self.color_passive

            # Handle events
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
                    if bot_bot_left_rect.collidepoint(event.pos):
                        return target_bot_bot_left
                    if leave_rect.collidepoint(event.pos):
                        return target_leave
                    if party_rect.collidepoint(event.pos):
                        self.stats_menu()
                    if debug_rect.collidepoint(event.pos):
                        return "party_debug"

            # Turn boxes/text backgrounds red if moused over
            if top_left_rect.collidepoint(pygame.mouse.get_pos()):
                color_top_left = self.color_active
            if top_right_rect.collidepoint(pygame.mouse.get_pos()):
                color_top_right = self.color_active
            if bot_left_rect.collidepoint(pygame.mouse.get_pos()):
                color_bot_left = self.color_active
            if bot_right_rect.collidepoint(pygame.mouse.get_pos()):
                color_bot_right = self.color_active
            if bot_bot_left_rect.collidepoint(pygame.mouse.get_pos()):
                color_bot_bot_left = self.color_active
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = self.color_active
            if party_rect.collidepoint(pygame.mouse.get_pos()):
                color_party = self.color_active
            if debug_rect.collidepoint(pygame.mouse.get_pos()):
                color_boost = self.color_active
                
            # render text on buttons and draw rectangles
            gl_text_name(self.font, color_top_left, cgls(width-1550, width), cgls(width-850, width), cgls(height-550, height), cgls(height-600, height), text_top_left, 1, 1.115)
            gl_text_name(self.font, color_top_right, cgls(width-750, width), cgls(width-50, width), cgls(height-550, height), cgls(height-600, height), text_top_right, 1, 1.115)
            gl_text_name(self.font, color_bot_left, cgls(width-1550, width), cgls(width-850, width), cgls(height-650, height), cgls(height-700, height), text_bot_left, 1, 1.17)
            gl_text_name(self.font, color_bot_right, cgls(width-750, width), cgls(width-50, width), cgls(height-650, height), cgls(height-700, height), text_bot_right, 1, 1.17)
            gl_text_name(self.font, color_boost, cgls(width-100, width), cgls(width-500, width), cgls(height-825, height), cgls(height-875, height), "Boost Party", 1, 2)
            gl_text_name(self.font, color_bot_bot_left, cgls(width-1550, width), cgls(width-850, width), cgls(height-750, height), cgls(height-800, height), text_bot_bot_left, 1, 1.31)
            gl_text_name(self.font, color_leave, cgls(width-750, width), cgls(width-50, width), cgls(height-750, height), cgls(height-800, height), text_leave, 1, 1.31)
            gl_text_name(self.font, color_party, cgls(width-300, width), cgls(width-0, width), cgls(height-50, height), cgls(height, height), "Party", 1, .99)

            pygame.display.flip()
            self.clock.tick(60)

    def inn_menu(self):
        """
        The conversations menu when you click "Inn" from Habbit screen
        Inputs: None
        Return: Name of character to load dialog for, or "town" to return to town menu
        """
        black = 0, 0, 0

        # create rectangles left (invisible)
        left_larrow_rect = pygame.Rect(width-1500, height/2+65, 100, 100)
        left_rarrow_rect = pygame.Rect(width-1050, height/2+65, 100, 100)

        # create rectangles right (invisible)
        right_larrow_rect = pygame.Rect(width-650, height/2+65, 100, 100)
        right_rarrow_rect = pygame.Rect(width-200, height/2+65, 100, 100)

        check_rect = pygame.Rect(width/2-100, height-150, 200, 50)
        back_rect = pygame.Rect(width/2-100, height-75, 200, 50)

        # remove mc from rom list or else it's uneven
        rom_no_mc = self.rom_characters.copy()
        rom_no_mc.remove(self.main_character)

        # add mc to their own list
        mc_what_list = [self.main_character]

        # make list out of lists for each character
        characters_left = []

        # make a list that has all party member pictures and a separate list with all
        # characters that have been recruited
        party_member_pics = []
        for member in self.characters:
            if member.get_recruited() != 0:
                characters_left.append(member)
                party_member_pics.append(member.get_stats_picture())
        current_member_left = 0
        current_member_right = 1

        characters_right = characters_left.copy()

        # background
        self.background = retrieve_background("tavern")

        while True:
            # background stuff
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)

            # set rect colors as black
            color_back = "BLACK"
            color_check = "BLACK"

            # Make back rectangle red if you hover over it
            if back_rect.collidepoint(pygame.mouse.get_pos()):
                color_back = self.color_active
            if check_rect.collidepoint(pygame.mouse.get_pos()):
                color_check = self.color_active

            # Name of current party member
            char_left = characters_left[current_member_left]
            char_name_left = char_left.get_name()

            # Party member portrait
            image1 = party_member_pics[current_member_left]
            if char_name_left in ["Henrietta", "N. Steen"]:
                blit_image((width, height), width-1470, height/2/2-50, image1, 1,1,1)
            elif char_name_left in ["Dane", "Rayna", self.main_character.get_name(), "Radish", "Grapefart", "Lam'baste", "Sunny", "Hollow"]:
                blit_image((width, height), width-1430, height/2/2-50, image1, 1,1,1)
            else:    
                blit_image((width, height), width-1380, height/2/2-50, image1, 1,1,1)

            # Name of current party member
            char_right = characters_left[current_member_right]
            char_name_right = char_right.get_name()

            # Party member portrait
            image2 = party_member_pics[current_member_right]
            if char_name_right in ["Henrietta", "N. Steen"]:
                blit_image((width, height), width-630, height/2/2-50, image2, 1,1,1)
            elif char_name_right in ["Dane", "Rayna", self.main_character.get_name(), "Radish", "Grapefart", "Lam'baste", "Sunny", "Hollow"]:
                blit_image((width, height), width-590, height/2/2-50, image2, 1,1,1)
            else:    
                blit_image((width, height), width-540, height/2/2-50, image2, 1,1,1)

            image2 = pygame.image.load("images/leftarrow.png")
            blit_image((width, height), width-1500, height/2-(height/8)-50, image2, 1,1,1)
            blit_image((width, height), width-650, height/2-(height/8)-50, image2, 1,1,1)
            image3 = pygame.image.load("images/rightarrow.png")
            blit_image((width, height), width-1050, height/2-(height/8)-50, image3, 1,1,1)
            blit_image((width, height), width-200, height/2-(height/8)-50, image3, 1,1,1)

            # get current rank for selected pair
            num = char_right.which_num_party_member_bonds(char_right.get_name(), self.main_character.get_name())
            bond_rank = char_left.get_bond_rank(num)
            r_bond_rank = 0

            if char_left == self.main_character or char_right == self.main_character:
                if char_left.get_romanced() == True:
                    r_bond_rank = char_left.get_rom_bond_rank()
                if char_right.get_romanced() == True:
                    r_bond_rank = char_right.get_rom_bond_rank()

            gl_text_name(self.font, "BLACK", cgls(width/2+200, width), cgls(width/2-200, width), cgls(825, height), cgls(875, height), "Bond Rank: " + str(bond_rank), 1, .985)
            gl_text_name(self.font, "BLACK", cgls(width-1400, width), cgls(width-1050, width), cgls(height/2/2-125, height), cgls(height/2/2-75, height), char_name_left, 1, .89)
            gl_text_name(self.font, "BLACK", cgls(width-200, width), cgls(width-550, width), cgls(height/2/2-125, height), cgls(height/2/2-75, height), char_name_right, 1, .89)
            gl_text_name(self.font, color_back, cgls(width/2+100, width), cgls(width/2-100, width), cgls(height-825, height), cgls(height-875, height), "Back", 1, 2)
            gl_text_name(self.font, color_check, cgls(width/2+100, width), cgls(width/2-100, width), cgls(height/2/2-125, height), cgls(height/2/2-75, height), "Check", 1, .88)

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if left_larrow_rect.collidepoint(event.pos):
                        if current_member_left-1 >= 0:
                            current_member_left -= 1
                        else:
                            current_member_left = len(party_member_pics) - 1
                        arrow = 1
                    elif left_rarrow_rect.collidepoint(event.pos):
                        if current_member_left+1 < len(party_member_pics):
                            current_member_left += 1
                        else:
                            current_member_left = 0
                        arrow = 2
                    elif right_larrow_rect.collidepoint(event.pos):
                        if current_member_right-1 >= 0:
                            current_member_right -= 1
                        else:
                            current_member_right = len(party_member_pics) - 1
                        arrow = 3
                    elif right_rarrow_rect.collidepoint(event.pos):
                        if current_member_right+1 < len(party_member_pics):
                            current_member_right += 1
                        else:
                            current_member_right = 0
                        arrow = 4
                    if current_member_left == current_member_right:
                        if arrow == 1:
                            if current_member_right+1 < len(party_member_pics):
                                current_member_right += 1
                            else:
                                current_member_right = 0
                        if arrow == 2:
                            if current_member_right-1 < 0:
                                current_member_right = len(party_member_pics) - 1
                            else:
                                current_member_right -= 1
                        if arrow == 3:
                            if current_member_left+1 < len(party_member_pics):
                                current_member_left += 1
                            else:
                                current_member_left = 0
                        if arrow == 4:
                            if current_member_left-1 < 0:
                                current_member_left = len(party_member_pics) - 1
                            else:
                                current_member_left -= 1
                    if back_rect.collidepoint(event.pos):
                        return "town"
                    if check_rect.collidepoint(event.pos):
                        self.show_inn_dialog_options(char_left, char_right, bond_rank, r_bond_rank)
                    

            pygame.display.flip()
            self.clock.tick(60)

    def show_inn_dialog_options(self, char_left, char_right, bond_rank, r_bond_rank):
        """
        The conversations menu when you click "Inn" from Habbit screen
        Inputs: None
        Return: Name of character to load dialog for, or "town" to return to town menu
        """
        black = 0, 0, 0

        opt1_rect = pygame.Rect(100, height-750, 100, 100)
        opt2_rect = pygame.Rect(244, height-750, 100, 100)
        opt3_rect = pygame.Rect(388, height-750, 100, 100)
        opt4_rect = pygame.Rect(532, height-750, 100, 100)
        opt5_rect = pygame.Rect(676, height-750, 100, 100)
        opt6_rect = pygame.Rect(820, height-750, 100, 100)
        opt7_rect = pygame.Rect(964, height-750, 100, 100)
        opt8_rect = pygame.Rect(1108, height-750, 100, 100)
        opt9_rect = pygame.Rect(1252, height-750, 100, 100)
        opt10_rect = pygame.Rect(1396, height-750, 100, 100)
        optr1_rect = pygame.Rect(820, height-625, 100, 100)
        optr2_rect = pygame.Rect(964, height-625, 100, 100)
        optr3_rect = pygame.Rect(1108, height-625, 100, 100)
        optr4_rect = pygame.Rect(1252, height-625, 100, 100)
        optr5_rect = pygame.Rect(1396, height-625, 100, 100)

        back_rect = pygame.Rect(100, height-875, 100, 100)

        # make a list that has all party member pictures and a separate list with all
        # characters that have been recruited
        party_member_pics = []
        party_member_pics.append(char_left.get_stats_picture)
        party_member_pics.append(char_right.get_stats_picture)

        # background
        self.background = retrieve_background("tavern")

        while True:
            # background stuff
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)

            # set rect colors as black
            color_1, color_2, color_3, color_4, color_5, color_6, color_7, color_8, color_9, color_10 = "BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK" 
            color_r1, color_r2, color_r3, color_r4, color_r5 = "PINK", "PINK", "PINK", "PINK", "PINK"

            active_rank = None
            r_active_rank = None
            # Make back rectangle red if you hover over it
            if opt1_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 1:
                color_1 = self.color_active
                active_rank = 0
            if opt2_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 2:
                color_2 = self.color_active
                active_rank = 1
            if opt3_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 3:
                color_3 = self.color_active
                active_rank = 2
            if opt4_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 4:
                color_4 = self.color_active
                active_rank = 3
            if opt5_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 5:
                color_5 = self.color_active
                active_rank = 4
            if opt6_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 6:
                color_6 = self.color_active
                active_rank = 5
            if opt7_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 7:
                color_7 = self.color_active
                active_rank = 6
            if opt8_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 8:
                color_8 = self.color_active
                active_rank = 7
            if opt9_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 9:
                color_9 = self.color_active
                active_rank = 8
            if opt10_rect.collidepoint(pygame.mouse.get_pos()) and bond_rank >= 10:
                color_10 = self.color_active
                active_rank = 9
            if optr1_rect.collidepoint(pygame.mouse.get_pos()) and r_bond_rank >= 1:
                color_r1 = self.color_active
                r_active_rank = 1
            if optr2_rect.collidepoint(pygame.mouse.get_pos()) and r_bond_rank >= 2:
                color_r2 = self.color_active
                r_active_rank = 2
            if optr3_rect.collidepoint(pygame.mouse.get_pos()) and r_bond_rank >= 3:
                color_r3 = self.color_active
                r_active_rank = 3
            if optr4_rect.collidepoint(pygame.mouse.get_pos()) and r_bond_rank >= 4:
                color_r4 = self.color_active
                r_active_rank = 4
            if optr5_rect.collidepoint(pygame.mouse.get_pos()) and r_bond_rank >= 5:
                color_r5 = self.color_active
                r_active_rank = 5

            current_completeness = None
            previous_complete = True
            if active_rank != None or r_active_rank != None:
                complete = char_left.get_conversation_completeness(char_right.get_name(), self.main_character.get_name())
                current_completeness = complete[active_rank]
                if current_completeness == 1:
                    description = self.dialog.get_dialog_description(char_left.get_name(), char_right.get_name(), self.main_character.get_name(), active_rank, r_active_rank)
                else:
                    description = "A conversation is brewing..."
                
                if active_rank > 0:
                    before = complete[active_rank-1]
                    if before == 0:
                        previous_completed = False
            else:
                description = "Please select a rank to view."

            # Name of current party member
            char_left_name = char_left.get_name()
            char_right_name = char_right.get_name()

            # Party member portrait
            image1 = char_left.get_stats_picture()
            if char_left_name in ["Henrietta", "N. Steen"]:
                blit_image((width, height), width-1650, height/2/2-350, image1, 1,1,1)
            elif char_left_name in ["Dane", "Rayna", self.main_character.get_name(), "Radish", "Grapefart", "Lam'baste", "Sunny", "Hollow"]:
                blit_image((width, height), width-1600, height/2/2-300, image1, 1,1,1)
            else:    
                blit_image((width, height), width-1380, height/2/2-50, image1, 1,1,1)

            # Party member portrait
            image2 = char_right.get_stats_picture()
            if char_right_name in ["Henrietta", "N. Steen"]:
                blit_image((width, height), width-450, height/2/2-350, image2, 1,1,1)
            elif char_right_name in ["Dane", "Rayna", self.main_character.get_name(), "Radish", "Grapefart", "Lam'baste", "Sunny", "Hollow"]:
                blit_image((width, height), width-400, height/2/2-300, image2, 1,1,1)
            else:    
                blit_image((width, height), width-540, height/2/2-50, image2, 1,1,1)

            image2 = pygame.image.load("images/leftarrow.png")
            blit_image((width, height), 100, 775, image2, 1,1,1)

            # draw support boxes depending on the rank
            if bond_rank > 0:
                gl_text_name(self.font, color_1, cgls(100, width), cgls(200, width), cgls(650, height), cgls(750, height), "1", 1, .945)
            if bond_rank > 1:
                gl_text_name(self.font, color_2, cgls(244, width), cgls(344, width), cgls(650, height), cgls(750, height), "2", 1, .945)
            if bond_rank > 2:
                gl_text_name(self.font, color_3, cgls(388, width), cgls(488, width), cgls(650, height), cgls(750, height), "3", 1, .945)
            if bond_rank > 3:
                gl_text_name(self.font, color_4, cgls(532, width), cgls(632, width), cgls(650, height), cgls(750, height), "4", 1, .945)
            if bond_rank > 4:
                gl_text_name(self.font, color_5, cgls(676, width), cgls(776, width), cgls(650, height), cgls(750, height), "5", 1, .945)
            if bond_rank > 5:
                gl_text_name(self.font, color_6, cgls(820, width), cgls(920, width), cgls(650, height), cgls(750, height), "6", 1, .945)
            if bond_rank > 6:
                gl_text_name(self.font, color_7, cgls(964, width), cgls(1064, width), cgls(650, height), cgls(750, height), "7", 1, .945)
            if bond_rank > 7:
                gl_text_name(self.font, color_8, cgls(1108, width), cgls(1208, width), cgls(650, height), cgls(750, height), "8", 1, .945)
            if bond_rank > 8:
                gl_text_name(self.font, color_9, cgls(1252, width), cgls(1352, width), cgls(650, height), cgls(750, height), "9", 1, .945)
            if bond_rank > 9:
                gl_text_name(self.font, color_10, cgls(1396, width), cgls(1496, width), cgls(650, height), cgls(750, height), "10", 1, .945)
            if r_bond_rank > 0:
                gl_text_name(self.font, color_r1, cgls(820, width), cgls(920, width), cgls(525, height), cgls(625, height), "1", 1, .94)
            if r_bond_rank > 1:
                gl_text_name(self.font, color_r2, cgls(964, width), cgls(1064, width), cgls(525, height), cgls(625, height), "2", 1, .94)
            if r_bond_rank > 2:
                gl_text_name(self.font, color_r3, cgls(1108, width), cgls(1208, width), cgls(525, height), cgls(625, height), "3", 1, .94)
            if r_bond_rank > 3:
                gl_text_name(self.font, color_r4, cgls(1252, width), cgls(1352, width), cgls(525, height), cgls(625, height), "4", 1, .94)
            if r_bond_rank > 4:
                gl_text_name(self.font, color_r5, cgls(1396, width), cgls(1496, width), cgls(525, height), cgls(625, height), "5", 1, .94)

            gl_text_name(self.font, "GREEN", cgls(width/2+400, width), cgls(width/2-400, width), cgls(height-600, height), cgls(height-650, height), "RANK " + str(bond_rank), 1, 1.14, True)
            gl_text_name(self.font, "BLACK", cgls(width/2-200, width), cgls(width/2-400, width), cgls(height-550, height), cgls(height-600, height), char_left_name, 1, 1.12)
            gl_text_name(self.font, "BLACK", cgls(width/2+400, width), cgls(width/2+200, width), cgls(height-550, height), cgls(height-600, height), char_right_name, 1, 1.12)
            gl_text_wrap_dialog(self.font, "BLACK", cgls(width-1200, width), cgls(width-400, width), cgls(height-650, height), -.999999, description, .95, 2.15, self.level)

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if current_completeness == 0 and previous_complete:
                        if opt1_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 1)
                        if opt2_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 2)
                        if opt3_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 3)
                        if opt4_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 4)
                        if opt5_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 5)
                        if opt6_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 6)
                        if opt7_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 7)
                        if opt8_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 8)
                        if opt9_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 9)
                        if opt10_rect.collidepoint(event.pos):
                            self.handle_inn_dialog(char_left, char_right, 10)
                    if back_rect.collidepoint(event.pos):
                        return
                    

            pygame.display.flip()
            self.clock.tick(60)


    def location_menu(self):
        """
        The menu with the dungeons on it.
        Inputs: None
        Return: loaded dungeon depending on button pressed
        """

        # default setup stuff
        black = 0, 0, 0
        progress = self.progress
        self.background, self.background_move = self.determine_background("map", self.background, self.background_move)

        # page for multiple dungeon lists
        page = 1
      
        # clickable rects for each button
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
        difficulty_rect = pygame.Rect(width-750,height-800,700,50)

        progress_reqs = [
            0,  # Habbitt Cave 
            2,  # Grilla Garage 
            4,  # Tantamount Tower 
            6,  # Auspicious Abode 
            8,  # Desert/Temple 
            10, # Pasture 
            12, # Mall Mountain
            14, # Haunted Home
            16, # ???
            18, # Windmill Wilds
            20, # ???
            22, # Shark School
            24, # ???
            26, # Reaper's Respite
            28, # Ursine Utopia
            30, # Lake of Life
            32, # Homea
            34, # St. Stephonia
            36, # Tower of Torment
            38, # Acrimonious Abyss
            40,  # Bonus
            42,  # Bonus
            44,  # Bonus
            46  # Bonus
        ]

        d = self.difficulty
        if d == "Smooth":
            colors = ["BLACK" for x in range(0,8)]
        elif d == "Groovy":
            colors = ["BLUE" for x in range(0,8)]
        elif d == "Bodacious":
            colors = ["GREEN" for x in range(0,8)]
        elif d == "Chaos":
            colors = ["PINK" for x in range(0,8)]

        while True:
            # fill screen to cover up previous elements and assign black to all the buttons
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)
            
            color_c1, color_c2, color_c3, color_c4, color_c5, color_c6, color_c7, color_c8, color_next, color_leave = colors[0], colors[1], colors[2], colors[3], colors[4], colors[5], colors[6], colors[7], self.color_passive, self.color_passive
            color_diff = self.color_passive

            # assign maps to buttons based on page
            # process map checks if you have the progress assigned and otherwise returns ???
            if page == 1:
                dungeon_1 = "Habbitt Cave"
                dungeon_2 = self.high_enough_progress_to_show_map_name(progress_reqs[1], "Grilla's Garage")
                dungeon_3 = self.high_enough_progress_to_show_map_name(progress_reqs[2], "Kahuna Sands")
                dungeon_4 = self.high_enough_progress_to_show_map_name(progress_reqs[3], "Tantamount Tower")
                dungeon_5 = self.high_enough_progress_to_show_map_name(progress_reqs[4], "Auspicious Abode")
                dungeon_6 = self.high_enough_progress_to_show_map_name(progress_reqs[5], "Mall Mountain")
                dungeon_7 = self.high_enough_progress_to_show_map_name(progress_reqs[6], "Haunted Home")
                dungeon_8 = self.high_enough_progress_to_show_map_name(progress_reqs[7], "Pristine Pasture")
            elif page == 2:
                dungeon_1 = self.high_enough_progress_to_show_map_name(progress_reqs[8], "???")
                dungeon_2 = self.high_enough_progress_to_show_map_name(progress_reqs[9], "Windmill Wilds")
                dungeon_3 = self.high_enough_progress_to_show_map_name(progress_reqs[10], "???")
                dungeon_4 = self.high_enough_progress_to_show_map_name(progress_reqs[11], "Sea Sharp Shark School")
                dungeon_5 = self.high_enough_progress_to_show_map_name(progress_reqs[12], "???")
                dungeon_6 = self.high_enough_progress_to_show_map_name(progress_reqs[13], "Reaper's Respite")
                dungeon_7 = self.high_enough_progress_to_show_map_name(progress_reqs[14], "Ursine Utopia")
                dungeon_8 = self.high_enough_progress_to_show_map_name(progress_reqs[15], "Lake of Life")
            elif page == 3:
                dungeon_1 = self.high_enough_progress_to_show_map_name(progress_reqs[16], "Homea")
                dungeon_2 = self.high_enough_progress_to_show_map_name(progress_reqs[17], "St. Stephonia")
                dungeon_3 = self.high_enough_progress_to_show_map_name(progress_reqs[18], "Tower of Torment")
                dungeon_4 = self.high_enough_progress_to_show_map_name(progress_reqs[19], "Acrimonious Abyss")
                dungeon_5 = self.high_enough_progress_to_show_map_name(progress_reqs[20], "Bonus")
                dungeon_6 = self.high_enough_progress_to_show_map_name(progress_reqs[21], "Bonus")
                dungeon_7 = self.high_enough_progress_to_show_map_name(progress_reqs[22], "Bonus")
                dungeon_8 = self.high_enough_progress_to_show_map_name(progress_reqs[23], "Bonus")

            # add dungeons to an array
            dungeons = [dungeon_1, dungeon_2, dungeon_3, dungeon_4, dungeon_5, dungeon_6, dungeon_7, dungeon_8]

            # click events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if dungeon_1_rect.collidepoint(event.pos):
                        if page == 1:
                            return self.load_dungeon("cave")
                        elif self.progress > progress_reqs[8] and page == 2:
                            return self.load_dungeon("garage")
                        elif self.progress > progress_reqs[16] and page == 2:
                            return self.load_dungeon("garage")
                    if dungeon_2_rect.collidepoint(event.pos):
                        if self.progress > progress_reqs[1] and page == 1:
                            return self.load_dungeon("garage")
                        elif self.progress > progress_reqs[9] and page == 2:
                            return self.load_dungeon("garage")                        
                        elif self.progress > progress_reqs[17] and page == 3:
                            return self.load_dungeon("garage")
                    if dungeon_3_rect.collidepoint(event.pos): 
                        if self.progress > progress_reqs[2] and page == 1:
                            return self.load_dungeon("None")
                        elif self.progress > progress_reqs[10] and page == 2:
                                return self.load_dungeon("garage")
                        elif self.progress > progress_reqs[18] and page == 3:
                            return self.load_dungeon("garage")
                    if dungeon_4_rect.collidepoint(event.pos):
                        if self.progress > progress_reqs[3] and page == 1:
                            return self.load_dungeon("forest")
                        elif self.progress > progress_reqs[11] and page == 2:
                            return self.load_dungeon("garage")
                        elif self.progress > progress_reqs[19] and page == 3:
                            return self.load_dungeon("garage")
                    if dungeon_5_rect.collidepoint(event.pos):
                        if self.progress > progress_reqs[4] and page == 1:
                            return self.load_dungeon("forest")
                        elif self.progress > progress_reqs[12] and page == 2:
                            return self.load_dungeon("garage")
                        elif self.progress > progress_reqs[20] and page == 3:
                            return self.load_dungeon("garage")
                    if dungeon_6_rect.collidepoint(event.pos):
                        if self.progress > progress_reqs[5] and page == 1:
                            return self.load_dungeon("forest")
                        elif self.progress > progress_reqs[21] and page == 2:
                            return self.load_dungeon("garage")
                        elif self.progress > progress_reqs[19] and page == 3:
                            return self.load_dungeon("garage")
                    if dungeon_7_rect.collidepoint(event.pos):
                        if self.progress > progress_reqs[6] and page == 1:
                            return self.load_dungeon("forest")
                        elif self.progress > progress_reqs[14] and page == 2:
                            return self.load_dungeon("garage")
                        elif self.progress > progress_reqs[22] and page == 3:
                            return self.load_dungeon("garage")
                    if dungeon_8_rect.collidepoint(event.pos):
                        if self.progress > progress_reqs[7] and page == 1:
                            return self.load_dungeon("forest")
                        elif self.progress > progress_reqs[15] and page == 2:
                            return self.load_dungeon("garage")
                        elif self.progress > progress_reqs[23] and page == 3:
                            return self.load_dungeon("garage")
                    if next_rect.collidepoint(event.pos):
                        if page == 1:
                            page = 2
                        elif page == 2:
                            page = 3
                        elif page == 3:
                            page = 1
                    if leave_rect.collidepoint(event.pos):
                        return "LEFT"
                    if difficulty_rect.collidepoint(event.pos):
                        if self.difficulty == "Smooth":
                            self.difficulty = "Groovy"
                            colors = ["BLUE" for x in range(0,8)]
                        elif self.difficulty == "Groovy":
                            self.difficulty = "Bodacious"
                            colors = ["GREEN" for x in range(0,8)]
                        elif self.difficulty == "Bodacious":
                            self.difficulty = "Chaos"
                            colors = ["PINK" for x in range(0,8)]
                        elif self.difficulty == "Chaos":
                            self.difficulty = "Smooth"
                            colors = ["BLACK" for x in range(0,8)]
                    
            number_highlight = find_collide_for_highlight_color(self.progress, progress_reqs, page)

            # make buttons red if you hover over them
            if dungeon_1_rect.collidepoint(pygame.mouse.get_pos()) and number_highlight[0] == 1:
                color_c1 = self.color_active
            if dungeon_2_rect.collidepoint(pygame.mouse.get_pos()) and number_highlight[1] == 1:
                color_c2 = self.color_active
            if dungeon_3_rect.collidepoint(pygame.mouse.get_pos()) and number_highlight[2] == 1:
                color_c3 = self.color_active
            if dungeon_4_rect.collidepoint(pygame.mouse.get_pos()) and number_highlight[3] == 1:
                color_c4 = self.color_active
            if dungeon_5_rect.collidepoint(pygame.mouse.get_pos()) and number_highlight[4] == 1:
                color_c5 = self.color_active
            if dungeon_6_rect.collidepoint(pygame.mouse.get_pos()) and number_highlight[5] == 1:
                color_c6 = self.color_active
            if dungeon_7_rect.collidepoint(pygame.mouse.get_pos()) and number_highlight[6] == 1:
                color_c7 = self.color_active
            if dungeon_8_rect.collidepoint(pygame.mouse.get_pos()) and number_highlight[7] == 1:
                color_c8 = self.color_active
            if next_rect.collidepoint(pygame.mouse.get_pos()):
                color_next = self.color_active
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = self.color_active
            if difficulty_rect.collidepoint(pygame.mouse.get_pos()):
                color_diff = self.color_active

            # handy variable for text position adjustments (y)
            bulk_adjust_y = 1.07

            if self.difficulty == "Bodacious" or self.difficulty == "Chaos":
                black_text = True
            else:
                black_text = False

            # create visual buttons and text
            gl_text_name(self.font, color_diff, cgls(width-750, width), cgls(width-50, width), cgls(height-150, height), cgls(height-100, height), "Difficulty: " + self.difficulty, 1, .98)
            gl_text_name(self.font, color_c1, cgls(width-1550, width), cgls(width-850, width), cgls(height-350, height), cgls(height-400, height), dungeons[0], 1,  bulk_adjust_y, black_text)
            gl_text_name(self.font, color_c2, cgls(width-750, width), cgls(width-50, width), cgls(height-350, height), cgls(height-400, height), dungeons[1], 1,  bulk_adjust_y, black_text)
            gl_text_name(self.font, color_c3, cgls(width-1550, width), cgls(width-850, width), cgls(height-450, height), cgls(height-500, height), dungeons[2], 1,  bulk_adjust_y+.02, black_text)
            gl_text_name(self.font, color_c4, cgls(width-750, width), cgls(width-50, width), cgls(height-450, height), cgls(height-500, height), dungeons[3], 1,  bulk_adjust_y+.02, black_text)
            gl_text_name(self.font, color_c5, cgls(width-1550, width), cgls(width-850, width), cgls(height-550, height), cgls(height-600, height), dungeons[4], 1, 1.115, black_text)
            gl_text_name(self.font, color_c6, cgls(width-750, width), cgls(width-50, width), cgls(height-550, height), cgls(height-600, height), dungeons[5], 1, 1.115, black_text)
            gl_text_name(self.font, color_c7, cgls(width-1550, width), cgls(width-850, width), cgls(height-650, height), cgls(height-700, height), dungeons[6], 1, 1.17, black_text)
            gl_text_name(self.font, color_c8, cgls(width-750, width), cgls(width-50, width), cgls(height-650, height), cgls(height-700, height), dungeons[7], 1, 1.17, black_text)
            gl_text_name(self.font, color_next, cgls(width-1550, width), cgls(width-850, width), cgls(height-750, height), cgls(height-800, height), "Next", 1, 1.31)
            gl_text_name(self.font, color_leave, cgls(width-750, width), cgls(width-50, width), cgls(height-750, height), cgls(height-800, height), "Leave", 1, 1.31)

            pygame.display.flip()
            self.clock.tick(60)


    def character_creator(self):
        """
        Allows player to customize and create their avatar.
        inputs: None
        return: Main Character object
        """
        
        # default setup stuff
        black = 0, 0, 0
        color = self.color_passive

        # variable that holds the typed name
        input_text = ''
        
        # create interactable rectangles
        input_rect = pygame.Rect(width-750, height/2/2, 200, 50)
        input_rect.center = (width/2, height/2/2*3)
        left_rect = pygame.Rect(width-1050, height/2, 100, 100)
        right_rect = pygame.Rect(width-650, height/2, 100, 100)

        # array of possible image names for creatable characters
        poss_images = ["dogdude", "batdude"]
        curr_image = 0
        
        # active is for the text box being clicked on
        active = False
        
        while True:
            # typical background stuff
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)

            # stop the input name from being longer than 15 letters (cuz it would go out of the box)
            if len(input_text) > 16:
                input_text = input_text[:14]

            # load and blit the images that has been selected
            image1 = pygame.image.load("images/" + poss_images[curr_image] + ".png").convert_alpha()
            blit_image((width, height), width-900, height/2/2, image1, 1,1,1)

            # load and blit the arrows for changing which character is selected
            image2 = pygame.image.load("images/leftarrow.png")
            blit_image((width, height), width-1050, height/2-(height/8), image2, 1,1,1)
            image3 = pygame.image.load("images/rightarrow.png")
            blit_image((width, height), width-650, height/2-(height/8), image3, 1,1,1)

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # swap images if an arrow is clicked
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
                    # make input rectangle active if clicked on
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
        
                if event.type == pygame.KEYDOWN:
        
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
        
                        # Input text equals itself minus the last letter
                        input_text = input_text[:-1]
        
                    # Unicode standard is used for string
                    # formation
                    else:
                        input_text += event.unicode
                    
                    if event.key == pygame.K_RETURN:
                        # submit character name and fill in character object
                        char = MainCharacter([10,10,10,10,10,10], poss_images[curr_image], input_text[:-1])
                        self.mc_for_save = [poss_images[curr_image], input_text[:-1]]
                        self.char_name = input_text[:-1]
                        return char
        
            # change the color of the box if it's active
            if active:
                color = self.color_active
            else:
                color = self.color_passive
                
            # draw rectangle and argument passed which should
            # be on self.screen
            glBegin(GL_QUADS)
            #pygame.draw.rect(self.screen, color, input_rect)
            # width-750, height/2/2, 200, 50
            rect_ogl(color, cgls(width-950, width), cgls(width-650, width), cgls(height/2/2-25, height), cgls(height/2/2-75, height))
            glEnd()
        
            rect = gl_text_name(self.font, color, cgls(width-650, width), cgls(width-950, width), cgls(height/2/2-75, height), cgls(height/2/2-25, height), input_text, 1, .93)
            
            # set width of textfield so that text cannot get
            # outside of user's text input
            if rect != None:
                input_rect.w = max(100, rect.get_width()+10)
                input_rect.center = (width/2, height/2/2*3)
            
            # display.flip() will update only a portion of the
            # self.screen to updated, not full area
            pygame.display.flip()
            
            # self.clock.tick(60) means that for every second at most
            # 60 frames should be passed.
            self.clock.tick(60)

    def stats_menu(self):
        """
        Menu that displays recruited members, their stats, and their relationships.
        inputs: None
        returns: None
        """

        # black for fill
        black = 0, 0, 0
        
        # create rectangles (invisible)
        back_rect = pygame.Rect(width/2-100, height-75, 200, 50)
        party_rect = pygame.Rect(width-500, height-75, 400, 50)
        left_rect = pygame.Rect(width-1500, height/2+65, 100, 100)
        right_rect = pygame.Rect(width-1050, height/2+65, 100, 100)
        switch_rect = pygame.Rect(width-250, height-425, 150, 50)

        # switcher for relationships (npcs, romances, and mc)
        switcher = 0

        # remove mc from rom list or else it's uneven
        rom_no_mc = self.rom_characters.copy()
        rom_no_mc.remove(self.main_character)

        # add mc to their own list
        mc_what_list = [self.main_character]

        # make list out of lists for each character
        what_list = [rom_no_mc, self.npc_characters, mc_what_list]
        characters = []

        # make a list that has all party member pictures and a separate list with all
        # characters that do not equal "None"
        party_member_pics = []
        for x in what_list:
            for member in x:
                if member != None:
                    if member.get_recruited() != False:
                        characters.append(member)
                        party_member_pics.append(member.get_stats_picture())
        current_member = 0
        
        self.background, self.background_move = self.determine_background("stat_menu", self.background, self.background_move)
        new_char_names_list = self.character_names.copy()
        if self.main_character.get_name() in new_char_names_list:
            new_char_names_list.remove(self.main_character.get_name())
        mc_list = [self.main_character.get_name()]
        which_list = [new_char_names_list, self.npc_names, mc_list]
        switcher = 2
        
        while True:
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)
            color_back = "BLACK"
            color_switch = "BLACK"
            color_party = "BLACK"

            party_names = []
            for member in self.party:
                if member != None:
                    party_names.append(member.get_name())

            # Make back rectangle red if you hover over it
            if back_rect.collidepoint(pygame.mouse.get_pos()):
                color_back = self.color_active
            if switch_rect.collidepoint(pygame.mouse.get_pos()):
                color_switch = self.color_active
            if party_rect.collidepoint(pygame.mouse.get_pos()):
                color_party = self.color_active

            # Name of current party member
            char_name = characters[current_member].get_name()

            # Party member portrait
            image1 = party_member_pics[current_member]
            if char_name in ["Henrietta", "N. Steen"]:
                blit_image((width, height), width-1470, height/2/2-50, image1, 1,1,1)
            elif char_name in ["Dane", "Rayna", "Radish", "Grapefart", self.main_character.get_name(), "Lambaste", "Sunny", "Hollow"]:
                blit_image((width, height), width-1430, height/2/2-50, image1, 1,1,1)
            else:    
                blit_image((width, height), width-1380, height/2/2-50, image1, 1,1,1)

            # Arrows
            image2 = pygame.image.load("images/leftarrow.png")
            blit_image((width, height), width-1500, height/2-(height/8)-50, image2, 1,1,1)
            image3 = pygame.image.load("images/rightarrow.png")
            blit_image((width, height), width-1050, height/2-(height/8)-50, image3, 1,1,1)

            # Character name and back button
            gl_text_name(self.font, "BLACK", cgls(width-1400, width), cgls(width-1050, width), cgls(height/2/2-125, height), cgls(height/2/2-75, height), char_name, 1, .89)
            gl_text_name(self.font, color_back, cgls(width/2+100, width), cgls(width/2-100, width), cgls(height-825, height), cgls(height-875, height), "Back", 1, 2)

            # party portraits
            """
            if len(self.party) > 0:
                blit_image(SIZE, width - 100, height-825, self.party[0].get_portrait_dungeon(), 1, 1, 1)
            if len(self.party) > 1:
                blit_image(SIZE, width - 200, height-825, self.party[1].get_portrait_dungeon(), 1, 1, 1)
            if len(self.party) > 2:
                blit_image(SIZE, width - 300, height-825, self.party[2].get_portrait_dungeon(), 1, 1, 1)
            if len(self.party) > 3:
                blit_image(SIZE, width - 400, height-825, self.party[3].get_portrait_dungeon(), 1, 1, 1)
            """

            # Add/Remove party member button
            if characters[current_member] != self.main_character:
                if char_name not in party_names:
                    gl_text_name(self.font, color_party, cgls(width-100, width), cgls(width-500, width), cgls(height-825, height), cgls(height-875, height), "Add to Party", 1, 2)
                else:
                    gl_text_name(self.font, color_party, cgls(width-100, width), cgls(width-500, width), cgls(height-825, height), cgls(height-875, height), "Remove from Party", 1, 2)

            bounds = [width-800, width-50, height-50, height-800]

            # square behind the stats
            glBegin(GL_QUADS)
            rect_ogl("BLACK", cgls(bounds[0], width), cgls(bounds[1], width), cgls(bounds[2], height), cgls(bounds[3], height))
            glEnd()

            name = character_full_name(char_name)

            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 50, width), cgls(bounds[1] - 50, width), cgls(bounds[2] - 50, height), cgls(bounds[2] - 100, height), name, 1, 1)

            # stats
            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 50, width), cgls(bounds[0] + 350, width), cgls(bounds[2] - 100, height), cgls(bounds[2] - 150, height), "ROLE: " + characters[current_member].get_role(), 1, 1)
            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 350, width), cgls(bounds[0] + 700, width), cgls(bounds[2] - 100, height), cgls(bounds[2] - 150, height), "LEVEL: " + str(characters[current_member].get_level()), 1, 1)

            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 50, width), cgls(bounds[0] + 350, width), cgls(bounds[2] - 150, height), cgls(bounds[2] - 200, height), "HP: " + str(characters[current_member].get_hp()), 1, 1)
            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 350, width), cgls(bounds[0] + 700, width), cgls(bounds[2] - 150, height), cgls(bounds[2] - 200, height), "HEAL: " + str(characters[current_member].get_healing()), 1, 1)
                        
            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 50, width), cgls(bounds[0] + 350, width), cgls(bounds[2] - 200, height), cgls(bounds[2] - 250, height), "PHYSICAL: " + str(characters[current_member].get_physical_attack()), 1, 1)
            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 350, width), cgls(bounds[0] + 700, width), cgls(bounds[2] - 200, height), cgls(bounds[2] - 250, height), "MAGIC: " + str(characters[current_member].get_magic_attack()), 1, 1)

            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 50, width), cgls(bounds[0] + 350, width), cgls(bounds[2] - 250, height), cgls(bounds[2] - 300, height), "GUARD: " + str(characters[current_member].get_physical_guard()), 1, 1)
            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 350, width), cgls(bounds[0] + 700, width), cgls(bounds[2] - 250, height), cgls(bounds[2] - 300, height), "MAG GUARD: " + str(characters[current_member].get_magical_guard()), 1, 1)

            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 50, width), cgls(bounds[0] + 350, width), cgls(bounds[2] - 300, height), cgls(bounds[2] - 350, height), "QUICK: " + str(characters[current_member].get_quickness()), 1, 1)
            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 350, width), cgls(bounds[0] + 700, width), cgls(bounds[2] - 300, height), cgls(bounds[2] - 350, height), "HEART: " + str(characters[current_member].get_heartiness()), 1, 1)

            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 50, width), cgls(bounds[0] + 350, width), cgls(bounds[2] - 350, height), cgls(bounds[2] - 400, height), "CHUTZ: " + str(characters[current_member].get_chutzpah()), 1, 1)
            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 350, width), cgls(bounds[0] + 700, width), cgls(bounds[2] - 350, height), cgls(bounds[2] - 400, height), "XP: " + str(characters[current_member].get_xp()), 1, 1)

            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 50, width), cgls(bounds[0] + 350, width), cgls(bounds[2] - 475, height), cgls(bounds[2] - 450, height), "CREATURES' COMFORTS:", 1, .95)

            gl_text_name(self.font, color_switch, cgls(bounds[0] + 550, width), cgls(bounds[0] + 700, width),  cgls(bounds[2] - 475, height), cgls(bounds[2] - 450, height), "[SWITCH]", 1, .95)
            
            if switcher == 0:
                question_port = pygame.image.load("images/question_port.png")
            else:
                question_port = pygame.image.load("images/question_port.png").convert_alpha()
            question_port = pygame.transform.scale(question_port, (50,50))
            current = 0
            y = 0
            which_character = 0
            
            
            romanced = 0
            char = characters[current_member]
            bonds = char.get_bonds()
            

            # relationship portraits, dynamically shows only the other characters
            for member in which_list[switcher]:
                if member != char_name:
                    if member != None:
                        # retrieve which number party member we're talking about
                        party_member_num = which_num_party_member(member, self.main_character.get_name())

                        # calculate how many points are required to rank up
                        rank = char.get_bond_rank(party_member_num)
                        points = char.get_bond_points(party_member_num)
                        to_next = char.get_needed_to_next_rank(rank)
                        decimal = (points/to_next)
                        percentage = decimal*100

                    else:
                        decimal = 0
                        percentage = 0

                    if current % 2 == 0:
                        if member == None:
                            blit_image((width, height), bounds[0] + 50, bounds[2] - 525 + y, question_port, 1, 1, 1)
                        else:
                            image = what_list[switcher][which_character].get_portrait()
                            image = pygame.transform.scale(image, (50,50))
                            blit_image((width, height), bounds[0] + 50, bounds[2] - 525 + y, image, 1,1,1)
                            # rectangle "healthbar"-like tracking for relationship status
                            # show pink rectangle instead of green for bonded characters
                            glBegin(GL_QUADS)
                            rect_ogl(self.color_active, cgls(bounds[0]+125, width), cgls(bounds[0]+375, width), cgls(bounds[2] - 525 + y, height), cgls(bounds[2] - 475 + y, height))
                            if romanced == 1 and percentage != 0:
                                rect_ogl("PINK", cgls(bounds[0]+125, width), cgls(bounds[0]+125+(250*decimal), width), cgls(bounds[2] - 525 + y, height), cgls(bounds[2] - 475 + y, height))
                            elif percentage != 0:
                                rect_ogl("GREEN", cgls(bounds[0]+125, width), cgls(bounds[0]+125+(250*decimal), width), cgls(bounds[2] - 525 + y, height), cgls(bounds[2] - 475 + y, height))
                            glEnd()
                            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 125, width), cgls(bounds[0] + 375, width), cgls(bounds[2] - 525 + y, height), cgls(bounds[2] - 525 + y, height), "RANK " + str(rank), 1, 1)
                    else:
                        if member == None:
                            blit_image((width, height), bounds[0] + 400, bounds[2] - 525 + y, question_port, 1, 1, 1)
                        else:
                            image = what_list[switcher][which_character].get_portrait()
                            image = pygame.transform.scale(image, (50,50))
                            blit_image((width, height), bounds[0] + 400, bounds[2] - 525 + y, image, 1,1,1)
                            # rectangle "healthbar"-like tracking for relationship status
                            # show pink rectangle instead of green for bonded characters
                            glBegin(GL_QUADS)
                            rect_ogl(self.color_active, cgls(bounds[0]+475, width), cgls(bounds[0]+725, width), cgls(bounds[2] - 525 + y, height), cgls(bounds[2] - 475 + y, height))
                            if romanced == 1:
                                rect_ogl("PINK", cgls(bounds[0]+475, width), cgls(bounds[0]+475+(250*decimal), width), cgls(bounds[2] - 525 + y, height), cgls(bounds[2] - 475 + y, height))
                            else:
                                rect_ogl("GREEN", cgls(bounds[0]+475, width), cgls(bounds[0]+475+(250*decimal), width), cgls(bounds[2] - 525 + y, height), cgls(bounds[2] - 475 + y, height))
                            glEnd()
                            gl_text_name(self.font, "BLACK", cgls(bounds[0] + 475, width), cgls(bounds[0] + 725, width), cgls(bounds[2] - 525 + y, height), cgls(bounds[2] - 525 + y, height), "RANK " + str(rank), 1, 1)
                        y -= 50
                    current += 1
                which_character += 1

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
                            switcher = 0
                    if right_rect.collidepoint(event.pos):
                        if current_member+1 < len(party_member_pics):
                            current_member += 1
                        else:
                            current_member = 0
                        switcher = 0
                    if back_rect.collidepoint(event.pos):
                        return
                    if switch_rect.collidepoint(event.pos):
                        if switcher == 0:
                            switcher = 1
                        elif switcher == 1:
                            if char_name == self.main_character.get_name():
                                switcher = 0
                            else:
                                switcher = 2
                        elif switcher == 2:
                            switcher = 0
                    if party_rect.collidepoint(event.pos):
                        if characters[current_member] in self.party:
                            self.party.remove(characters[current_member])
                            self.party.append(None)
                        elif self.party[1] == None:
                            self.party[1] = characters[current_member]
                        elif self.party[2] == None:
                            self.party[2] = characters[current_member]
                        elif self.party[3] == None:
                            self.party[3] = characters[current_member]

            #glBegin(GL_QUADS)
            #rect_ogl("BLACK", cgls(width-950, width), cgls(width-650, width), cgls(height/2/2-25, height), cgls(height/2/2-75, height))
            #glEnd()
            
            pygame.display.flip()

            self.clock.tick(60)

    def options_menu(self):
        """
        The options menu, accessed from a number of different places
        Inputs: None
        Return: None
        """
        black = 0, 0, 0

        # rects for character names
        option1_rect = pygame.Rect(width-1550,height-550,700,50)
        option2_rect = pygame.Rect(width-750,height-550,700,50)
        option3_rect = pygame.Rect(width-1550,height-450,700,50)
        option4_rect = pygame.Rect(width-750,height-450,700,50)
        option5_rect = pygame.Rect(width-1550,height-350,700,50)
        option6_rect = pygame.Rect(width-750,height-350,700,50)
        option7_rect = pygame.Rect(width-1550,height-250,700,50)
        option8_rect = pygame.Rect(width-750,height-250,700,50)
        next_rect = pygame.Rect(width-1550,height-150,700,50)
        leave_rect = pygame.Rect(width-750,height-150,700,50)

        # background
        self.background = retrieve_background("options_menu")
        self.background_move = True

        while True:
            # background stuff
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)

            # set rect colors as black
            color_c1 = self.color_passive
            color_c2 = self.color_passive
            color_c3 = self.color_passive
            color_c4 = self.color_passive
            color_c5 = self.color_passive
            color_c6 = self.color_passive
            color_c7 = self.color_passive
            color_c8 = self.color_passive
            color_next = self.color_passive
            color_leave = self.color_passive

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if option1_rect.collidepoint(event.pos):
                        if self.color_active == "RED":
                            self.color_active = "BLUE"
                        elif self.color_active == "BLUE":
                            self.color_active = "GREEN"
                        elif self.color_active == "GREEN":
                            self.color_active = "RED"
                    if option2_rect.collidepoint(event.pos):
                        pass
                    if option3_rect.collidepoint(event.pos):
                        pass
                    if option4_rect.collidepoint(event.pos):
                        pass
                    if option5_rect.collidepoint(event.pos):
                        pass
                    if option6_rect.collidepoint(event.pos):
                        pass
                    if option7_rect.collidepoint(event.pos):
                        pass
                    if option8_rect.collidepoint(event.pos):
                        pass
                    if leave_rect.collidepoint(event.pos):
                        return
                    if next_rect.collidepoint(event.pos):
                        pass

            # turn red if moused over
            if option1_rect.collidepoint(pygame.mouse.get_pos()):
                color_c1 = self.color_active
            if option2_rect.collidepoint(pygame.mouse.get_pos()):
                color_c2 = self.color_active
            if option3_rect.collidepoint(pygame.mouse.get_pos()):
                color_c3 = self.color_active
            if option4_rect.collidepoint(pygame.mouse.get_pos()):
                color_c4 = self.color_active
            if option5_rect.collidepoint(pygame.mouse.get_pos()):
                color_c5 = self.color_active
            if option6_rect.collidepoint(pygame.mouse.get_pos()):
                color_c6 = self.color_active
            if option7_rect.collidepoint(pygame.mouse.get_pos()):
                color_c7 = self.color_active
            if option8_rect.collidepoint(pygame.mouse.get_pos()):
                color_c8 = self.color_active
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = self.color_active
            if next_rect.collidepoint(pygame.mouse.get_pos()):
                color_next = self.color_active

            # bulk adjustment variable to ease the process a little
            bulk_adjust_y = 1.07

            # draw names for menu
            gl_text_name(self.font, color_c1, cgls(width-1550, width), cgls(width-850, width), cgls(height-350, height), cgls(height-400, height), "Active Color: " + self.color_active, 1,  bulk_adjust_y)
            gl_text_name(self.font, color_c2, cgls(width-750, width), cgls(width-50, width), cgls(height-350, height), cgls(height-400, height), "NONE", 1,  bulk_adjust_y)
            gl_text_name(self.font, color_c3, cgls(width-1550, width), cgls(width-850, width), cgls(height-450, height), cgls(height-500, height), "NONE", 1,  bulk_adjust_y+.01)
            gl_text_name(self.font, color_c4, cgls(width-750, width), cgls(width-50, width), cgls(height-450, height), cgls(height-500, height), "NONE", 1,  bulk_adjust_y+.01)
            gl_text_name(self.font, color_c5, cgls(width-1550, width), cgls(width-850, width), cgls(height-550, height), cgls(height-600, height), "NONE", 1, 1.115)
            gl_text_name(self.font, color_c6, cgls(width-750, width), cgls(width-50, width), cgls(height-550, height), cgls(height-600, height), "NONE", 1, 1.115)
            gl_text_name(self.font, color_c7, cgls(width-1550, width), cgls(width-850, width), cgls(height-650, height), cgls(height-700, height), "NONE", 1, 1.17)
            gl_text_name(self.font, color_c8, cgls(width-750, width), cgls(width-50, width), cgls(height-650, height), cgls(height-700, height), "NONE", 1, 1.17)
            gl_text_name(self.font, color_next, cgls(width-1550, width), cgls(width-850, width), cgls(height-750, height), cgls(height-800, height), "Next", 1, 1.31)
            gl_text_name(self.font, color_leave, cgls(width-750, width), cgls(width-50, width), cgls(height-750, height), cgls(height-800, height), "Leave", 1, 1.31)

            pygame.display.flip()
            self.clock.tick(60)

    def load_dungeon(self, dungeon):
        """Loads a dungeon and sends player to the crawler mode.

        Args:
            dungeon (string): Name of the dungeon for loading purposes

        Returns:
            string: Either "WIN" or "DEAD" depending on what happens in crawler mode.
        """
        state = dungeon_crawler.Crawler(self.screen).play(self.party, get_dungeon(dungeon), dungeon, True)
        self.counter_x = 1600
        self.main_menu_fade("Habbitt", False)
        return state
        
    def fade(self, fade_image, counter_x, counter_y):
        """Handles general fading math.

        Args:
            fade_image (pygame surface): The black box to be used for fading
            counter_x (int): Int representing x location of the fade image
            counter_y (int): Int representing y location of the fade image
        """
        fade_out = 1
        while fade_out != 0:
            if fade_out == 1:
                if self.debug == 1:
                    print("Fading out | counter_x == " + str(counter_x) + " | counter_y == " + str(counter_y))
                counter_x += 256
                counter_y += 144
                circle_fade_out(self.screen, counter_x, counter_y, fade_image)
                if counter_x >= 12800 or counter_y >= 7200:
                    fade_out = 2
                    counter_x = 0
                    counter_y = 0
            elif fade_out == 2:
                if self.debug == 1:
                    print("Fading in")
                counter_x += 256
                counter_y += 144
                circle_fade_in(self.screen, counter_x, counter_y, fade_image)
                if counter_x >= 6400 or counter_y >= 3600:
                    fade_out = 0
                    counter_x = 0
                    counter_y = 0

    def determine_background(self, dialog, bg, move):
        """Determines the background that will be used based on current dialog.

        Args:
            dialog (string): Currently displayed dialog
            bg (string): Current background
            move (bool): Whether the background is currently moving

        Returns:
            Background: string representing the name of the current background to be loaded
            Move: Whether the background should be scrolling
        """
        if dialog == "Regardless of your choice, I'm taking you outside.":
            return retrieve_background("forest"), True
        elif dialog == "Maybe you should just follow that road over there until you run into something." or dialog == "To Town":
            return retrieve_background("villageinn"), False
        elif dialog == "villageinnnight" or dialog == "To Town" or dialog == "You cross what feels like an endless number of hills until you come upon a single building in a clearing.":
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
        
    def high_enough_progress_to_show_map_name(self, pnum, map_name):
        """Determines if you have high enough progress to show map name.

        Args:
            pnum (int): Progress number needed to show map
            map_name (string): Name of the map to be shown if progress is met

        Returns:
            string: Name of map if progress met, or question marks if not
        """
        if self.progress > pnum:
            return map_name
        else:
            return "???"

    def in_party(self, name):
        """Checks if a member is in the party.

        Args:
            name (string): The name of character to be checked

        Returns:
            bool: Returns True if character in party, or False if not
        """
        for member in self.party:
            if member != None:
                if member.get_name() == name:
                    return True
        return False

    def controller(self):
        """
        Controls where in the game you are relative to the main menu
        """
        while True:
            option = self.start_screen()
            #self.fade(self.fade_image, self.counter_x, self.counter_y)
            if option == "new_game":
                self.progress = 1
                self.main_menu_fade("Start_quick")
                self.in_dialog(True)
            elif option == "dialog skip":
                self.name_global = "Dogdude"
                self.progress = 2
                self.main_menu_fade("Habbitt")
                self.in_dialog(False, "To Town", 0)
            elif option == "load":
                #check if load file exists
                if os.path.isfile("save.txt") or os.path.isfile("save2.txt") or os.path.isfile("save3.txt"):
                    self.load_save_choices("LOAD")
                else:
                    print("Save file does not exist.")
            elif option == "exit":
                sys.exit()

    def load_save_choices(self, mode):
        """
        Config for loading and saving.

        Args:
            mode (string): "LOAD" or "SAVE" depending on the function

        Returns:
            None, to return to the previous menu
        """
        #### SETUP ####
        black = 0, 0, 0
        speed = [3, 0]

        self.background, self.background_move = self.determine_background("villageinnnight", None, False)

        load1_rect = pygame.Rect(width-1200,height-800,800,150)
        load2_rect = pygame.Rect(width-1200,height-550,800,150)
        load3_rect = pygame.Rect(width-1200,height-300,800,150)
        back_rect = pygame.Rect(width-900,height-100,200,50)

        while True:
            self.screen.fill(black)
            color_load1, color_load2, color_load3, color_back = self.color_passive, self.color_passive, self.color_passive, self.color_passive

            for event in pygame.event.get():                  
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mode == "LOAD":
                        if load1_rect.collidepoint(event.pos) and os.path.isfile('save.txt'):
                            return self.load_file('save.txt')
                        if load2_rect.collidepoint(event.pos) and os.path.isfile('save2.txt'):
                            return self.load_file('save2.txt')
                        if load3_rect.collidepoint(event.pos) and os.path.isfile("save3.txt"):
                            return self.load_file('save3.txt')
                        if back_rect.collidepoint(event.pos):
                            return
                    if mode == "SAVE":
                        if load1_rect.collidepoint(event.pos):
                            return self.save_game('save.txt')
                        if load2_rect.collidepoint(event.pos):
                            return self.save_game('save2.txt')
                        if load3_rect.collidepoint(event.pos):
                            return self.save_game('save3.txt')
                        if back_rect.collidepoint(event.pos):
                            return [[[None, "Your data has NOT been saved."], [None, "[Returning to town.]"]]]

            if load1_rect.collidepoint(pygame.mouse.get_pos()):
                color_load1 = self.color_active
            if load2_rect.collidepoint(pygame.mouse.get_pos()):
                color_load2 = self.color_active
            if load3_rect.collidepoint(pygame.mouse.get_pos()):
                color_load3 = self.color_active
            if back_rect.collidepoint(pygame.mouse.get_pos()):
                color_back = self.color_active

            if not os.path.isfile("save.txt"):
                color_load = "GRAY"

            if os.path.isfile('save.txt'):
                file1 = open('save.txt', 'rb')
                self.save1 = pickle.load(file1)
            if os.path.isfile('save2.txt'):
                file2 = open('save2.txt', 'rb')
                self.save2 = pickle.load(file2)
            if os.path.isfile('save3.txt'):
                file3 = open('save3.txt', 'rb')
                self.save3 = pickle.load(file3)

            self.gl_draw_load_save_screen(color_load1, color_load2, color_load3, color_back)
            self.clock.tick(60)

    def load_file(self, filename):
        """Loads a save game.

        Args:
            filename (string): The file to be loaded.
        """
        #load file
        file = open(filename, 'rb')
        self.data = pickle.load(file)
        file.close()
        #place player in location associated with progress (usually town)
        self.distribute_data()
        self.main_menu_fade("Habbitt")
        self.in_dialog(False, "Load", self.progress)

    def gl_draw_load_save_screen(self, load1c, load2c, load3c, backc):
        """Draws the save/load interface.

        Args:
            load1c (string): Color of the first load button
            load2c (string): Color of the second load button
            load3c (string): Color of the third load button
            backc (string): Color of the back button
        """
        self.i = blit_bg(self.i, self.background, self.background_move)

        # Squares
        glBegin(GL_QUADS)
        rect_ogl(load1c, cgls(width-1200, width), cgls(width-400, width), cgls(height-250, height), cgls(height-100, height))
        rect_ogl(load2c, cgls(width-1200, width), cgls(width-400, width), cgls(height-500, height), cgls(height-350, height))
        rect_ogl(load3c, cgls(width-1200, width), cgls(width-400, width), cgls(height-750, height), cgls(height-600, height))
        glEnd()

        # data to display
        if os.path.isfile('save.txt'):
            save = self.save1
            name = save[23][1]
            level = save[1][13]
            progress = save[0][0]
            progress_percent = str(round(int(progress) / 46*100, 2)) + "%"
        if os.path.isfile('save2.txt'):
            save = self.save2
            name2 = save[23][1]
            level2 = save[1][13]
            progress = save[0][0]
            progress_percent2 = str(round(int(progress) / 46*100, 2)) + "%"
        if os.path.isfile('save3.txt'):
            save = self.save3
            name3 = save[23][1]
            level3 = save[1][13]
            progress = save[0][0]
            progress_percent3 = str(round(int(progress) / 46*100, 2)) + "%"

        y_adjust = .985
        y_adjust2 = y_adjust - .005
        y_adjust3 = y_adjust2 - .01

        # text
        gl_text_name(self.font, load1c, cgls(width-700, width), cgls(width-900, width), cgls(height-150, height), cgls(height-100, height), "File 1", 1, y_adjust)
        if os.path.isfile('save.txt'):
            gl_text_name(self.font, load1c, cgls(width-700, width), cgls(width-900, width), cgls(height-200, height), cgls(height-150, height), name + ": LEVEL " + str(level) + " LEADER", 1, y_adjust)
            gl_text_name(self.font, load1c, cgls(width-700, width), cgls(width-900, width), cgls(height-250, height), cgls(height-200, height), "Progress: " + progress_percent, 1, y_adjust - .006)
        else:
            gl_text_name(self.font, load1c, cgls(width-700, width), cgls(width-900, width), cgls(height-200, height), cgls(height-150, height), "No Save Data", 1, y_adjust)
            gl_text_name(self.font, load1c, cgls(width-700, width), cgls(width-900, width), cgls(height-250, height), cgls(height-200, height), "", 1, y_adjust - .006)

        gl_text_name(self.font, load2c, cgls(width-675, width), cgls(width-925, width), cgls(height-400, height), cgls(height-350, height), "File 2", 1, y_adjust2)
        if os.path.isfile('save2.txt'):
            gl_text_name(self.font, load2c, cgls(width-700, width), cgls(width-900, width), cgls(height-450, height), cgls(height-400, height), name2 + ": LEVEL " + str(level2) + " LEADER", 1, y_adjust2 - .004)
            gl_text_name(self.font, load2c, cgls(width-700, width), cgls(width-900, width), cgls(height-500, height), cgls(height-450, height), "Progress: " + progress_percent2, 1, y_adjust2 - .015)
        else:
            gl_text_name(self.font, load2c, cgls(width-700, width), cgls(width-900, width), cgls(height-450, height), cgls(height-400, height), "No Save Data", 1, y_adjust2 - .004)
            gl_text_name(self.font, load2c, cgls(width-700, width), cgls(width-900, width), cgls(height-500, height), cgls(height-450, height), "", 1, y_adjust2 - .015)

        gl_text_name(self.font, load3c, cgls(width-700, width), cgls(width-900, width), cgls(height-650, height), cgls(height-600, height), "File 3", 1, y_adjust3 - .01)
        if os.path.isfile('save3.txt'):
            gl_text_name(self.font, load3c, cgls(width-700, width), cgls(width-900, width), cgls(height-700, height), cgls(height-650, height), name3 + ": LEVEL " + str(level3) + " LEADER", 1, y_adjust3 - .03)
            gl_text_name(self.font, load3c, cgls(width-700, width), cgls(width-900, width), cgls(height-750, height), cgls(height-700, height), "Progress: " + progress_percent3, 1, y_adjust3 - .06)
        else:
            gl_text_name(self.font, load3c, cgls(width-700, width), cgls(width-900, width), cgls(height-700, height), cgls(height-650, height), "No Save Data", 1, y_adjust3 - .03)
            gl_text_name(self.font, load3c, cgls(width-700, width), cgls(width-900, width), cgls(height-750, height), cgls(height-700, height), "", 1, y_adjust3 - .06)

        gl_text_name(self.font, backc, cgls(width-700, width), cgls(width-900, width), cgls(height-850, height), cgls(height-800, height), "Back", 1, y_adjust3-.185)

        pygame.display.flip()

    def main_menu_fade(self, skip, new_fade=True):
        """Handles the fading that the main menu does when you select
        an option.

        Args:
            skip (string): The skip, if any, that will be applied after the fade
            new_fade (bool, optional): Whether the fade is 
                continued from another or not. Defaults to True.
        """
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
        """Blits (in OpenGL) background according to the 
        location of the camera.

        Args:
            bg (str, optional): Name of background file. Defaults to "cave.png".
            move (bool, optional): Whether the background should move. Defaults to True.
        """
        background = pygame.image.load("images/" + bg).convert_alpha()
        background = pygame.transform.scale(background,(1600,900))
        blit_image([width, height], 0, 0, background, 1, 1, 1)

    def distribute_data(self):
        """Distributes the data held in a save file (txt)
        """
        if self.debug == 1:
            print(len(self.data))
            print(self.data)
        self.progress = self.data[0][0]
        for x in range(1, 22):
            c = self.characters[x-1]
            if self.data[x][12] != False:
                c.set_hp(self.data[x][0])
                c.set_physical_guard(self.data[x][1])
                c.set_magical_guard(self.data[x][2])
                c.set_physical_attack(self.data[x][3])
                c.set_magic_attack(self.data[x][4])
                c.set_quickness(self.data[x][5])
                c.set_heartiness(self.data[x][6])
                c.set_healing(self.data[x][7])
                c.set_chutzpah(self.data[x][8])
                c.set_willpower(self.data[x][9])
                c.set_xp(self.data[x][10])
                c.set_bonds(self.data[x][11])
                c.set_recruited(self.data[x][12])
                c.set_level(self.data[x][13]) 
                c.set_all_conv_comp(self.data[x][14])
        self.main_character = self.characters[0]
        self.party[0] = self.characters[self.data[22][0]] 
        if self.data[22][1] != None:
            self.party[1] = self.characters[self.data[22][1]] 
        else:
            self.party[1] = None
        if self.data[22][2] != None:
            self.party[2] = self.characters[self.data[22][2]]
        else:
            self.party[2] = None
        if self.data[22][3] != None:
            self.party[3] = self.characters[self.data[22][3]]
        else:
            self.party[3] = None
        self.mc_for_save = self.data[23]
        self.characters[0].set_name(self.mc_for_save[1])
        self.characters[0].set_pictures_mc(self.mc_for_save[0])
        self.character_names = self.data[24]
        self.npc_names = self.data[25]
        if self.debug == 1:
            print(self.mc_for_save[1])
        self.dialog = dia.Dialog(self.mc_for_save[1])

    def handle_inn_dialog(self, left, right, rank):
        """Picks a bond conversation based on the characters selected.

        Args:
            left (string): The character on the left
            right (string): The character on the right
            rank (int): _description_
        """
        l = which_num_party_member(left.get_name(), self.main_character.get_name())
        r = which_num_party_member(right.get_name(), self.main_character.get_name())
        # MC
        if l == 0 or r == 0:
            if r == 1 or l == 1:
                self.user_text = self.dialog.mc_bear_bond_dialog[rank-1]
            elif r == 2 or l == 2:
                self.user_text = self.dialog.mc_radish_bond_dialog[rank-1]
            elif r == 3 or l == 3:
                self.user_text = self.dialog.mc_grapefart_bond_dialog[rank-1]
            elif r == 4 or l == 4:
                self.user_text = self.dialog.mc_lambaste_bond_dialog[rank-1]
            elif r == 5 or l == 5:
                self.user_text = self.dialog.mc_sunny_bond_dialog[rank-1]
            elif r == 6 or l == 6:
                self.user_text = self.dialog.mc_oscar_bond_dialog[rank-1]
            elif r == 7 or l == 7:
                self.user_text = self.dialog.mc_donkey_bond_dialog[rank-1]
            elif r == 8 or l == 8:
                self.user_text = self.dialog.mc_sidney_bond_dialog[rank-1]
            elif r == 9 or l == 9:
                self.user_text = self.dialog.mc_hollow_bond_dialog[rank-1]
            elif r == 10 or l == 10:
                self.user_text = self.dialog.mc_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.mc_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.mc_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.mc_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.mc_rayna_bond_dialog[rank-1]
        # Bear
        elif l == 1 or r == 1:
            if r == 2 or l == 2:
                self.user_text = self.dialog.bear_radish_bond_dialog[rank-1]
            elif r == 3 or l == 3:
                self.user_text = self.dialog.bear_grapefart_bond_dialog[rank-1]
            elif r == 4 or l == 4:
                self.user_text = self.dialog.bear_lambaste_bond_dialog[rank-1]
            elif r == 5 or l == 5:
                self.user_text = self.dialog.bear_sunny_bond_dialog[rank-1]
            elif r == 6 or l == 6:
                self.user_text = self.dialog.bear_oscar_bond_dialog[rank-1]
            elif r == 7 or l == 7:
                self.user_text = self.dialog.bear_donkey_bond_dialog[rank-1]
            elif r == 8 or l == 8:
                self.user_text = self.dialog.bear_sidney_bond_dialog[rank-1]
            elif r == 9 or l == 9:
                self.user_text = self.dialog.bear_hollow_bond_dialog[rank-1]
            elif r == 10 or l == 10:
                self.user_text = self.dialog.bear_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.bear_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.bear_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.bear_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.bear_rayna_bond_dialog[rank-1]
        # Radish
        elif l == 2 or r == 2:
            if r == 3 or l == 3:
                self.user_text = self.dialog.radish_grapefart_bond_dialog[rank-1]
            elif r == 4 or l == 4:
                self.user_text = self.dialog.radish_lambaste_bond_dialog[rank-1]
            elif r == 5 or l == 5:
                self.user_text = self.dialog.radish_sunny_bond_dialog[rank-1]
            elif r == 6 or l == 6:
                self.user_text = self.dialog.radish_oscar_bond_dialog[rank-1]
            elif r == 7 or l == 7:
                self.user_text = self.dialog.radish_donkey_bond_dialog[rank-1]
            elif r == 8 or l == 8:
                self.user_text = self.dialog.radish_sidney_bond_dialog[rank-1]
            elif r == 9 or l == 9:
                self.user_text = self.dialog.radish_hollow_bond_dialog[rank-1]
            elif r == 10 or l == 10:
                self.user_text = self.dialog.radish_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.radish_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.radish_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.radish_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.radish_rayna_bond_dialog[rank-1]
        # Grapefart
        elif l == 3 or r == 3:
            if r == 4 or l == 4:
                self.user_text = self.dialog.grapefart_lambaste_bond_dialog[rank-1]
            elif r == 5 or l == 5:
                self.user_text = self.dialog.grapefart_sunny_bond_dialog[rank-1]
            elif r == 6 or l == 6:
                self.user_text = self.dialog.grapefart_oscar_bond_dialog[rank-1]
            elif r == 7 or l == 7:
                self.user_text = self.dialog.grapefart_donkey_bond_dialog[rank-1]
            elif r == 8 or l == 8:
                self.user_text = self.dialog.grapefart_sidney_bond_dialog[rank-1]
            elif r == 9 or l == 9:
                self.user_text = self.dialog.grapefart_hollow_bond_dialog[rank-1]
            elif r == 10 or l == 10:
                self.user_text = self.dialog.grapefart_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.grapefart_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.grapefart_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.grapefart_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.grapefart_rayna_bond_dialog[rank-1]
        # Lam'baste
        elif l == 4 or r == 4:
            if r == 5 or l == 5:
                self.user_text = self.dialog.lambaste_sunny_bond_dialog[rank-1]
            elif r == 6 or l == 6:
                self.user_text = self.dialog.lambaste_oscar_bond_dialog[rank-1]
            elif r == 7 or l == 7:
                self.user_text = self.dialog.lambaste_donkey_bond_dialog[rank-1]
            elif r == 8 or l == 8:
                self.user_text = self.dialog.lambaste_sidney_bond_dialog[rank-1]
            elif r == 9 or l == 9:
                self.user_text = self.dialog.lambaste_hollow_bond_dialog[rank-1]
            elif r == 10 or l == 10:
                self.user_text = self.dialog.lambaste_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.lambaste_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.lambaste_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.lambaste_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.lambaste_rayna_bond_dialog[rank-1]
        # Sunny
        elif l == 5 or r == 5:
            if r == 6 or l == 6:
                self.user_text = self.dialog.sunny_oscar_bond_dialog[rank-1]
            elif r == 7 or l == 7:
                self.user_text = self.dialog.sunny_donkey_bond_dialog[rank-1]
            elif r == 8 or l == 8:
                self.user_text = self.dialog.sunny_sidney_bond_dialog[rank-1]
            elif r == 9 or l == 9:
                self.user_text = self.dialog.sunny_hollow_bond_dialog[rank-1]
            elif r == 10 or l == 10:
                self.user_text = self.dialog.sunny_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.sunny_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.sunny_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.sunny_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.sunny_rayna_bond_dialog[rank-1]
        # Oscar
        elif l == 6 or r == 6:
            if r == 7 or l == 7:
                self.user_text = self.dialog.oscar_donkey_bond_dialog[rank-1]
            elif r == 8 or l == 8:
                self.user_text = self.dialog.oscar_sidney_bond_dialog[rank-1]
            elif r == 9 or l == 9:
                self.user_text = self.dialog.oscar_hollow_bond_dialog[rank-1]
            elif r == 10 or l == 10:
                self.user_text = self.dialog.oscar_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.oscar_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.oscar_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.oscar_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.oscar_rayna_bond_dialog[rank-1]
        # Donkey Hote
        elif l == 7 or r == 7:
            if r == 8 or l == 8:
                self.user_text = self.dialog.donkey_sidney_bond_dialog[rank-1]
            elif r == 9 or l == 9:
                self.user_text = self.dialog.donkey_hollow_bond_dialog[rank-1]
            elif r == 10 or l == 10:
                self.user_text = self.dialog.donkey_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.donkey_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.donkey_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.donkey_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.donkey_rayna_bond_dialog[rank-1]
        # Sidney Shark
        elif l == 8 or r == 8:
            if r == 9 or l == 9:
                self.user_text = self.dialog.sidney_hollow_bond_dialog[rank-1]
            elif r == 10 or l == 10:
                self.user_text = self.dialog.sidney_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.sidney_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.sidney_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.sidney_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.sidney_rayna_bond_dialog[rank-1]
        # Hollow
        elif l == 9 or r == 9:
            if r == 10 or l == 10:
                self.user_text = self.dialog.hollow_gol_bond_dialog[rank-1]
            elif r == 11 or l == 11:
                self.user_text = self.dialog.hollow_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.hollow_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.hollow_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.hollow_rayna_bond_dialog[rank-1]
        # Giver of Life
        elif l == 10 or r == 10:
            if r == 11 or l == 11:
                self.user_text = self.dialog.gol_henrietta_bond_dialog[rank-1]
            elif r == 12 or l == 12:
                self.user_text = self.dialog.gol_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.gol_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.gol_rayna_bond_dialog[rank-1]
        # Henrietta
        elif l == 11 or r == 11:
            if r == 12 or l == 12:
                self.user_text = self.dialog.bear_grilla_bond_dialog[rank-1]
            elif r == 13 or l == 13:
                self.user_text = self.dialog.bear_dane_bond_dialog[rank-1]
            elif r == 14 or l == 14:
                self.user_text = self.dialog.bear_rayna_bond_dialog[rank-1]
        # Grilla
        elif l == 12 or r == 12:
            if l == 13 or r == 13:
                self.user_text = self.dialog.grilla_dane_bond_dialog[rank-1]
            elif l == 14 or r == 14:
                self.user_text = self.dialog.grilla_rayna_bond_dialog[rank-1]
        if self.debug == 1:
            print(self.user_text)
        self.in_dialog(False, False, self.progress)
        left.set_conversation_completeness(right.get_name(), self.main_character.get_name(), rank)
        right.set_conversation_completeness(left.get_name(), self.main_character.get_name(), rank)

if __name__ == "__main__":
    # Does the same thing as main.py does
    print("Creatures of Habbitt Version Alpha 1")
    MainGame().controller()



