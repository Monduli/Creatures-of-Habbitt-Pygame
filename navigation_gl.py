import sys, pygame, os
import dialog as dia
import classes
from helpers import *
import match
from classes import *
import crawler
import pickle

SIZE = width, height = 1600, 900

class MainGame():
    def __init__(self):
        pygame.init()
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
        self.color_passive = "BLACK" 
        self.color_active = "RED"
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        self.boosted = 0

    def start_screen(self):
        #### SETUP ####
        pygame.display.set_caption("Creatures of Habbitt v.01")
        
        black = 0, 0, 0
        speed = [3, 0]

        
        self.background, self.background_move = self.determine_background("villageinnnight", None, False)
        
        title_rect = pygame.Rect(width-1100,height-800,500,50)
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
        speed = [3, 0]
        black = 0, 0, 0

        if self.background == None:
            self.background = retrieve_background("cave")

        self.user_text = [[[None, "[Character creation]"]
        ], "intro_3_quick"]

        self.advance = 0

        dialog_rect = pygame.Rect(width-1550,height-250, 1500, 200)
        name_rect = pygame.Rect(width-1550, height-320, 300, 50)

        remove = ["VIZGONE", "GUARDGONE", "MYSTBEARGONE", "HENRIETTAGONE"]

        self.slots = [0, 0, 0]

        curr_text = self.user_text[0][self.advance][1]
        if curr_text in ["inn"]:
            choice = self.inn_menu()

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

            # add mc to party
            self.party.append(self.main_character)

            # create n steen
            self.nsteen.set_name("N. Steen")
            self.nsteen.set_portrait_dungeon("bear")

            # add n steen to party by default
            self.party.append(self.nsteen)

            # set dialog MC variable to name of MC for replacement
            self.dialog = dia.Dialog(self.main_character.get_name())
            
            # find the next dialog
            self.user_text = self.dialog.determine_dialog(self.user_text[1], self.progress, self.char_name)
            self.advance = 0

            # create lists with romance characters and npcs for later use
            self.rom_characters = [self.main_character, self.nsteen, None, None, None, None, None, None, None, None, None]
            self.character_names = [self.main_character.get_name(), self.nsteen.get_name(), None, None, None, None, None, None, None, None, None]
            self.characters = []

            # add all characters that we have so far into "self.characters" array for later
            for char in self.rom_characters:
                if char != None:
                    self.characters.append(char)
            
            # create and add Henrietta as we will rescue her before returning to town the first time
            self.npc_names = ["Henrietta", None, None, None, None, None, None, None, None, None]
            henrietta = Innkeeper([15, 10, 10, 10, 10, 10])
            henrietta.set_name("Henrietta")
            henrietta.set_portrait("hippo_port_100.png")
            self.npc_characters = [henrietta, None, None, None, None, None, None, None, None, None]

            # same as above
            for char in self.npc_characters:
                if char != None:
                    self.characters.append(char)
            return
        
        # start the fade if [Dungeon CAVE] is dialog
        elif self.user_text[0][self.advance][1] == "[Dungeon CAVE]":
            self.fade_over = 1

        # add n. steen to party if dialog says to (deprecated)
        elif self.user_text[0][self.advance][1] == "[Bear N. Steen has joined your party.]":
            self.party.append(add_party_member("nsteen"))

        # open town menu
        elif self.user_text[0][self.advance][1] in ["Please select a destination.", "[Returning to town.]", "To Town"]:
            self.village_choices()
            self.slots = [0, 0, 0]

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
        Display choices for village menu 
        inputs: None
        return: None
        """
        self.habbitt_music = pygame.mixer.Sound("audio/bgm/habbittnature.wav")
        self.habbitt_music.set_volume(0)
        self.habbitt_music.play(-1)
        # retrieve background
        self.background, self.background_move = self.determine_background("Habbitt", self.background, self.background_move)

        # if progress is 1 (Context: Deprecated, before Henrietta retrieved)
        if self.progress == 1:
            # MENU:
            # Inn       || ???
            # Add Party || Save
            #           || Venture Out
            options = ["Inn", "???", "inn", None, "Save", "Add Party", "save", "party_debug", "Venture Out", "leave"]
            choice = self.town_options(options)
            # Add party members
            if choice == "party_debug":
                self.party = fill_party()
                self.user_text = [[[None, "Added party members."], [None, "[Returning to town.]"]]]
                self.advance = 0
            # Try to enter the inn (nobody to run it)
            elif choice == "inn":
                self.user_text = [[[None, "There is currently no one to run the inn."], [None, "[Returning to town.]"]]]
                self.advance = 0
            # Try to leave town (no party members)
            elif choice == "leave":
                self.user_text = [[[None, "You shouldn't go out alone. Maybe someone in the inn can help you?"], [None, "[Returning to town.]"]]]
                self.advance = 0
            # Save the game
            elif choice == "save":
                self.user_text = self.save_game()
                self.advance = 0
        # MENU:
            # Inn           || Smithy
            # Boost Party   || Save
            #               || Venture Out
        elif self.progress == 2:
            options = ["Inn", "Smithy", "inn", "blacksmith", "Haberdashery", "Save", "haberdashery", "save", "Venture Out", "leave",]
            choice = self.town_options(options)
            # Add all current characters and then boost them to 9999
            if choice == "party_debug":
                if self.boosted == 1:
                    self.user_text = [[[None, "Party has already been boosted."], [None, "[Returning to town.]"]]]
                    self.advance = 0
                else:
                    # give party of MC, Bear, Radish, Grapefart, lvl9999
                    self.party = boost_party()
                    # add chars to rom list and name list
                    self.rom_characters[2] = self.party[2]
                    self.rom_characters[3] = self.party[3]
                    self.character_names[2] = "Radish"
                    self.character_names[3] = "Grapefart"

                    # generate 2 npc characters, add to npc and name lists
                    self.npc_characters[2] = add_char("dane")
                    self.npc_characters[3] = add_char("rayna")
                    self.npc_names[2] = "Dane"
                    self.npc_names[3] = "Rayna"
                    
                    # return confirm text
                    self.user_text = [[[None, "Added party members."], [None, "[Returning to town.]"]]]
                    self.advance = 0
                    self.boosted = 1
            # No blacksmith to run yet
            if choice == "blacksmith":
                self.user_text = [[[None, "There is no one to run the blacksmith, so it remains closed."], [None, "[Returning to town.]"]]]
                self.advance = 0

            if choice == "haberdashery":
                self.user_text = [[[None, "There is no one to run the accessories shop, so it remains closed."], [None, "[Returning to town.]"]]]
                self.advance = 0
            
            # Inn menu loads because Henrietta is retrieved by prog2
            elif choice == "inn":
                choice = self.inn_menu()
                self.user_text = self.dialog.determine_dialog(choice, self.progress, self.char_name)
                self.advance = 0

            # save game (TODO: Broken)
            elif choice == "save":
                self.user_text = self.save_game()
                self.advance = 0

            # Open dungeons menu and process result
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
        """
        Saves game using Pickle module (TODO: Currently crashes the game)
        Input: None
        Returns: user_text for save game
        """
        if not os.path.isfile("save.txt"):
            file = open('save.txt', 'x')
            file.close()
        file = open('save.txt', 'wb')
        self.data = [self.progress, self.party]
        pickle.dump(self.data, file)
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
        text_leave, target_leave = options[8], options[9]

        # for screen fill
        black = 0, 0, 0

        # rectangles representing clickable space
        party_rect = pygame.Rect(width-300,height-900,300,50)
        top_left_rect = pygame.Rect(width-1550,height-350,700,50)
        top_right_rect = pygame.Rect(width-750,height-350,700,50)
        bot_left_rect = pygame.Rect(width-1550,height-250,700,50)
        bot_right_rect = pygame.Rect(width-750,height-250,700,50)
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
            gl_text_name(self.font, color_leave, cgls(width-750, width), cgls(width-50, width), cgls(height-750, height), cgls(height-800, height), text_leave, 1, 1.31)
            gl_text_name(self.font, color_party, cgls(width-300, width), cgls(width-0, width), cgls(height-50, height), cgls(height, height), "Party", 1, .99)

            pygame.display.flip()
            self.clock.tick(60)

    def inn_menu(self):
        """
        The conversations menu when you click "Inn" from Habbit screen
        TODO: This needs to be overhauled so you can start conversations as characters other than the MC
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

        back_rect = pygame.Rect(width/2-100, height-75, 200, 50)

        # remove mc from rom list or else it's uneven
        rom_no_mc = self.rom_characters.copy()
        rom_no_mc.remove(self.main_character)

        # add mc to their own list
        mc_what_list = [self.main_character]

        # make list out of lists for each character
        what_list = [rom_no_mc, self.npc_characters, mc_what_list]
        characters_left = []

        # make a list that has all party member pictures and a separate list with all
        # characters that do not equal "None"
        party_member_pics = []
        for x in what_list:
            for member in x:
                if member != None:
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

            # Make back rectangle red if you hover over it
            if back_rect.collidepoint(pygame.mouse.get_pos()):
                color_back = self.color_active

            # Name of current party member
            char_name_left = characters_left[current_member_left].get_name()

            # Party member portrait
            image1 = party_member_pics[current_member_left]
            if char_name_left in ["Henrietta", "N. Steen"]:
                blit_image((width, height), width-1470, height/2/2-50, image1, 1,1,1)
            elif char_name_left in ["Dane", "Rayna", self.main_character.get_name(), "Radish", "Grapefart"]:
                blit_image((width, height), width-1430, height/2/2-50, image1, 1,1,1)
            else:    
                blit_image((width, height), width-1380, height/2/2-50, image1, 1,1,1)

            # Name of current party member
            char_name_right = characters_left[current_member_right].get_name()

            # Party member portrait
            image2 = party_member_pics[current_member_right]
            if char_name_right in ["Henrietta", "N. Steen"]:
                blit_image((width, height), width-630, height/2/2-50, image2, 1,1,1)
            elif char_name_right in ["Dane", "Rayna", self.main_character.get_name(), "Radish", "Grapefart"]:
                blit_image((width, height), width-590, height/2/2-50, image2, 1,1,1)
            else:    
                blit_image((width, height), width-540, height/2/2-50, image2, 1,1,1)

            image2 = pygame.image.load("images/leftarrow.png")
            blit_image((width, height), width-1500, height/2-(height/8)-50, image2, 1,1,1)
            blit_image((width, height), width-650, height/2-(height/8)-50, image2, 1,1,1)
            image3 = pygame.image.load("images/rightarrow.png")
            blit_image((width, height), width-1050, height/2-(height/8)-50, image3, 1,1,1)
            blit_image((width, height), width-200, height/2-(height/8)-50, image3, 1,1,1)

            gl_text_name(self.font, "BLACK", cgls(width-1400, width), cgls(width-1050, width), cgls(height/2/2-125, height), cgls(height/2/2-75, height), char_name_left, 1, .89)
            gl_text_name(self.font, "BLACK", cgls(width-200, width), cgls(width-550, width), cgls(height/2/2-125, height), cgls(height/2/2-75, height), char_name_right, 1, .89)
            gl_text_name(self.font, color_back, cgls(width/2+100, width), cgls(width/2-100, width), cgls(height-825, height), cgls(height-875, height), "Back", 1, 2)

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

        while True:
            # fill screen to cover up previous elements and assign black to all the buttons
            self.screen.fill(black)
            self.i = blit_bg(self.i, self.background, self.background_move)
            colors = ["BLACK" for x in range(0,8)]
            color_c1, color_c2, color_c3, color_c4, color_c5, color_c6, color_c7, color_c8, color_next, color_leave = colors[0], colors[1], colors[2], colors[3], colors[4], colors[5], colors[6], colors[7], self.color_passive, self.color_passive

            # assign maps to buttons based on page
            # process map checks if you have the progress assigned and otherwise returns ???
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

            # add dungeons to an array
            dungeons = [dungeon_1, dungeon_2, dungeon_3, dungeon_4, dungeon_5, dungeon_6, dungeon_7, dungeon_8]

            # click events
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

            # make buttons red if you hover over them
            if dungeon_1_rect.collidepoint(pygame.mouse.get_pos()):
                color_c1 = self.color_active
            if dungeon_2_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 1:
                color_c2 = self.color_active
            if dungeon_3_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 2:
                color_c3 = self.color_active
            if dungeon_4_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 3:
                color_c4 = self.color_active
            if dungeon_5_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 4:
                color_c5 = self.color_active
            if dungeon_6_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 5:
                color_c6 = self.color_active
            if dungeon_7_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 6:
                color_c7 = self.color_active
            if dungeon_8_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 7:
                color_c8 = self.color_active
            if next_rect.collidepoint(pygame.mouse.get_pos()) and self.progress > 7:
                color_next = self.color_active
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = self.color_active

            # handy variable for text position adjustments (y)
            bulk_adjust_y = 1.07

            # create visual buttons and text
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
                        char = MainCharacter([10,10,10,10,10,10])
                        char.set_name(input_text[:-1])
                        char.set_dialog_picture(poss_images[curr_image] + "_port.png")
                        char.set_portrait(poss_images[curr_image] + "_port_100.png")
                        char.set_portrait_dungeon(poss_images[curr_image])
                        char.set_portrait_dialog(poss_images[curr_image] + "_portrait")
                        char.set_stats_picture(poss_images[curr_image] + "_port_stats")
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
            elif char_name in ["Dane", "Rayna", "Radish", "Grapefart", self.main_character.get_name()]:
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
                        party_member_num = which_num_party_member_bonds(member, self.main_character.get_name())

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
                        elif len(self.party) < 4:
                            self.party.append(characters[current_member])

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
        state = crawler.Crawler(self.screen).play(self.party, get_dungeon(dungeon), "cave", True)
        self.counter_x = 1600
        self.main_menu_fade("Habbitt", False)
        return state

    def sort_options(self, choice):
        if choice == "martial_choice":
            prof = classes.Martial([12,10,10,10,10,10])
            prof.set_name(self.name_global) 
            return ["class", prof]
        elif choice == "bookish_choice":
            prof = classes.Bookish([10,10,10,12,10,10])
            prof.set_name(self.name_global)
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
        
    def process_map(self, pnum, map_name):
        if self.progress > pnum:
            return map_name
        else:
            return "???"

    def in_party(self, name):
        for member in self.party:
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
                self.name_global = "Dan"
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



