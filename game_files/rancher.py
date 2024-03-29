from helpers import * 
import pygame as pyg
from OpenGL.GL import *
from OpenGL.GLU import *

size = width, height = 1600, 900

class PetCharacter():

    def __init__(self, img):
        """
        The function initializes an object with an image, converts it to an alpha surface, scales it to
        a specific size, and sets the initial coordinates to (0, 0).
        
        :param img: The `img` parameter is the file path of the image that you want to load and use for
        the object
        """
        to_convert = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(to_convert, (88,89))
        self.coords = [0, 0]

    def get_coords(self):
        """
        The function returns the coordinates of an object.
        :return: The method is returning the value of the "coords" attribute.
        """
        return self.coords
    
    def get_image(self):
        """
        The function returns the image attribute of an object.
        :return: The image attribute of the object.
        """
        return self.image
    
    def set_squares(self, squares):
        """
        The function sets the value of the "squares" attribute of an object.
        
        :param squares: The "squares" parameter is a list of square objects
        """
        self.squares = squares
    
    def set_rect(self):
        """
        The function sets the rectangle attributes of an object using the coordinates and dimensions
        provided.
        """
        self.rect = pygame.rect.Rect(self.squares[self.coords[0]][self.coords[1]][0], self.squares[self.coords[0]][self.coords[1]][1], 88, 89)

    def draw(self):
        """
        The function "draw" is used to draw a pet by blitting an image onto a specified coordinate.
        """
        c = self.coords
        blit_image(size, self.squares[c[0]][c[1]][0], self.squares[c[0]][c[1]][1], self.image, 1,1,1)

    def move(self, target):
        """
        The function moves an object towards a target by adjusting its x and y coordinates.
        
        :param target: The "target" parameter is a tuple containing the x and y coordinates of the
        target location
        """
        # x
        if target[0] < self.coords[0]:
            self.coords[0] -= 1
        elif target[0] > self.coords[0]:
            self.coords[0] += 1

        # y
        if target[1] < self.coords[1]:
            self.coords[1] -= 1
        elif target[1] > self.coords[1]:
            self.coords[1] += 1

class RancherMinigame():

    def __init__(self, screen):
        """
        The function initializes various attributes for a game screen, including the background image,
        clock, debug mode, selected item, font, and weather.
        
        :param screen: The "screen" parameter is the surface object representing the game window or
        screen on which the game will be displayed. It is typically created using the
        pygame.display.set_mode() function
        """
        self.screen = screen
        self.background = "ranchbg.png"
        self.clock = pygame.time.Clock()
        self.debug = 0
        self.selected = None
        self.font = pygame.font.Font("font/VCR.001.ttf", 32)
        self.weather = "Sun"

    def standalone(self):
        """
        The function initializes Pygame, sets up the screen, creates a PetCharacter object, and runs the
        game loop.
        """
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
        pet1 = PetCharacter("images/rancher/illusium.png")
        self.run([pet1])
        

    def run(self, pets = None, screen = None):
        """
        The `run` function takes in `pets` and `screen` as optional parameters, sets up a grid of
        squares, handles user input, and updates the screen with the pets' positions.
        
        :param pets: The `pets` parameter is a list of pet objects. Each pet object represents a pet in
        the game and has various attributes and methods associated with it
        :param screen: The `screen` parameter is used to specify the screen on which the game will be
        displayed. It is an optional parameter, and if not provided, the default screen will be used
        :return: The code does not explicitly return anything.
        """
        if screen != None:
            self.screen = screen
        self.pets = pets
        x = 455
        y = 39
        add_x = 91.4
        add_y = 91.4
        squares = [
            [(x, y), (x+add_x, y), (x+add_x*2, y), (x+add_x*3, y), (x+add_x*4, y), (x+add_x*5, y), (x+add_x*6, y), (x+add_x*7, y), (x+add_x*8, y), (x+add_x*9, y), (x+add_x*10, y), (x+add_x*11, y)],
            [(x, y+add_y), (x+add_x, y+add_y), (x+add_x*2, y+add_y), (x+add_x*3, y+add_y), (x+add_x*4, y+add_y), (x+add_x*5, y+add_y), (x+add_x*6, y+add_y), (x+add_x*7, y+add_y), (x+add_x*8, y+add_y), (x+add_x*9, y+add_y), (x+add_x*10, y+add_y), (x+add_x*11, y+add_y)],
            [(x, y+add_y*2), (x+add_x, y+add_y*2), (x+add_x*2, y+add_y*2), (x+add_x*3, y+add_y*2), (x+add_x*4, y+add_y*2), (x+add_x*5, y+add_y*2), (x+add_x*6, y+add_y*2), (x+add_x*7, y+add_y*2), (x+add_x*8, y+add_y*2), (x+add_x*9, y+add_y*2), (x+add_x*10, y+add_y*2), (x+add_x*11, y+add_y*2)],
            [(x, y+add_y*3), (x+add_x, y+add_y*3), (x+add_x*2, y+add_y*3), (x+add_x*3, y+add_y*3), (x+add_x*4, y+add_y*3), (x+add_x*5, y+add_y*3), (x+add_x*6, y+add_y*3), (x+add_x*7, y+add_y*3), (x+add_x*8, y+add_y*3), (x+add_x*9, y+add_y*3), (x+add_x*10, y+add_y*3), (x+add_x*11, y+add_y*3)],
            [(x, y+add_y*4), (x+add_x, y+add_y*4), (x+add_x*2, y+add_y*4), (x+add_x*3, y+add_y*4), (x+add_x*4, y+add_y*4), (x+add_x*5, y+add_y*4), (x+add_x*6, y+add_y*4), (x+add_x*7, y+add_y*4), (x+add_x*8, y+add_y*4), (x+add_x*9, y+add_y*4), (x+add_x*10, y+add_y*4), (x+add_x*11, y+add_y*4)],
            [(x, y+add_y*5), (x+add_x, y+add_y*5), (x+add_x*2, y+add_y*5), (x+add_x*3, y+add_y*5), (x+add_x*4, y+add_y*5), (x+add_x*5, y+add_y*5), (x+add_x*6, y+add_y*5), (x+add_x*7, y+add_y*5), (x+add_x*8, y+add_y*5), (x+add_x*9, y+add_y*5), (x+add_x*10, y+add_y*5), (x+add_x*11, y+add_y*5)],
            [(x, y+add_y*6), (x+add_x, y+add_y*6), (x+add_x*2, y+add_y*6), (x+add_x*3, y+add_y*6), (x+add_x*4, y+add_y*6), (x+add_x*5, y+add_y*6), (x+add_x*6, y+add_y*6), (x+add_x*7, y+add_y*6), (x+add_x*8, y+add_y*6), (x+add_x*9, y+add_y*6), (x+add_x*10, y+add_y*6), (x+add_x*11, y+add_y*6)],
            [(x, y+add_y*7), (x+add_x, y+add_y*7), (x+add_x*2, y+add_y*7), (x+add_x*3, y+add_y*7), (x+add_x*4, y+add_y*7), (x+add_x*5, y+add_y*7), (x+add_x*6, y+add_y*7), (x+add_x*7, y+add_y*7), (x+add_x*8, y+add_y*7), (x+add_x*9, y+add_y*7), (x+add_x*10, y+add_y*7), (x+add_x*11, y+add_y*7)],
            [(x, y+add_y*8), (x+add_x, y+add_y*8), (x+add_x*2, y+add_y*8), (x+add_x*3, y+add_y*8), (x+add_x*4, y+add_y*8), (x+add_x*5, y+add_y*8), (x+add_x*6, y+add_y*8), (x+add_x*7, y+add_y*8), (x+add_x*8, y+add_y*8), (x+add_x*9, y+add_y*8), (x+add_x*10, y+add_y*8), (x+add_x*11, y+add_y*8)]
        ]

        # create rects
        rects = []
        z = 0
        for x in range(len(squares)):
            for y in range(len(squares[0])):
                nums_x = [8,7,6,5,4,3,2,1,0]
                rects.append([[nums_x[x],y], pygame.rect.Rect(squares[x][y][0], squares[x][y][1], 91.4, 91.4)])

        back_rect = pygame.rect.Rect(39, 781, 400, 80)

        for pet in pets:
            pet.set_squares(squares)

        target = None
        current_positions = [[0, 0]]
        timer = pygame.time.get_ticks()
        while True:
            coords_1 = squares[current_positions[0][0]][current_positions[0][1]]
            coords_list = [coords_1]
            for event in pygame.event.get():                  
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #if return_rect.collidepoint(event.pos):
                    #    return "RAN"
                    if event.button == 1:
                        if self.debug == 1:
                            pos = pygame.mouse.get_pos()
                            print(pos)
                        if back_rect.collidepoint(pygame.mouse.get_pos()):
                            return
                        for rect in rects:
                            if rect[1].collidepoint(pygame.mouse.get_pos()):
                                target = rect[0]
            if pygame.time.get_ticks() - timer > 200 and target != None:
                pets[0].move(target)
                timer = pygame.time.get_ticks()
                if target == pets[0].get_coords():
                    target = None

            hlb = "BLACK"
            if back_rect.collidepoint(pygame.mouse.get_pos()):
                hlb = "RED"

            self.show_screen(hlb)
            self.draw_pets(pets)
            pygame.display.flip()
            self.clock.tick(60)

    def show_screen(self, hlb):
        """
        The function `show_screen` is responsible for displaying the game screen with various elements
        such as background, pets, and information pane.
        
        :param hlb: The parameter "hlb" stands for "highlight_back" and it represents the color used to
        highlight the background of the text
        """
        highlight_back = hlb
        black = 0, 0, 0
        self.screen.fill(black)
        blit_bg(0, self.background, False)

        # draw pets

        # draw info pane
        glBegin(GL_QUADS)
        rect_ogl("BLACK", cgls(39, width), cgls(439, width), cgls(339, height), cgls(858, height))

        rect_ogl("BLACK", cgls(39, width), cgls(119, width), cgls(239, height), cgls(319, height))
        rect_ogl("BLACK", cgls(39, width), cgls(119, width), cgls(219, height), cgls(139, height))

        rect_ogl("BLACK", cgls(144, width), cgls(224, width), cgls(239, height), cgls(319, height))
        rect_ogl("BLACK", cgls(144, width), cgls(224, width), cgls(219, height), cgls(139, height))

        rect_ogl("BLACK", cgls(254, width), cgls(334, width), cgls(239, height), cgls(319, height))
        rect_ogl("BLACK", cgls(254, width), cgls(334, width), cgls(219, height), cgls(139, height))

        rect_ogl("BLACK", cgls(359, width), cgls(439, width), cgls(239, height), cgls(319, height))
        rect_ogl("BLACK", cgls(359, width), cgls(439, width), cgls(219, height), cgls(139, height))

        glEnd()

        if self.selected == None:
            gl_text_name(self.font, "BLACK", cgls(39, width), cgls(439, width), cgls(808, height), cgls(858, height), "Ranch Information", 1, 1)
            gl_text_name(self.font, "BLACK", cgls(39, width), cgls(439, width), cgls(758, height), cgls(808, height), "Weather: " + self.weather, 1, 1)
            gl_text_name(self.font, "BLACK", cgls(39, width), cgls(439, width), cgls(708, height), cgls(758, height), "Pets Present: " + str(len(self.pets)), 1, 1)
            gl_text_name(self.font, highlight_back, cgls(39, width), cgls(439, width), cgls(119, height), cgls(39, height), "Return to Town", 1, 1.8)

    def draw_pets(self, pets):
        """
        The function "draw_pets" takes a list of pets and calls the "draw" method on each pet.
        
        :param pets: A list of pet objects that need to be drawn
        """
        for pet in pets:
            pet.draw()

    def test_pets(self, squares):
        """
        The function "test_pets" loads an image, scales it, and then blits it onto a surface.
        
        :param squares: The "squares" parameter is a list of lists. Each inner list represents a square
        and contains two elements: the x-coordinate and the y-coordinate of the square
        """
        for x in squares:
            for y in x:
                image = pygame.image.load("images/rancher/illusium.png").convert_alpha()
                scaled = pygame.transform.scale(image, (88,89))
                blit_image(size, y[0], y[1], scaled, 1,1,1)

if __name__ == "__main__":
    ranch = RancherMinigame()
    ranch.standalone()
