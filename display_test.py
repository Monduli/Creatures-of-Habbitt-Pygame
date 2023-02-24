import os
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from helpers import *

ESCAPE = '\033'
texture = 0

A_TEX_NUMBER = None
B_TEX_NUMBER = None

FONT_SIZE = 36

class GameTest():
    def __init__(self, w, h, window):
        pygame.init()
        self.window = window
        A_TEX_NUMBER = self.generate_texture_for_text("a")
        B_TEX_NUMBER = self.generate_texture_for_text("b")
        glEnable(GL_TEXTURE_2D)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        self.done = 1

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

            glClear(GL_COLOR_BUFFER_BIT)

            #self.draw_gl_scene()

            glFlush()

            pygame.display.flip()
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

    def rect_ogl(self, color, left, right, bot, top):
        self.shape_color(color)
        glVertex2f(left, bot)
        glVertex2f(left, top)
        glVertex2f(right, top)
        glVertex2f(right, bot)

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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0,0.0,-10.0)
        glBegin(GL_QUADS)

        self.shape_color("BLACK")
        # party 1 portrait
        party_port_1 = self.rect_ogl("GREEN", .28, .4, .8, 1)
        party_name_1 = self.rect_ogl("BLUE", .4, 1, .9, 1)
        party_hp_1 = self.rect_ogl("RED", .4, 1, .8, .9)

        # party 2 portrait
        party_port_2 = self.rect_ogl("RED", .28, .4, .6, .8)
        party_name_2 = self.rect_ogl("BLUE", .4, 1, .7, .8)
        party_hp_2 = self.rect_ogl("GREEN", .4, 1, .6, .7)

        # party 2 portrait
        party_port_3 = self.rect_ogl("BLUE", .28, .4, .4, .6)
        party_name_3 = self.rect_ogl("RED", .4, 1, .5, .6)
        party_hp_3 = self.rect_ogl("GREEN", .4, 1, .4, .5)

        # party 2 portrait
        party_port_3 = self.rect_ogl("GREEN", .28, .4, .2, .4)
        party_name_3 = self.rect_ogl("BLUE", .4, 1, .3, .4)
        party_hp_3 = self.rect_ogl("RED", .4, 1, .2, .3)

        glEnd()
        glutSwapBuffers()

    def keyPressed(*args):
        if args[0] == ESCAPE:
            glutDestroyWindow(self.window)
            sys.exit()

if __name__ == "__main__":
    glutInit("")
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(1600, 900)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Dan's OpenGL Display Test")
    game = GameTest(1600, 900, window)
    glutDisplayFunc(game.draw_gl_scene)
    glutIdleFunc(game.draw_gl_scene)
    glutKeyboardFunc(game.keyPressed)
    glutMainLoop()
    GameTest().play()