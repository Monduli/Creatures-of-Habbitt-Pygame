from helpers import * 
import pygame as pyg
from OpenGL.GL import *
from OpenGL.GLU import *

size = width, height = 1600, 900

class PetCharacter():

    def __init__(self, img):
        to_convert = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(to_convert, (88,89))
        self.coords = [0, 0]

    def get_coords(self):
        return self.coords
    
    def get_image(self):
        return self.image
    
    def set_squares(self, squares):
        self.squares = squares
    
    def set_rect(self):
        self.rect = pygame.rect.Rect(self.squares[self.coords[0]][self.coords[1]][0], self.squares[self.coords[0]][self.coords[1]][1], 88, 89)

    def draw(self):
        c = self.coords
        blit_image(size, self.squares[c[0]][c[1]][0], self.squares[c[0]][c[1]][1], self.image, 1,1,1)

    def move(self, target):
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

    def __init__(self):
        pygame.init()
        self.background = "ranchbg.png"
        self.clock = pygame.time.Clock()
        self.debug = 0
        self.selected = None
        self.font = pygame.font.Font("font/VCR.001.ttf", 32)
        self.weather = "Sunny"

    def standalone(self):
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
        pet1 = PetCharacter("images/rancher/illusium.png")
        self.run([pet1])
        

    def run(self, pets = None, screen = None):
        if screen != None:
            self.screen = screen
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
                        for rect in rects:
                            if rect[1].collidepoint(pygame.mouse.get_pos()):
                                target = rect[0]
            if pygame.time.get_ticks() - timer > 200 and target != None:
                pets[0].move(target)
                timer = pygame.time.get_ticks()
                if target == pets[0].get_coords():
                    target = None

            self.show_screen()
            self.draw_pets(pets)
            pygame.display.flip()
            self.clock.tick(60)

    def show_screen(self):
        black = 0, 0, 0
        self.screen.fill(black)
        blit_bg(0, self.background, False)

        # draw pets

        # draw info pane
        glBegin(GL_QUADS)
        rect_ogl("BLACK", cgls(39, width), cgls(439, width), cgls(239, height), cgls(858, height))

        rect_ogl("BLACK", cgls(39, width), cgls(119, width), cgls(139, height), cgls(219, height))
        rect_ogl("BLACK", cgls(39, width), cgls(119, width), cgls(119, height), cgls(39, height))

        rect_ogl("BLACK", cgls(144, width), cgls(224, width), cgls(139, height), cgls(219, height))
        rect_ogl("BLACK", cgls(144, width), cgls(224, width), cgls(119, height), cgls(39, height))

        rect_ogl("BLACK", cgls(254, width), cgls(334, width), cgls(139, height), cgls(219, height))
        rect_ogl("BLACK", cgls(254, width), cgls(334, width), cgls(119, height), cgls(39, height))

        rect_ogl("BLACK", cgls(359, width), cgls(439, width), cgls(139, height), cgls(219, height))
        rect_ogl("BLACK", cgls(359, width), cgls(439, width), cgls(119, height), cgls(39, height))

        glEnd()

        if self.selected == None:
            gl_text_name(self.font, "BLACK", cgls(39, width), cgls(439, width), cgls(808, height), cgls(858, height), "Ranch Information", 1, 1)

    def draw_pets(self, pets):
        for pet in pets:
            pet.draw()

    def test_pets(self, squares):
        for x in squares:
            for y in x:
                image = pygame.image.load("images/rancher/illusium.png").convert_alpha()
                scaled = pygame.transform.scale(image, (88,89))
                blit_image(size, y[0], y[1], scaled, 1,1,1)

if __name__ == "__main__":
    ranch = RancherMinigame()
    ranch.standalone()
