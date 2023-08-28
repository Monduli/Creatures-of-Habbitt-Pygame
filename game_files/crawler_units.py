import pygame
from helpers import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import match_game as match_game
from classes import *
import crawler_tiled as c

size = width, height = 1600, 900
FPS = 60
texID = glGenTextures(1)        

class Creature():
    def __init__(self, display, x, y, image, animation_frames):
        self.x = x
        self.y = y
        self.x_on_screen = x
        self.y_on_screen = y
        self.x_adjust = -36
        self.y_adjust = -140
        self.animation_frames = animation_frames
        self.current_frame = 0
        self.image = image
        self.display = display
        self.rect = pygame.Rect(self.x_on_screen, self.y_on_screen, 24, 24)

    def draw(self):
        """
        The draw function blits an animation frame onto the screen at the specified x and y coordinates.
        Uses: self.x, self.y, self.animation_frames, self.current_frame, self.screen
        """        
        self.display.blit(self.animation_frames[self.current_frame].convert_alpha(), [self.rect.left-36, self.rect.top-140])
        #self.display.blit(pygame.image.load("images/black.png"), self.rect)
    
    # Getters
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_x_on_screen(self):
        return self.x_on_screen
    
    def get_y_on_screen(self):
        return self.y_on_screen
    
    def get_animation_frames(self):
        return self.animation_frames
    
    def get_current_frame(self):
        return self.current_frame
    
    def get_image(self):
        return self.image
    
    def get_display(self):
        return self.display
    
    def get_rect(self):
        return self.rect
    
    # Setters
    def set_x(self, value):
        self.x = value

    def set_y(self, value):
        self.y = value

    def set_animation_frames(self, value):
        self.animation_frames = value

    def set_current_frame(self, value):
        self.current_frame = value

    def set_display(self, value):
        self.display = value
    
    # Image functions
    def set_image(self, value):
        """
        The function sets the image attribute of an object to the value returned by the get_portrait
        function.
        
        :param value: The value parameter is the input value that is passed to the set_image method. It
        is used as an argument to the get_portrait function
        """
        self.image = get_portrait(value)
    
    def next_image(self):
        """
        The function increments the current frame index of an animation and resets it to 0 if it reaches
        the end.
        """
        if self.current_frame+1 < len(self.animation_frames):
            self.current_frame += 1
        else:
            self.current_frame = 0

    def image_stop(self):
        """
        The function sets the current frame of an image to 0.
        """
        self.current_frame = 0

    # Rect Functions
    def set_rect(self):
        """
        The function sets the rectangle attribute of an object using the x and y coordinates and a fixed
        width and height.
        """
        self.rect = pygame.Rect(self.x-self.x_adjust, self.y-self.y_adjust, 24, 24)

    def reset_rect(self):
        """
        The function sets the rectangle attribute of an object using the x and y coordinates and a fixed
        width and height.
        """
        self.rect = pygame.Rect(width-self.x-self.x_adjust, height-self.y-self.y_adjust, 24, 24)


class PlayerMap(Creature):
    def __init__(self, mc, display, x, y, image, animation_frames):
        super().__init__(display, x, y, image, animation_frames)
        self.mc = mc

class EnemyMap(Creature):
    def __init__(self, display, x, y, image, animation_frames):
        super().__init__(display, x, y, image, animation_frames)
        self.can_chase = 1


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((width, height),
                                    pygame.DOUBLEBUF)
    crawl = c.Crawler(screen)
    crawl.run_ind(crawl)