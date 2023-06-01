from helpers import * 
import pygame as pyg
from OpenGL.GL import *
from OpenGL.GLU import *

class EquipmentMenu():

    def __init__(self, function, standalone=False):
        if standalone != False:
            pygame.init()
        self.background = "ranchbg.png"
        self.clock = pygame.time.Clock()
        self.debug = 0
        self.selected = None
        self.font = pygame.font.Font("font/VCR.001.ttf", 32)
        self.function = function
        self.level = 0
        self.items = []
        self.database = []

    def standalone(self):
        """
        Runs if this file is run by itself.
        """
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.OPENGL)
        self.run()

    def pull_proper_list(self):
        """
        Loads the proper list depending on if this menu is for accessories or weaponsmithing.
        """
        if self.function == "ACC":
            # Load accessories list to create haberdash menu
            # TODO: Create the actual categories for accessories, these are placeholders
            self.items = ["Circlets", "Bracelets", "Watches", "Earrings", "Necklaces", "Crystals", "Rings", "Adornments"]
            self.database = [
                # Swords
                [], 
                # Staves
                [],
                # Shields
                [],
                # Wands
                [],
                # Daggers
                [],
                # Flasks
                [],
                # Instruments
                []
            ]

        elif self.function == "WEP":
            # Load weapons list to create smithing menu
            self.items = ["Swords", "Staves", "Shields", "Wands", "Daggers", "Flasks", "Instruments", "Hammers"]
            self.database = [
                # Swords
                [], 
                # Staves
                [],
                # Shields
                [],
                # Wands
                [],
                # Daggers
                [],
                # Flasks
                [],
                # Instruments
                []
            ]

    def run(self, screen = None):
        """
        The main code of equipmentmenu
        screen = pygame screen that everything is blitted to
        """
        self.pull_proper_list()
        if screen != None:
            self.screen = screen

        black = 0, 0, 0
        self.color_passive = "BLACK"
        self.color_active = "RED"

        type_1_rect = pygame.Rect(width-1550,height-550,700,50)
        type_2_rect = pygame.Rect(width-750,height-550,700,50)
        type_3_rect = pygame.Rect(width-1550,height-450,700,50)
        type_4_rect = pygame.Rect(width-750,height-450,700,50)
        type_5_rect = pygame.Rect(width-1550,height-350,700,50)
        type_6_rect = pygame.Rect(width-750,height-350,700,50)
        type_7_rect = pygame.Rect(width-1550,height-250,700,50)
        type_8_rect = pygame.Rect(width-750,height-250,700,50)
        next_rect = pygame.Rect(width-1550,height-150,700,50)
        leave_rect = pygame.Rect(width-750,height-150,700,50)

        colors = ["BLACK" for x in range(8)]

        while True:

            self.screen.fill(black)

            color_c1, color_c2, color_c3, color_c4, color_c5, color_c6, color_c7, color_c8, color_next, color_leave = colors[0], colors[1], colors[2], colors[3], colors[4], colors[5], colors[6], colors[7], self.color_passive, self.color_passive
            color_diff = self.color_passive

            # pygame events
            for event in pygame.event.get():                  
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #if return_rect.collidepoint(event.pos):
                    #    return "RAN"
                    if event.button == 1:
                        if self.debug == 1:
                            pos = pygame.mouse.get_pos()
                            print(pos)
                        if leave_rect.collidepoint(pygame.mouse.get_pos()):
                            return

            if type_1_rect.collidepoint(pygame.mouse.get_pos()):
                color_c1 = self.color_active
            if type_2_rect.collidepoint(pygame.mouse.get_pos()):
                color_c2 = self.color_active
            if type_3_rect.collidepoint(pygame.mouse.get_pos()):
                color_c3 = self.color_active
            if type_4_rect.collidepoint(pygame.mouse.get_pos()):
                color_c4 = self.color_active
            if type_5_rect.collidepoint(pygame.mouse.get_pos()):
                color_c5 = self.color_active
            if type_6_rect.collidepoint(pygame.mouse.get_pos()):
                color_c6 = self.color_active
            if type_7_rect.collidepoint(pygame.mouse.get_pos()):
                color_c7 = self.color_active
            if type_8_rect.collidepoint(pygame.mouse.get_pos()):
                color_c8 = self.color_active
            if next_rect.collidepoint(pygame.mouse.get_pos()):
                color_next = self.color_active
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                color_leave = self.color_active

            colors_move = [color_c1, color_c2, color_c3, color_c4, color_c5, color_c6, color_c7, color_c8, color_next, color_leave]
            self.display_menu(colors_move)
                            

    def display_menu(self, colors):
        """
        Draws the menu (OpenGL)
        colors = colors of the menu items which are set in run
        """

        blit_bg(0, "blacksmith.png", False)

        items = self.items
        # handy variable for text position adjustments (y)
        bulk_adjust_y = 1.07

        black_text = False

        # create visual buttons and text
        # gl_text_name(self.font, color_diff, cgls(width-750, width), cgls(width-50, width), cgls(height-150, height), cgls(height-100, height), "Difficulty: " + self.difficulty, 1, .98)
        gl_text_name(self.font, self.color_passive, cgls(width-1000, width), cgls(width-600, width), cgls(height-100, height), cgls(height-50, height), "What'll it be?", 1,  .985, black_text)
        gl_text_name(self.font, colors[0], cgls(width-1550, width), cgls(width-850, width), cgls(height-350, height), cgls(height-400, height), items[0], 1,  bulk_adjust_y, black_text)
        gl_text_name(self.font, colors[1], cgls(width-750, width), cgls(width-50, width), cgls(height-350, height), cgls(height-400, height), items[1], 1,  bulk_adjust_y, black_text)
        gl_text_name(self.font, colors[2], cgls(width-1550, width), cgls(width-850, width), cgls(height-450, height), cgls(height-500, height), items[2], 1,  bulk_adjust_y+.02, black_text)
        gl_text_name(self.font, colors[3], cgls(width-750, width), cgls(width-50, width), cgls(height-450, height), cgls(height-500, height), items[3], 1,  bulk_adjust_y+.02, black_text)
        gl_text_name(self.font, colors[4], cgls(width-1550, width), cgls(width-850, width), cgls(height-550, height), cgls(height-600, height), items[4], 1, 1.115, black_text)
        gl_text_name(self.font, colors[5], cgls(width-750, width), cgls(width-50, width), cgls(height-550, height), cgls(height-600, height), items[5], 1, 1.115, black_text)
        gl_text_name(self.font, colors[6], cgls(width-1550, width), cgls(width-850, width), cgls(height-650, height), cgls(height-700, height), items[6], 1, 1.17, black_text)
        gl_text_name(self.font, colors[7], cgls(width-750, width), cgls(width-50, width), cgls(height-650, height), cgls(height-700, height), items[7], 1, 1.17, black_text)
        gl_text_name(self.font, colors[8], cgls(width-1550, width), cgls(width-850, width), cgls(height-750, height), cgls(height-800, height), "Next", 1, 1.31, black_text)
        gl_text_name(self.font, colors[9], cgls(width-750, width), cgls(width-50, width), cgls(height-750, height), cgls(height-800, height), "Leave", 1, 1.31, black_text)

        pygame.display.flip()


if __name__ == "__main__":
    # create equipmentmenu
    menu = EquipmentMenu("WEP", True)
    # run standalone version
    menu.standalone()
