import pytmx
import pygame
from helpers import *
import crawler_tiled as c

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
        """
        The render function fills the surface with black color and then iterates through the visible
        layers of a Tiled map, blitting each tile onto the surface.
        
        :param surface: The `surface` parameter is the surface object on which the tiles will be
        rendered. It could be a pygame surface or any other compatible surface object
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
        """
        The function applies the camera's top left position to the entity's coordinates and returns the
        updated rectangle.
        
        :param entity: The "entity" parameter is an object that represents a game entity, such as a
        character or an object in the game world. It likely has attributes like "x" and "y" that
        represent its position on the game screen
        :return: The code is returning the updated position of the entity's rectangle after applying the
        camera's top left position.
        """
        entity.x + self.camera.topleft[0]
        entity.y + self.camera.topleft[1]
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        """
        The function applies the position of a rectangle relative to the camera's top left corner.
        
        :param rect: The parameter "rect" is a rectangle object that represents the position and size of
        an object. It typically has attributes such as "left", "top", "width", and "height" that define
        its position and size on the screen
        :return: the rectangle `rect` after applying the camera's top left position to it.
        """
        return rect.move(self.camera.topleft)

    def update(self, target):
        """
        The function updates the camera position based on the target's position to ensure that the
        target is centered on the screen.
        
        :param target: The "target" parameter is an object that has a "rect" attribute. The "rect"
        attribute is a rectangle that represents the position and size of the target object. The
        "centerx" and "centery" attributes of the "rect" represent the x and y coordinates of the center
        of the rectangle
        """
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)

        # limit scrolling to map size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)

        temp = pygame.Rect(x, y, self.width, self.height)
        if temp != self.camera:
            ret = True
        else:
            ret = False
        self.camera = pygame.Rect(x, y, self.width, self.height)
        return ret
    
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((width, height),
                                    pygame.DOUBLEBUF)
    crawl = c.Crawler(screen)
    crawl.run_ind(crawl)