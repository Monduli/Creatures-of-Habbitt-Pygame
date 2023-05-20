from helpers import * 
import pygame as pyg
from OpenGL.GL import *
from OpenGL.GLU import *

size = width, height = 1600, 900

class RancherMinigame():

    def __init__(self):
        self.background = "ranchbg.png"
        self.clock = pygame.time.Clock()

    def standalone(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():                  
                if event.type == pygame.QUIT: sys.exit()
            self.show_screen()
            self.clock.tick(60)

    def show_screen(self):
        black = 0, 0, 0
        self.screen.fill(black)
        blit_bg(0, self.background, False)

        # draw pets

        # draw info pane
        glBegin(GL_QUADS)
        rect_ogl("BLACK", cgls(39, width), cgls(439, width), cgls(39, height), cgls(858, height))
        glEnd()

        pygame.display.flip()

if __name__ == "__main__":
    ranch = RancherMinigame()
    ranch.standalone()
