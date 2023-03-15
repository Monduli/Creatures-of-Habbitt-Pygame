import sys, pygame, os
import dialog as dia
import classes
from helpers import *
import match
from classes import *
import crawler

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
        self.fade_out = 0
        self.fade_image = pygame.image.load("images/circlefade.png")
        self.i = 0
        self.font = pygame.font.Font("font/VCR.001.ttf", 32)
        self.level = 0

    def start_screen(self):

        #### SETUP ####
        
        pygame.display.set_caption("Creatures of Habbitt v.01")
        
        black = 0, 0, 0
        speed = [3, 0]

        clock = pygame.time.Clock()

        color_passive = "BLACK"
        
        self.background = retrieve_background("cave")
        
        title_rect = pygame.Rect(width-1100,height-800,500,50)
        start_rect = pygame.Rect(width-900,height-550,200,50)
        town_start_rect = pygame.Rect(width-900,height-475,200,50)
        options_rect = pygame.Rect(width-900,height-400,200,50)
        exit_rect = pygame.Rect(width-850,height-250,100,50)

        i = 0

        while True:
            self.screen.fill(black)
            color_start, color_town_start, color_options, color_exit = color_passive, color_passive, color_passive, color_passive
            color_exit = "BLACK"

            for event in pygame.event.get():                  
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        return "dialog"
                    if town_start_rect.collidepoint(event.pos):
                        return "dialog skip"
                    if exit_rect.collidepoint(event.pos):
                        return "exit"

            if start_rect.collidepoint(pygame.mouse.get_pos()):
                color_start = "RED"
            if town_start_rect.collidepoint(pygame.mouse.get_pos()):
                color_town_start = "RED"
            if options_rect.collidepoint(pygame.mouse.get_pos()):
                color_options = "RED"
            if exit_rect.collidepoint(pygame.mouse.get_pos()):
                color_exit = "RED"

            self.gl_draw_start_screen(color_passive, color_start, color_town_start, color_options, color_exit)
            clock.tick(60)

    def gl_draw_start_screen(self, cp, c1, c2, c3, c4):
        self.i = blit_bg(self.i)

        glBegin(GL_QUADS)
        # Draw buttons
        #pygame.draw.rect(self.screen, color_passive, title_rect)
        # width-1100,height-800,500,50
        rect_ogl(cp, cgls(width-500, width), cgls(width-1100, width), cgls(height-100, height), cgls(height-150, height))
        #pygame.draw.rect(self.screen, color_start, start_rect)
        #pygame.draw.rect(self.screen, color_town_start, town_start_rect)
        #pygame.draw.rect(self.screen, color_options, options_rect)
        #pygame.draw.rect(self.screen, color_exit, exit_rect)
        rect_ogl(c1, cgls(width-700, width), cgls(width-900, width), cgls(height-350, height), cgls(height-400, height))
        rect_ogl(c2, cgls(width-650, width), cgls(width-950, width), cgls(height-425, height), cgls(height-475, height))
        rect_ogl(c3, cgls(width-700, width), cgls(width-900, width), cgls(height-500, height), cgls(height-550, height))
        rect_ogl(c4, cgls(width-700, width), cgls(width-900, width), cgls(height-650, height), cgls(height-700, height))

        glEnd()
        
        # Draw the text onto the buttons
        #drawText(self.screen, "Creatures of Habbitt v.01", (255,255,255), title_rect, base_font, center=True)
        #drawText(self.screen, "Wake Up", (255,255,255), start_rect, base_font, center=True)
        #drawText(self.screen, "Skip to Town", (255,255,255), town_start_rect, base_font, center=True)
        #drawText(self.screen, "Options", (255,255,255), options_rect, base_font, center=True)
        #drawText(self.screen, "Exit", (255,255,255), exit_rect, base_font, center=True)

        gl_text(self.font, "BLACK",  cgls(width-500, width), cgls(width-1100, width), cgls(height-150, height), cgls(height-100, height), "Creatures of Habbitt v.01", .88, .982)
        gl_text(self.font, c1, cgls(width-700, width), cgls(width-900, width), cgls(height-400, height), cgls(height-350, height), "Wake Up", .955,.975)
        gl_text(self.font, c2, cgls(width-650, width), cgls(width-950, width), cgls(height-475, height), cgls(height-425, height), "Skip to Town", .95,.97)
        gl_text(self.font, c3, cgls(width-700, width), cgls(width-900, width), cgls(height-550, height), cgls(height-500, height), "Options", .95,.97)
        gl_text(self.font, c4, cgls(width-700, width), cgls(width-900, width), cgls(height-700, height), cgls(height-650, height), "Exit", .92,.95)

        pygame.display.flip()

    def in_dialog(self, skip=None):

        #### SETUP ####
        size = width, height = 1600, 900
        speed = [3, 0]
        black = 0, 0, 0

        clock = pygame.time.Clock()

        self.background = retrieve_background("cave")

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)
        self.user_text = dia.intro_1

        dialog_rect = pygame.Rect(width-1550,height-250, 1500, 200)
        name_rect = pygame.Rect(width-1550, height-320, 300, 50)
        color_passive = pygame.Color('black')

        remove = ["VIZGONE", "GUARDGONE", "MYSTBEARGONE"]

        i = 0
        global progress
        global party
        party = []
        slots = [0, 0, 0]

        curr_text = self.user_text[0][self.advance][1]
        if curr_text in ["inn"]:
            choice = self.inn_menu(self.screen, progress, retrieve_background("tavern"))

        if skip:
            self.user_text = [[[None, "To Town"]]]

        while True:            
            self.pick_dialog()            
            self.screen.fill(black)
            self.i = blit_bg(self.i)
                
            if slots != [0,0,0]:
                print(slots)    
            if slots[0] != 0:
                character = retrieve_character(slots[0], self.main_character)
                blit_image(self.screen, width-1500, 100, character, 1,1,1)
            if slots[1] != 0:
                character = retrieve_character(slots[1], self.main_character)
                if slots[1] == "N. Steen" or slots[1] == "Mysterious Bear":
                    blit_image(self.screen, width/2-300, 0, character, 1,1,1)
                else:
                    blit_image(self.screen, width/2-150, 0, character, 1,1,1)
            if slots[2] != 0:
                character = retrieve_character(slots[2], self.main_character)
                if slots[2] == "N. Steen" or slots[2] == "Mysterious Bear":
                    blit_image(self.screen, width - (width/2/2)-300, 0, character, 1,1,1)
                else:
                    blit_image(self.screen, width - (width/2/2), 0, character, 1,1,1)
            if slots[1] != 0 and slots[2] == 0:
                slots[2] = slots[1]
                slots[1] = 0

            speaking_name = self.user_text[0][self.advance][0]
            if speaking_name != None:
                if speaking_name in remove:
                    slots = remove_portrait(speaking_name, slots)
                else:
                    gl_text(self.font, "BLACK", cgls(width-1550, width), cgls(width-1250, width), cgls(height-320, height), cgls(height-270, height), speaking_name, 1.055, .982)
                    # Arg 1 is the name of the character to be portraited, Arg 2 is always main character
                    character = retrieve_character(speaking_name, self.main_character)
                    # slots[0] is left, slots[1] is middle, slots[2] is right
                    if slots[0] == 0 and slots[1] != speaking_name and slots[2] != speaking_name:
                        slots[0] = speaking_name
                    elif slots[2] == 0 and slots[0] != speaking_name and slots[1] != speaking_name:
                        slots[2] = speaking_name
                    elif slots[1] == 0 and slots[0] != speaking_name and slots[2] != speaking_name:
                        slots[1] = speaking_name

            # (width-1550,height-250,1500,200)
            #glBegin(GL_QUADS)
            #rect_ogl("BLACK", cgls(width-1550, width), cgls(width-50, width), cgls(height-650, height), cgls(height-850, height))
            #glEnd()
            gl_text_wrap_dialog(self.font, "BLACK", cgls(width-1550, width), cgls(width-50, width), cgls(height-650, height), cgls(height-850, height), self.user_text[0][self.advance][1], .7, 2.15, self.level)

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
            self.screen.blit(self.background, (width+i,0))
            self.screen.blit(self.background, (i, 0))
            color_left = pygame.Color('black')
            color_right = pygame.Color('black')

            if (i == -width):
                self.screen.blit(self.background, (width+i, 0))
                i=0
            i-=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if left_rect.collidepoint(event.pos):
                        return target_left
                    if right_rect.collidepoint(event.pos):
                        return target_right
                
            if left_rect.collidepoint(pygame.mouse.get_pos()):
                color_left = pygame.Color(200,0,0)
            if right_rect.collidepoint(pygame.mouse.get_pos()):
                color_right = pygame.Color(200,0,0)

            pygame.draw.rect(self.screen, color_left, left_rect)
            drawText(self.screen, text_left, (255,255,255), left_rect, base_font)
            pygame.draw.rect(self.screen, color_right, right_rect)
            drawText(self.screen, text_right, (255,255,255), right_rect, base_font)

            pygame.display.flip()
            clock.tick(60)       

    def pick_dialog(self):
        self.background, self.background_move = self.determine_background(self.user_text[0][self.advance][1], self.background, self.background_move)
        if self.exit_next == 1:
            sys.exit()
        elif self.user_text[0][self.advance][1] == "[Character creation]":
            self.main_character = self.character_creator()
            print(self.main_character)
            self.party.append(self.main_character)
            self.user_text = dia.determine_dialog(self.user_text[1], self.progress, self.char_name)
            self.advance = 0
            return
        elif self.user_text[0][self.advance][1] == "[Dungeon CAVE]":
            self.party.append(add_party_member("nsteen"))
            print(self.party)
            state = self.load_dungeon(self.user_text[1])
            self.user_text = dia.process_state("cave_dungeon", state)
        elif self.user_text[0][self.advance][1] == "[Bear N. Steen has joined your party.]":
            self.party.append(add_party_member("nsteen"))
        elif self.user_text[0][self.advance][1] in ["Please select a destination.", "[Returning to town.]", "To Town"]:
            if self.progress == 1:
                options = ["Inn", "???", "inn", None, "???", "Add Party", None, "party_debug", "Venture Out", "leave"]
                choice = self.town_options(self.screen, options, self.background)
                if choice == "party_debug":
                    party = fill_party()
                    self.user_text = [[[None, "Added party members."], [None, "[Returning to town.]"]]]
                    self.advance = 0
                if choice == "inn":
                    self.user_text = [[[None, "There is currently no one to run the inn."], [None, "[Returning to town.]"]]]
                    self.advance = 0
                if choice == "leave":
                    self.user_text = [[[None, "You shouldn't go out alone. Maybe someone in the inn can help you?"], [None, "[Returning to town.]"]]]
                    self.advance = 0
            elif progress == 2:
                options = ["Inn", "Smithy", "inn", "blacksmith", "???", "???", None, None, "Venture Out", "leave",]
                choice = self.town_options(self.screen, options, self.background)
                if choice == "blacksmith":
                    self.user_text = [[[None, "There is no one to run the blacksmith, so it remains closed."], [None, "[Returning to town.]"]]]
                    self.advance = 0
                elif choice == "inn":
                    choice = self.inn_menu(self.screen, progress, retrieve_background("tavern"))
                    self.user_text = dia.determine_dialog(choice, progress, self.char_name)
                    self.advance = 0
                elif choice == "leave":
                    if len(party) > 0:
                    # Should go to location menu
                        state = self.location_menu()
                        if state == "WIN":
                            self.user_text = [[[None, "Your party was victorious!"],[None, "[Returning to town.]"]]]
                        elif state == "DEAD":
                            self.user_text = [[[None, "Your party was wiped out..."],[None, "[Returning to town.]"]]]
                        elif state == "RAN" or "LEFT":
                            self.user_text = [[[None, "[Returning to town.]"]]]
                        self.advance = 0
        elif self.user_text[0][self.advance][1] == "[You leave him to his devices.]" or self.user_text[0][self.advance][1] == "[You leave her to her devices.]":
            choice = self.inn_menu(self.screen, progress, self.background)
            self.user_text = dia.determine_dialog(choice, progress, self.char_name)
            self.advance = 0
        elif self.user_text[0][self.advance][1] == "SELECTION":
            left_option = self.user_text[0][self.advance+1][1]
            right_option = self.user_text[0][self.advance+2][1]
            left_target = self.user_text[1]
            right_target = self.user_text[2]
            choice = self.dialog_options(self.screen, left_option, right_option, left_target, right_target)
            proceed = self.sort_options(choice)
            self.user_text = dia.determine_dialog(choice, progress, self.char_name)
            self.advance = 0
        elif self.user_text[0][self.advance][1] == "Please type into the box.":
            array = self.input_box(self.user_text[1], self.background)
            temp = self.user_text[1]
            self.user_text, name = array[0], array[1]
            global name_global
            name_global = name
            self.sort_options(temp)
            self.advance = 0
        else:
            pass


    def town_options(self, screen, options, background):

        text_top_left, text_top_right, target_top_left, target_top_right = options[0], options[1], options[2], options[3]
        text_bot_left, text_bot_right, target_bot_left, target_bot_right = options[4], options[5], options[6], options[7]
        text_leave, target_leave = options[8], options[9]
        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)

        color_passive = pygame.Color('black')

        top_left_rect = pygame.Rect(width-1550,height-350,700,50)
        top_right_rect = pygame.Rect(width-750,height-350,700,50)
        bot_left_rect = pygame.Rect(width-1550,height-250,700,50)
        bot_right_rect = pygame.Rect(width-750,height-250,700,50)
        leave_rect = pygame.Rect(width-750,height-150,700,50)

        while True:
            self.screen.fill(black)
            self.screen.blit(self.background, (0,0))
            color_top_left = color_passive
            color_top_right = color_passive
            color_bot_left = color_passive
            color_bot_right = color_passive
            color_leave = color_passive

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

            if top_left_rect.collidepoint(pygame.mouse.get_pos()):
                color_top_left = pygame.Color(200,0,0)
            if top_right_rect.collidepoint(pygame.mouse.get_pos()):
                color_top_right = pygame.Color(200,0,0) 
            if bot_left_rect.collidepoint(pygame.mouse.get_pos()):
                color_bot_left = pygame.Color(200,0,0)
            if bot_right_rect.collidepoint(pygame.mouse.get_pos()):
                color_bot_right = pygame.Color(200,0,0)
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = pygame.Color(200,0,0)

            pygame.draw.rect(self.screen, color_top_left, top_left_rect)
            drawText(self.screen, text_top_left, (255,255,255), top_left_rect, base_font)
            pygame.draw.rect(self.screen, color_top_right, top_right_rect)
            drawText(self.screen, text_top_right, (255,255,255), top_right_rect, base_font)
            pygame.draw.rect(self.screen, color_bot_left, bot_left_rect)
            drawText(self.screen, text_bot_left, (255,255,255), bot_left_rect, base_font)
            pygame.draw.rect(self.screen, color_bot_right, bot_right_rect)
            drawText(self.screen, text_bot_right, (255,255,255), bot_right_rect, base_font)
            pygame.draw.rect(self.screen, color_leave, leave_rect)
            drawText(self.screen, text_leave, (255,255,255), leave_rect, base_font)


            pygame.display.flip()
            clock.tick(60)

    def inn_menu(self, screen, progress, background):

        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)

        color_passive = pygame.Color('black')

        title_rect = pygame.Rect(width-1500,height-800,1400,50)
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

        self.background = retrieve_background("tavern")

        while True:
            self.screen.fill(black)
            self.screen.blit(self.background, (0,0))
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
                        if progress >= 3:
                            return "radish"
                    if character3_rect.collidepoint(event.pos):
                        if progress >= 3:
                            return "radish"
                    if character4_rect.collidepoint(event.pos):
                        if progress >= 3:
                            return "radish"
                    if character5_rect.collidepoint(event.pos):
                        if progress >= 3:
                            return "radish"
                    if character6_rect.collidepoint(event.pos):
                        if progress >= 3:
                            return "radish"
                    if character7_rect.collidepoint(event.pos):
                        if progress >= 3:
                            return "radish"
                    if character8_rect.collidepoint(event.pos):
                        if progress >= 3:
                            return "radish"
                    if leave_rect.collidepoint(event.pos):
                        return "town"
                    if next_rect.collidepoint(event.pos):
                        pass

            if character1_rect.collidepoint(pygame.mouse.get_pos()):
                color_c1 = pygame.Color(200,0,0)
            if character2_rect.collidepoint(pygame.mouse.get_pos()):
                color_c2 = pygame.Color(200,0,0) 
            if character3_rect.collidepoint(pygame.mouse.get_pos()):
                color_c3 = pygame.Color(200,0,0)
            if character4_rect.collidepoint(pygame.mouse.get_pos()):
                color_c4 = pygame.Color(200,0,0)
            if character5_rect.collidepoint(pygame.mouse.get_pos()):
                color_c5 = pygame.Color(200,0,0)
            if character6_rect.collidepoint(pygame.mouse.get_pos()):
                color_c6 = pygame.Color(200,0,0) 
            if character7_rect.collidepoint(pygame.mouse.get_pos()):
                color_c7 = pygame.Color(200,0,0)
            if character8_rect.collidepoint(pygame.mouse.get_pos()):
                color_c8 = pygame.Color(200,0,0)
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = pygame.Color(200,0,0)
            if next_rect.collidepoint(pygame.mouse.get_pos()):
                color_next = pygame.Color(200,0,0)

            global party
            pygame.draw.rect(self.screen, color_passive, title_rect)
            pygame.draw.rect(self.screen, color_c1, character1_rect)
            pygame.draw.rect(self.screen, color_c2, character2_rect)
            pygame.draw.rect(self.screen, color_c3, character3_rect)
            pygame.draw.rect(self.screen, color_c4, character4_rect)
            pygame.draw.rect(self.screen, color_c5, character5_rect)
            pygame.draw.rect(self.screen, color_c6, character6_rect)
            pygame.draw.rect(self.screen, color_c7, character7_rect)
            pygame.draw.rect(self.screen, color_c8, character8_rect)
            pygame.draw.rect(self.screen, color_next, next_rect)
            pygame.draw.rect(self.screen, color_leave, leave_rect)

            drawText(self.screen, "Who would you like to speak to?", (255,255,255), title_rect, base_font)

            drawText(self.screen, "Bear N. Steen", (255,255,255), character1_rect, base_font)

            if self.in_party("Radish"):
                drawText(self.screen, "Radish Rabbit", (255,255,255), character2_rect, base_font)
            else:
                drawText(self.screen, "???", (255,255,255), character2_rect, base_font)

            if self.in_party("Cinna"):
                drawText(self.screen, "Cinnamon Bun", (255,255,255), character3_rect, base_font)
            else:
                drawText(self.screen, "???", (255,255,255), character3_rect, base_font)

            if self.in_party("Grapefart"):
                drawText(self.screen, "Gilbert Grapefart", (255,255,255), character4_rect, base_font)
            else:
                drawText(self.screen, "???", (255,255,255), character4_rect, base_font)

            if self.in_party("???"):
                drawText(self.screen, "Name", (255,255,255), character5_rect, base_font)
            else:
                drawText(self.screen, "???", (255,255,255), character5_rect, base_font)

            if self.in_party("???"):
                drawText(self.screen, "Name", (255,255,255), character6_rect, base_font)
            else:
                drawText(self.screen, "???", (255,255,255), character6_rect, base_font)

            if self.in_party("???"):
                drawText(self.screen, "Name", (255,255,255), character7_rect, base_font)
            else:
                drawText(self.screen, "???", (255,255,255), character7_rect, base_font)

            if self.in_party("???"):
                drawText(self.screen, "Name", (255,255,255), character8_rect, base_font)
            else:
                drawText(self.screen, "???", (255,255,255), character8_rect, base_font)

            drawText(self.screen, "Next", (255,255,255), next_rect, base_font)
            drawText(self.screen, "Leave", (255,255,255), leave_rect, base_font)

            pygame.display.flip()
            clock.tick(60)

    def input_box(self, target, background):
        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)

        color_passive = pygame.Color('black')

        i = 0

        self.user_text = ''
        
        # create rectangle
        input_rect = pygame.Rect(width-750, height/2, 200, 50)
        input_rect.center = (width/2, height/2)

        color_active = pygame.Color('red')

        color = color_passive
        
        active = False
        
        while True:
            self.screen.fill(black)
            self.screen.blit(self.background, (width+i,0))
            self.screen.blit(self.background, (i, 0))

            if (i == -width):
                self.screen.blit(self.background, (width+i, 0))
                i=0
            i-=1
            for event in pygame.event.get():
        
            # if user types QUIT then the self.screen will close
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
        
                if event.type == pygame.KEYDOWN:
        
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
        
                        # get text input from 0 to -1 i.e. end.
                        self.user_text = self.user_text[:-1]
        
                    # Unicode standard is used for string
                    # formation
                    else:
                        self.user_text += event.unicode
                    
                    if event.key == pygame.K_RETURN:
                        return [dia.determine_dialog(target, 0, self.user_text[:-1]), self.user_text[:-1]]
        
            if active:
                color = color_active
            else:
                color = color_passive
                
            # draw rectangle and argument passed which should
            # be on self.screen
            pygame.draw.rect(self.screen, color, input_rect)
        
            rect = drawText(self.screen, self.user_text, pygame.Color('white'), input_rect, base_font, center=True, input=True)
            
            # set width of textfield so that text cannot get
            # outside of user's text input
            if rect != None:
                input_rect.w = max(100, rect.get_width()+10)
                input_rect.center = (width/2, height/2)
            
            # display.flip() will update only a portion of the
            # self.screen to updated, not full area
            pygame.display.flip()
            
            # clock.tick(60) means that for every second at most
            # 60 frames should be passed.
            clock.tick(60)

    def location_menu(self):
        size = width, height = 1600, 900
        clock = pygame.time.Clock()
        black = 0, 0, 0
        progress = self.progress

        base_font = pygame.font.Font("font/VCR.001.ttf", 32)

        color_passive = pygame.Color('black')
        page = 1
        self.background = retrieve_background("map")

        dungeon_1_rect = pygame.Rect(width-1550,height-350,700,50)
        dungeon_2_rect = pygame.Rect(width-750,height-350,700,50)
        dungeon_3_rect = pygame.Rect(width-1550,height-250,700,50)
        dungeon_4_rect = pygame.Rect(width-750,height-250,700,50)
        leave_rect = pygame.Rect(width-750,height-150,700,50)

        while True:
            self.screen.fill(black)
            self.screen.blit(self.background, (0,0))
            color_top_left = color_passive
            color_top_right = color_passive
            color_bot_left = color_passive
            color_bot_right = color_passive
            color_leave = color_passive

            if page == 1:
                dungeon_1 = "Cave"
                dungeon_2 = self.process_map(1, "Temple")
                dungeon_3 = self.process_map(2, "Grassland")
                dungeon_4 = self.process_map(3, "Forest")
            else:
                dungeon_1 = "Error"
                dungeon_2 = "Error"
                dungeon_3 = "Error"
                dungeon_4 = "Error"

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if dungeon_1_rect.collidepoint(event.pos):
                        return self.load_dungeon("cave")
                    if dungeon_2_rect.collidepoint(event.pos) and progress > 1:
                        return self.load_dungeon("Temple")
                    if dungeon_3_rect.collidepoint(event.pos) and progress > 2:
                        return self.load_dungeon("Grasslands")
                    if dungeon_4_rect.collidepoint(event.pos) and progress > 3:
                        return self.load_dungeon("Forest")
                    if leave_rect.collidepoint(event.pos):
                        return "LEFT"

            if dungeon_1_rect.collidepoint(pygame.mouse.get_pos()):
                color_top_left = pygame.Color(200,0,0)
            if dungeon_2_rect.collidepoint(pygame.mouse.get_pos()) and progress > 1:
                color_top_right = pygame.Color(200,0,0) 
            if dungeon_3_rect.collidepoint(pygame.mouse.get_pos()) and progress > 2:
                color_bot_left = pygame.Color(200,0,0)
            if dungeon_4_rect.collidepoint(pygame.mouse.get_pos()) and progress > 3:
                color_bot_right = pygame.Color(200,0,0)
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = pygame.Color(200,0,0)

            pygame.draw.rect(self.screen, color_top_left, dungeon_1_rect)
            drawText(self.screen, dungeon_1, (255,255,255), dungeon_1_rect, base_font)
            pygame.draw.rect(self.screen, color_top_right, dungeon_2_rect)
            drawText(self.screen, dungeon_2, (255,255,255), dungeon_2_rect, base_font)
            pygame.draw.rect(self.screen, color_bot_left, dungeon_3_rect)
            drawText(self.screen, dungeon_3, (255,255,255), dungeon_3_rect, base_font)
            pygame.draw.rect(self.screen, color_bot_right, dungeon_4_rect)
            drawText(self.screen, dungeon_4, (255,255,255), dungeon_4_rect, base_font)
            pygame.draw.rect(self.screen, color_leave, leave_rect)
            drawText(self.screen, "Leave", (255,255,255), leave_rect, base_font)

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
            self.i = blit_bg(self.i)

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
                        char.set_portrait(poss_images[curr_image] + "_port_100.png")
                        char.set_portrait_dungeon(poss_images[curr_image])
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
        
            rect = gl_text(self.font, "BLACK", cgls(width-650, width), cgls(width-950, width), cgls(height/2/2-75, height), cgls(height/2/2-25, height), input_text, .96, .93)
            
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


    def load_dungeon(self, dungeon):
        state = crawler.Crawler(self.screen).play(self.party, get_dungeon(dungeon), "cave")
        self.screen = pygame.display.set_mode((width, height))
        return state

    def sort_options(self, choice):
        if choice == "martial_choice":
            prof = classes.Martial([12,10,10,10,10,10])
            prof.set_name = name_global 
            return ["class", prof]
        elif choice == "bookish_choice":
            prof = classes.Bookish([10,10,10,12,10,10])
            prof.set_name(name_global )
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
        elif dialog == "Ah, yes. Here we are! Welcome to Habbitt.":
            return retrieve_background("villageinnnight"), True
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
        global name_global
        global progress
        progress = 1
        while True:
            option = self.start_screen()
            #self.fade(self.fade_image, self.counter_x, self.counter_y)
            if option == "dialog":
                self.in_dialog()
            elif option == "dialog skip":
                name_global = "Dan"
                self.in_dialog("To Town")
            elif option == "exit":
                sys.exit()

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



