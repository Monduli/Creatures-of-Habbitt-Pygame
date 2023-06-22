import pytmx
import pygame
from helpers import *

WIDTH = 1600
HEIGHT = 900
size = (WIDTH, HEIGHT)

class TiledMap:
    """
    Class that contains tools for creating a map using tiles.
    """

    def __init__(self, filename):
        """Constructor for TiledMap

        Args:
            filename (string): Name of file to be loaded with pytmx
        """
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        """Blits tiles to a surface that can later be either blit or displayed with OpenGL

        Args:
            surface (pygame Surface): The surface to be drawn to
        """
        surface.fill('black')
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmxdata.tilewidth, 
                                            y*self.tmxdata.tileheight))
                        
    def make_map(self):
        """Creates a surface then uses render to add tiles to it.

        Returns:
            surface: the surface created with tiles on it
        """
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
    
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        entity.x + self.camera.topleft[0]
        entity.y + self.camera.topleft[1]
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)