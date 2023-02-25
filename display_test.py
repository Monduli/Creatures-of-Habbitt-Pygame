import os
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from helpers import *
import numpy as np

ESCAPE = '\033'
texture = 0

A_TEX_NUMBER = None
B_TEX_NUMBER = None

FONT_SIZE = 36
debug = 0

class GameTest():
    def __init__(self, w, h):
        pygame.init()
        pygame.display.set_mode((w, h), pygame.DOUBLEBUF|pygame.OPENGL)
        pygame.display.set_caption("Creatures of Habbitt v.01")
        A_TEX_NUMBER = self.generate_texture_for_text("a")
        B_TEX_NUMBER = self.generate_texture_for_text("b")
        #glEnable(GL_TEXTURE_2D)
        #glMatrixMode(GL_PROJECTION)
        #gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
        #glMatrixMode(GL_MODELVIEW)
        self.font = pygame.font.Font('font/VCR.001.ttf', FONT_SIZE)

    def play(self):
        OGL_RED = 1.0, 0.0, 0.0, 1.0
        OGL_BLUE = 0.0, 0.0, 1.0, 1.0
        OGL_GREEN = 0.0, 1.0, 0.0, 1.0

        glClearColor(1.0, 1.0, 0.0, 1.0)

        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            self.draw_gl_scene()

            glFlush()
            clock.tick(60)

        pygame.quit()
        quit()

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
            if debug == 1:
                print("Drew triangle at vertices " + str(vertex_pair[0]) + " and " + str(vertex_pair[1]) + ".")

    def generate_texture_for_text(self, text):
        font = pygame.font.Font("font/VCR.001.ttf", FONT_SIZE)
        textSurface = font.render(text, True, (255,255,255,255), (0,0,0,255))
        ix, iy = textSurface.get_width(), textSurface.get_height()
        image = pygame.image.tostring(textSurface, "RGBX", True)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        i = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, i)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        return i
    
    def draw_gl_scene(self):
        #glLoadIdentity()
        #glTranslatef(0.0,0.0,-10.0)
        

        self.shape_color("BLACK")
        # party 1
        self.gl_text("BLACK", .4, 1, .9, 1, "N. Steen", 0.88, 1.045)
        self.gl_text("BLACK",.4, 1, .8, .9, "HP: 10/10", 0.885, 1.045)
        # party 2
        self.gl_text("BLACK", .4, 1, .7, .8, "Radish", 0.86, 1.04)
        self.gl_text("BLACK",.4, 1, .6, .7, "HP: 10/10", 0.885, 1.045)
        # party 3
        self.gl_text("BLACK", .4, 1, .5, .6, "Toffee", 0.88, 1.045)
        self.gl_text("BLACK",.4, 1, .4, .5, "HP: 10/10", 0.885, 1.045)
        # party 4
        self.gl_text("BLUE", .4, 1, .3, .4, "Grapefart", 0.89, 1.06)
        self.gl_text("RED",.4, 1, .2, .3, "HP: 10/10", 0.88, 1.07)
        # enemy 1
        self.gl_text("BLUE", .64, 1, -.9, -.8, "Enemy", 0.89, 1.06)
        self.gl_text("RED", .64, 1, -.7, -.8, "HP: 10/10", 0.88, 1.07)

        glBegin(GL_QUADS)
        party_port_1 = self.rect_ogl("GREEN", .28, .4, .8, 1)
        party_port_2 = self.rect_ogl("RED", .28, .4, .6, .8)
        party_port_3 = self.rect_ogl("BLUE", .28, .4, .4, .6)
        party_port_4 = self.rect_ogl("GREEN", .28, .4, .2, .4)

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
        
        pygame.display.flip()

    def keyPressed(self, *args):
        if args[0] == ESCAPE:
            glutDestroyWindow(self.window)
            sys.exit()

    def drawText(self, x, y, text, x_adjust, y_adjust):                                                
        textSurface = self.font.render(text, True, (255, 255, 255, 255), (0, 0, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        new_x = ((x+1)/2)*1600/x_adjust
        new_y = ((y+1)/2)*900/y_adjust
        glWindowPos2d(new_x, new_y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def gl_text(self, color, left, right, bot, top, text, x_adjust, y_adjust):
        glBegin(GL_QUADS)
        self.rect_ogl(color, left, right, bot, top)
        glEnd()
        self.drawText(left, top, text, x_adjust, y_adjust)

if __name__ == "__main__":
    game = GameTest(1600, 900)
    game.play()