import pygame
from helpers import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import match

size = width, height = 1600, 900
FPS = 60

class Creature():
    def __init__(self, display, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.display = display
        self.rect = pygame.Rect(x, y, 96, 96)

    def draw(self):
        blit_image([width, height], self.x, self.y, self.image, 1, 1, 1)

    def get_rect(self):
        return self.rect


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
        self.font = pygame.font.Font('font/VCR.001.ttf', 36)
        self.one_expand, self.two_expand, self.three_expand, self.four_expand = 0,0,0,0
        self.expand = 4
        self.fullscreen = 0
        self.counter_x = 0
        self.counter_y = 0
        self.fade_out = 0
        self.fade_image = pygame.image.load("images/circlefade.png")

    def start(self):
        goblin = Enemy("Goblin", 10, 10, 10, 10, 10, 10)
        self.enemy = EnemyMap(self.screen, goblin, width/2, height/2, get_portrait("Goblin_Stand"))
        character = BearKnight([10,10,10,10,10,10])
        self.player = PlayerMap(character, self.screen, 740, 125, get_portrait("dogdude"))

    def quit(self):
        pygame.quit()
        sys.exit()

    def play(self, party, dungeon):
        self.start()
        #gluPerspective(45, (1600/900), 0.1, 50.0)
        #glTranslatef(0.0, 0.0, -5)
        # Set all party member HPs to max before beginning
        self.party = party

        player_rect = self.player.get_rect()
        enemy_rect = self.enemy.get_rect()
        start_fade = 0
        stop = "not done"

        self.clock = pygame.time.Clock()

        # Timer for enemy attacks.
        timer = pygame.time.get_ticks()

        self.debug = 0
        self.debug_timer = pygame.time.get_ticks()

        current_room = 0
        dungeon_rooms = ["testroom.png"]

        while True:
            now = pygame.time.get_ticks()
            #print("x: " + str(self.player.x) + "| y: " + str(self.player.y))
            player_rect.x, player_rect.y = self.player.x, self.player.y
            enemy_rect.x, enemy_rect.y = self.enemy.x, self.enemy.y

            if self.enemy.get_rect().collidepoint(self.player.get_rect().x, self.player.get_rect().y):
                start_fade = 1

            if start_fade == 1:
                stop = self.fade(self.counter_x, self.counter_y, 1)
                
            if stop == "done":
                state = match.Game(self.screen).play(party, dungeon, self.screen, 1)

            self.draw_gl_scene(dungeon_rooms, current_room, party, start_fade)
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
                       for x in range(0, 4):
                        if self.party_ports[x].collidepoint(pos):
                            is_expanded = self.check_for_expand(x)
                            if is_expanded == False:
                                if x == 0:
                                    self.expand = 0
                                elif x == 1:
                                    self.expand = 1
                                elif x == 2:
                                    self.expand = 2
                                elif x == 3:
                                    self.expand = 3
                                break
                            else:
                                self.expand = 4

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
                        self.speed_y += 1
                self.player.y += self.speed_y
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.player.x > 485:
                if self.speed_x > 0:
                    self.speed_x -= 2
                else:
                    if self.speed_x > -10:
                        self.speed_x -= 1
                self.player.x += self.speed_x
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.player.x < 1055:
                if self.speed_x < 0:
                    self.speed_x += 2
                else:
                    if self.speed_x < 10:
                        self.speed_x += 1
                self.player.x += self.speed_x
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.player.y > 143:
                if self.speed_y > 0:
                    self.speed_y -= 2
                else:
                    if self.speed_y > -10:
                        self.speed_y -= 1
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

    def draw_gl_scene(self, dungeon_rooms, current_room, party, start_fade):
        #glLoadIdentity()
        #glTranslatef(0.0,0.0,-10.0)

        self.blit_bg_camera(dungeon_rooms[current_room], False)
        self.player.draw()
        self.enemy.draw()
        top = cgls(height-100, height)
        bot = cgls(height-10, height)
        nums = [[width-400, width-310, width-220, width-130],[height-100]]

        glBegin(GL_QUADS)

        #partyport_1 = rect_ogl("BLACK", cgls(nums[0][0], width), cgls(nums[0][0]+90, width), top, bot)
        #partyport_2 = rect_ogl("BLACK", cgls(nums[0][1], width), cgls(nums[0][1]+90, width), top, bot)
        #partyport_3 = rect_ogl("BLACK", cgls(nums[0][2], width), cgls(nums[0][2]+90, width), top, bot)
        #partyport_4 = rect_ogl("BLACK", cgls(nums[0][3], width), cgls(nums[0][3]+90, width), top, bot)
        party_text = rect_ogl("BLACK", cgls(nums[0][0], width), cgls(nums[0][3]+90, width), cgls(height-110, height), cgls(height-160, height))

        if self.expand != 4:
            explain_box = rect_ogl("BLACK", cgls(nums[0][0], width), cgls(nums[0][3]+90, width), cgls(height-170, height), cgls(height-810, height))

        glEnd()
        
        port1_rect = pygame.Rect(nums[0][0],height-850,90,90)
        port2_rect = pygame.Rect(nums[0][1],height-850,90,90)
        port3_rect = pygame.Rect(nums[0][2],height-850,90,90)
        port4_rect = pygame.Rect(nums[0][3],height-850,90,90)
        self.party_ports = [port1_rect, port2_rect, port3_rect, port4_rect]

        shape_color("BLACK")
        if len(party) > 0:    
            blit_image([width, height], width-400,height-100, pygame.image.load(get_portrait_2(party[0].get_name())).convert_alpha(), 1, 1, 1)
        if len(party) > 1:    
            blit_image([width, height], width-310,height-100, pygame.image.load(get_portrait_2(party[1].get_name())).convert_alpha(), 1, 1, 1)
        if len(party) > 2:
            blit_image([width, height], width-220,height-100, pygame.image.load(get_portrait_2(party[2].get_name())).convert_alpha(), 1, 1, 1)
        if len(party) > 3:
            blit_image([width, height], width-130,height-100, pygame.image.load(get_portrait_2(party[3].get_name())).convert_alpha(), 1, 1, 1)

        if self.expand == 0:
            self.write_details_gl(0, nums)
        if self.expand == 1:
            self.write_details_gl(1, nums)
        if self.expand == 2:
            self.write_details_gl(2, nums)
        if self.expand == 3:
            self.write_details_gl(3, nums)

        gl_text(self.font, "BLACK", cgls(nums[0][3]+90, width), cgls(nums[0][0], width), cgls(height-160, height), cgls(height-110, height), "PARTY", .91, .985)

        if start_fade == 1:
            blit_image((1600,900), -5600+self.counter_x/2, -3150+self.counter_y/2, self.fade_image, 1,1,1)

        pygame.display.flip()

        return
    
    def blit_bg_camera(self, bg="cave.png", move=True):
        background = pygame.image.load("images/" + bg).convert_alpha()
        background = pygame.transform.scale(background,(1600,900))
        blit_image([width, height], 0, 0, background, 1, 1, 1)

    def write_details_gl(self, party_member, nums):
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-210, height), cgls(height-160, height), self.get_actual_name(party[party_member].get_name()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-270, height), cgls(height-220, height), str(party[party_member].get_role()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-330, height), cgls(height-280, height), "HP: " + str(party[party_member].get_hp()) + "/" + str(party[party_member].get_hp()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-390, height), cgls(height-340, height), "PHYS ATTACK: " + str(party[party_member].get_str()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-450, height), cgls(height-400, height), "MAG ATTACK: " + str(party[party_member].get_magic()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-510, height), cgls(height-460, height), "PHYS GUARD: " + str(party[party_member].get_phys_guard()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-570, height), cgls(height-520, height), "MAG GUARD: " + str(party[party_member].get_mag_guard()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-630, height), cgls(height-580, height), "QUICKNESS: " + str(party[party_member].get_dex()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-690, height), cgls(height-640, height), "PASSION: " + str(party[party_member].get_wis()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-750, height), cgls(height-700, height), "CHUTZPAH: " + str(party[party_member].get_cha()), 1, 1)

    def check_for_expand(self, num):
        if self.expand == 0 and num == 0:
            return True
        if self.expand == 1 and num == 1:
            return True
        if self.expand == 2 and num == 2:
            return True
        if self.expand == 3 and num == 3:
            return True
        return False
    
    def get_actual_name(self, name):
        if name == "N. Steen":
            return "Bear N. Steen"
        if name == "Radish":
            return "Radish Rabbit"
        if name == "Cinna":
            return "Cinnamon Bun"
        if name == "Grapefart":
            return "Gil Grapefart"
        
    def fade(self, counter_x, counter_y, fade_dir):
        if fade_dir == 1:
            counter_x += 256
            counter_y += 144
            self.crawler_fade_out(counter_x, counter_y)
            if counter_x >= 12800 or counter_y >= 7200:
                counter_x = 0
                counter_y = 0
                return "done"
        elif fade_dir == 2:
            counter_x += 256
            counter_y += 144
            self.crawler_fade_in(counter_x, counter_y)
            if counter_x >= 6400 or counter_y >= 3600:
                counter_x = 0
                counter_y = 0
        return "not done"

    def crawler_fade_out(self, counter_x, counter_y):
        self.fade_image = pygame.transform.scale(self.fade_image,(12800 - counter_x,7200 - counter_y))

    def crawler_fade_in(self, counter_x, counter_y, fade):
        self.fade_image = pygame.transform.scale(self.fade_image,(0 + counter_x,0 + counter_y))
        blit_image((1600,900), 7200-counter_x/2, 4050-counter_y/2, fade, 1,1,1)



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
    party = fill_party()
    state = Crawler(screen).play(party, get_dungeon("cave"))
    print("Your final result was: " + state)