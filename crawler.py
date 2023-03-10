import pygame
from helpers import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

size = width, height = 1600, 900
FPS = 60

class Creature():
    def __init__(self, display, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.display = display

    def draw(self):
        blit_image([width, height], self.x, self.y, self.image, 1, 1, 1)


class PlayerMap(Creature):
    def __init__(self, mc, display, x, y, image):
        super().__init__(display, x, y, image)
        self.mc = mc


class EnemyMap(Creature):
    def __init__(self, enemy, display, x, y, image):
        super().__init__(display, x, y, image)
        self.enemy = enemy
        

class Crawler():
    def __init__(self, screen):
        self.screen = screen
        self.speed_x = 0
        self.speed_y = 0

    def start(self):
        goblin = Enemy("Goblin", 10, 10, 10, 10, 10, 10)
        self.enemy = EnemyMap(self.screen, goblin, width/2, height/2, get_portrait("Gobble"))
        character = BearKnight([10,10,10,10,10,10])
        self.player = PlayerMap(character, self.screen, 740, 125, get_portrait("dogdude"))

    def quit(self):
        pygame.quit()
        sys.exit()

    def play(self, party):
        #gluPerspective(45, (1600/900), 0.1, 50.0)
        #glTranslatef(0.0, 0.0, -5)
        # Set all party member HPs to max before beginning.

        self.start()
        self.party = party

        self.clock = pygame.time.Clock()

        # Timer for enemy attacks.
        timer = pygame.time.get_ticks()

        self.debug = 0
        self.debug_timer = pygame.time.get_ticks()

        current_room = 0
        dungeon_rooms = ["testroom.png"]

        while True:
            now = pygame.time.get_ticks()
            print("x: " + str(self.player.x) + "| y: " + str(self.player.y))

            self.draw_gl_scene(dungeon_rooms, current_room)
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)

            pressed = pygame.key.get_pressed()
            has_pressed = self.slow_down(pressed)
            if has_pressed == True:
                self.input(None, pressed)
            else:
                if self.speed_x > 0:
                    self.speed_x -= 2
                elif self.speed_x < 0:
                    self.speed_x += 2
                if self.speed_y > 0:
                    self.speed_y -= 2
                elif self.speed_y < 0:
                    self.speed_y += 2

            for event in pygame.event.get():
                if event.type == KEYUP:
                    self.input(event.key)
                elif event.type == QUIT:
                    #self.event.set()
                    self.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #if return_rect.collidepoint(event.pos):
                    #    return "RAN"
                    if event.button == 1:
                       pos = pygame.mouse.get_pos()

    def draw(self):
        pass
    
    def input(self, key = None, pressed = False):
        if pressed != False:
            keys = pressed  #checking pressed keys
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.player.y < 677:
                if self.speed_y < 0:
                    self.speed_y += 2
                else:
                    if self.speed_y < 10:
                        self.speed_y += 2
                self.player.y += self.speed_y
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.player.x > 485:
                if self.speed_x > 0:
                    self.speed_x -= 2
                else:
                    if self.speed_x > -10:
                        self.speed_x -= 2
                self.player.x += self.speed_x
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.player.x < 1055:
                if self.speed_x < 0:
                    self.speed_x += 2
                else:
                    if self.speed_x < 10:
                        self.speed_x += 2
                self.player.x += self.speed_x
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.player.y > 143:
                if self.speed_y > 0:
                    self.speed_y -= 2
                else:
                    if self.speed_y > -10:
                        self.speed_y -= 2
                self.player.y += self.speed_y
        else:
            if key == K_q:
                self.quit()
                """
            elif (key == K_RIGHT or key == K_d) and self.player.x < 1200:
                self.player.x += self.speed_x
            elif (key == K_LEFT or key == K_a) and self.player.x > 400:
                self.player.x += self.speed_x
            elif (key == K_DOWN or key == K_s) and self.player.y > 200:
                self.player.y += self.speed_y
            elif (key == K_UP or key == K_w) and self.player.y < 700:
                self.player.y += self.speed_y
                """
            elif key == K_r:
                if self.fullscreen == 0:
                    self.display = pygame.display.set_mode((width, height),
                                                pygame.DOUBLEBUF|pygame.OPENGL|pygame.FULLSCREEN)
                    self.fullscreen = 1
                else:
                    self.display = pygame.display.set_mode((width, height),
                                                pygame.DOUBLEBUF|pygame.OPENGL)
                    self.fullscreen = 0

    def slow_down(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            return True
        return False

    def draw_gl_scene(self, dungeon_rooms, current_room):
        #glLoadIdentity()
        #glTranslatef(0.0,0.0,-10.0)

        self.blit_bg_camera(dungeon_rooms[current_room], False)
        self.player.draw()
        self.enemy.draw()
        
        shape_color("BLACK")

        pygame.display.flip()

        return
    
    def blit_bg_camera(self, bg="cave.png", move=True):
        background = pygame.image.load("images/" + bg).convert_alpha()
        background = pygame.transform.scale(background,(1600,900))
        blit_image([width, height], 0, 0, background, 1, 1, 1)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
    party = fill_party()
    state = Crawler(screen).play(party)
    print("Your final result was: " + state)