import pygame
from helpers import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import match
import dungeon_layouts as dl
from pytmx.util_pygame import load_pygame
import sys
from os import path
import tiled_functions as tf

size = width, height = 1600, 900
FPS = 60

class Creature():
    def __init__(self, display, x, y, image, animation_frames):
        self.x = x
        self.y = y
        self.animation_frames = animation_frames
        self.current_frame = 0
        self.image = image
        self.display = display
        self.rect = pygame.Rect(self.x, self.y, 96, 96)

    def draw(self):
        blit_image([width, height], self.x, self.y, self.animation_frames[self.current_frame].convert_alpha(), 1, 1, 1)

    def get_rect(self):
        return self.rect
    
    def set_image(self, value):
        self.image = get_portrait(value)
    
    def next_image(self):
        if self.current_frame+1 < len(self.animation_frames):
            self.current_frame += 1
        else:
            self.current_frame = 0

    def image_stop(self):
        self.current_frame = 0

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, 96, 96)


class PlayerMap(Creature):
    def __init__(self, mc, display, x, y, image, animation_frames):
        super().__init__(display, x, y, image, animation_frames)
        self.mc = mc

class EnemyMap(Creature):
    def __init__(self, display, x, y, image, animation_frames):
        super().__init__(display, x, y, image, animation_frames)
        self.can_chase = 1
        

class Crawler():
    def __init__(self, screen):
        self.screen = screen

        # Speed of the player character
        self.speed_x = 0
        self.speed_y = 0

        # Font being used
        self.font = pygame.font.Font('font/VCR.001.ttf', 36)

        # Controls the menu on the right side of the screen
        self.one_expand, self.two_expand, self.three_expand, self.four_expand = 0,0,0,0
        self.expand = 4

        # Whether the game is fullscreen or not
        self.fullscreen = 0

        # Variables for fades
        self.counter_x = 0
        self.counter_y = 0
        self.fade_out = 0
        self.fade_image = pygame.image.load("images/black_pass.png").convert_alpha()
        self.move_to_match = 0
        self.into_combat_transfer = 0
        self.end_fade_transfer = 0

        # Room of the dungeon we're in
        self.current_room = 0

        self.fade_dir = "None"

        self.transfer = 0
        self.transfer_complete = 0

        self.enemy_set = 0
        self.texID = None

    def start(self, prefix):
        goblin_frames = [get_portrait("Goblin_Stand")]
        goblin = Enemy("Goblin", 10, 10, 10, 10, 10, 10)
        self.enemy = EnemyMap(self.screen, goblin, width/2, height/2, get_portrait("Goblin_Stand"), goblin_frames)
        character = BearNSteen([10,10,10,10,10,10])
        animation_frames_player = []
        for x in range (0, 2):
            image = pygame.image.load(self.party[0].get_portrait_dungeon_name() + "_" + str(x) + ".png")
            image = pygame.transform.scale(image,(90, 160))
            animation_frames_player.append(image)
        self.player = PlayerMap(character, self.screen, 740, 125, self.party[0].get_portrait_dungeon(), animation_frames_player)

        pygame.mixer.init()
        self.in_combat = pygame.mixer.Sound("audio/bgm/" + prefix + "dungeon_combat.wav")
        self.oo_combat = pygame.mixer.Sound("audio/bgm/" + prefix + "dungeon_ooc.wav")
        self.in_combat.set_volume(0)
        self.oo_combat.play(-1)
        self.in_combat.play(-1)
        self.camera(1280, 720)

    def start_player(self):
        character = self.party[0]
        animation_frames_player = []
        for x in range (0, 2):
            image = pygame.image.load(self.party[0].get_portrait_dungeon_name() + "_" + str(x) + ".png")
            image = pygame.transform.scale(image,(90, 160))
            animation_frames_player.append(image)
        self.player = PlayerMap(character, self.screen, 740, 125, self.party[0].get_portrait_dungeon(), animation_frames_player)
        self.camera = tf.Camera(self.map.width, self.map.height)

    def start_enemy(self):
        goblin_frames = [get_portrait("Goblin_Stand")]
        self.enemy = EnemyMap(self.screen, width*2, height*2, goblin_frames[0], goblin_frames)

    def amend_enemy(self, port_name):
        px = random.randint(600, 800)
        py = random.randint(300, 600)
        enemy_frames = [get_portrait(port_name), get_portrait(port_name)]
        self.enemy = EnemyMap(self.screen, px, py, enemy_frames[0], enemy_frames)

    def start_audio(self, prefix):
        pygame.mixer.init()
        prefix="pots"
        self.in_combat = pygame.mixer.Sound("audio/bgm/" + prefix + "dungeon_combat.wav")
        self.oo_combat = pygame.mixer.Sound("audio/bgm/" + prefix + "dungeon_ooc.wav")
        self.in_combat.set_volume(0)
        self.oo_combat.set_volume(.2)
        self.oo_combat.play(-1)
        self.in_combat.play(-1)

    def quit(self):
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map_folder = path.join(self.game_folder, 'data/tmx')
        self.map = tf.TiledMap(path.join(self.map_folder, 'cave1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def play(self, party, dungeon, prefix, fade_in=False):
        self.load_data()
        d = dl.get_dungeon_layout(prefix + "tiled")
        dungeon_rooms = d[0]
        dungeon_enemies = d[1]

        self.texID = glGenTextures(1)

        accel_x, accel_y = 0, 0

        chase = 1

        self.party = party
        enemy_port_name = dungeon_rooms[0][1]
        self.start_player()
        #self.start_audio(prefix)
        self.start_enemy()

        player_rect = self.player.get_rect()
        enemy_rect = self.enemy.get_rect()

        if fade_in == True:
            self.end_fade_transfer = 1
        
        stop = "not done"
        in_play = 0

        self.clock = pygame.time.Clock()

        # Timer for enemy attacks.
        timer = pygame.time.get_ticks()

        self.debug = 0
        self.debug_timer = pygame.time.get_ticks()
        animation_timer = pygame.time.get_ticks()
        move_timer = 0
        charge_timer = 0
        chase_move_timer = 0

        current_room = 0
        
        self.fade_image = pygame.transform.scale(self.fade_image,(1600,900))

        while True:
            enemy_port_name = dungeon_enemies[current_room][1]
            
            now = pygame.time.get_ticks()

            if self.enemy_set == 0:
                if dungeon_enemies[current_room][0][0] != None:
                    self.amend_enemy(enemy_port_name)
                    enemy_rect = self.enemy.get_rect()
                    #px = random.randint(485, 1055)
                    #py = random.randint(143, 750)
                    px = random.randint(600, 800)
                    py = random.randint(300, 600)
                    self.enemy.x = px
                    self.enemy.y = py
                    self.enemy_set = 1
                    charge_timer = pygame.time.get_ticks()
                else:
                    self.enemy.x = 3000
                    self.enemy.y = 3000
                    self.enemy_set = 1

            if chase == 1:
                # chase mechanic (test currently)
                if enemy_port_name == "Bazongle_Stand":
                    if now - charge_timer > 5000:
                        if self.player.x > self.enemy.x:
                            accel_x = 5
                        elif self.player.x < self.enemy.x:
                            accel_x = -5
                        else:
                            accel_x = 0
                        if self.player.y > self.enemy.y:
                            accel_y = 5
                        elif self.player.y < self.enemy.y:
                            accel_y = -5
                        else:
                            accel_y = 0
                        self.enemy.x += accel_x
                        self.enemy.y += accel_y

            
            if enemy_port_name == "Goblin_Stand" and now - move_timer > 100:
                if self.enemy.can_chase:
                    if now - charge_timer < 10000:
                        choice = random.randint(0, 11)
                        if choice == 0 or choice == 5:
                            accel_x += 5
                        elif choice == 1 or choice == 6:
                            accel_x += -5
                        elif choice == 2 or choice == 7:
                            accel_x = 0
                        elif choice == 3 or choice == 8:
                            accel_y += 5
                        elif choice == 4 or choice == 9:
                            accel_y += -5
                        elif choice == 10 or choice == 11:
                            accel_y = 0
                        if 485 < self.enemy.x + accel_x < 1055:
                            self.enemy.x += accel_x
                        if 143 < self.enemy.y + accel_y < 750:
                            self.enemy.y += accel_y
                        move_timer = pygame.time.get_ticks()
                    else:
                        if self.player.x > self.enemy.x:
                            accel_x = 3
                        elif self.player.x < self.enemy.x:
                            accel_x = -3
                        else:
                            accel_x = 0
                        if self.player.y > self.enemy.y:
                            accel_y = 3
                        elif self.player.y < self.enemy.y:
                            accel_y = -3
                        else:
                            accel_y = 0
                        self.enemy.x += accel_x
                        self.enemy.y += accel_y
            
            #print("x: " + str(self.player.x) + "| y: " + str(self.player.y))
            player_rect.x, player_rect.y = self.player.x, self.player.y
            enemy_rect.x, enemy_rect.y = self.enemy.x, self.enemy.y

            # collisions with objects / doorways
            
            if self.enemy.get_rect().collidepoint(self.player.get_rect().x, self.player.get_rect().y) and in_play == 0:
                in_play = 1
                self.into_combat_transfer = 1  

            # if left_door.collidepoint(self.player.get_rect().x, self.player.get_rect().y) and self.transfer == 0 and dungeon_rooms[current_room][1] != None:
            #     self.fade_dir = "fade_left"
            #     direction = "left"
            #     self.transfer = 1
            # if top_door.collidepoint(self.player.get_rect().x, self.player.get_rect().y) and self.transfer == 0 and dungeon_rooms[current_room][2] != None:
            #     self.fade_dir = "fade_up"
            #     direction = "up"
            #     self.transfer = 1
            # if right_door.collidepoint(self.player.get_rect().x, self.player.get_rect().y) and self.transfer == 0 and dungeon_rooms[current_room][3] != None:
            #     self.fade_dir = "fade_right"
            #     direction = "right"
            #     self.transfer = 1
            # if south_door.collidepoint(self.player.get_rect().x, self.player.get_rect().y) and self.transfer == 0 and dungeon_rooms[current_room][4] != None:
            #     self.fade_dir = "fade_down"
            #     direction = "down"
            #     self.transfer = 1

            # if self.transfer == 2:
            #     if direction == "left":
            #         if dungeon_rooms[current_room][1] == "END":
            #             self.oo_combat.stop()
            #             self.in_combat.stop()
            #             print("Dungeon Completed!")
            #             return "FINISHED"
            #         current_room = dungeon_rooms[current_room][1]
            #         self.player.x = 1000
            #         self.player.y = height/2
            #     if direction == "up":
            #         if dungeon_rooms[current_room][2] == "END":
            #             self.oo_combat.stop()
            #             self.in_combat.stop()
            #             print("Dungeon Completed!")
            #             return "FINISHED"
            #         current_room = dungeon_rooms[current_room][2]
            #         self.player.y = 170
            #         self.player.x = width/2 - 50
            #     if direction == "right":
            #         if dungeon_rooms[current_room][3] == "END":
            #             self.oo_combat.stop()
            #             self.in_combat.stop()
            #             print("Dungeon Completed!")
            #             return "FINISHED"
            #         current_room = dungeon_rooms[current_room][3]
            #         self.player.x = 500
            #         self.player.y = height/2
            #     if direction == "down":
            #         if dungeon_rooms[current_room][4] == "END":
            #             self.oo_combat.stop()
            #             self.in_combat.stop()
            #             print("Dungeon Completed!")
            #             return "FINISHED"
            #         current_room = dungeon_rooms[current_room][4]
            #         self.player.y = 700
            #         self.player.x = width/2 - 50
            #     if dungeon_enemies[current_room][1] != None:
            #         self.enemy.set_image(dungeon_enemies[current_room][1])
            #     self.enemy_set = 0
            #     self.enemy.can_chase = 1
            #     self.transfer = 3


            if self.into_combat_transfer == 1:
                pass
                #stop = self.fade(self.counter_x, self.counter_y, 1)
                #self.move_to_match = self.scoot(self.counter_x)
                
            if self.move_to_match == 1:
                print("Moving to match")
                self.in_combat.set_volume(self.oo_combat.get_volume())
                self.oo_combat.set_volume(0)
                state = match.MatchGame(self.screen).play(party, dungeon_enemies[current_room][0], self.screen, 1)
                self.oo_combat.set_volume(self.in_combat.get_volume())
                self.in_combat.set_volume(0)
                if state == "WIN":
                    self.enemy.x = 3200
                    self.enemy.y = 3200
                    self.enemy.can_chase = 0
                self.counter_x = 0
                self.end_fade_transfer = 1
                self.move_to_match = 0
                in_play = 0

            
            self.draw_gl_scene(dungeon_rooms, current_room, party, dungeon_enemies)
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)

            pressed = pygame.key.get_pressed()
            has_pressed = self.check_for_movement_keys_being_pressed(pressed)
            if has_pressed == True and self.transfer == 0:
                if now - animation_timer > 100:
                    self.player.next_image()
                    animation_timer = now
                self.input(None, pressed)
            else:
                if self.speed_x > 0:
                    if self.speed_x == 1:
                        self.speed_x -= 1
                    else:
                        self.speed_x -= 2
                elif self.speed_x < 0:
                    if self.speed_x == 1:
                        self.speed_x += 1
                    else:
                        self.speed_x += 2
                if self.speed_y > 0:
                    if self.speed_y == 1:
                        self.speed_y -= 1
                    else:
                        self.speed_y -= 2
                elif self.speed_y < 0:
                    if self.speed_y == 1:
                        self.speed_y += 1
                    else:
                        self.speed_y += 2

            for event in pygame.event.get():
                if event.type == KEYUP:
                    self.player.image_stop()
                    if self.into_combat_transfer == 0 and self.transfer == 0:
                        self.input(event.key)
                elif event.type == QUIT:
                    #self.event.set()
                    self.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #if return_rect.collidepoint(event.pos):
                    #    return "RAN"
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        print(pos)
                        # if left_door.collidepoint(pos):
                        #    print("Clicked on Left Door")
                        # if right_door.collidepoint(pos):
                        #    print("Clicked on Right Door")
                        # if top_door.collidepoint(pos):
                        #    print("Clicked on Top Door")
                        tot = 0
                        for x in self.party:
                            if x != None:
                                tot += 1
                        for x in range(0, tot):
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
        if self.into_combat_transfer != 1 and self.end_fade_transfer != 1:
            if pressed != False:
                keys = pressed  #checking pressed keys
                if (keys[pygame.K_UP] or keys[pygame.K_w]):
                    if self.speed_x != 0 and self.speed_y < 0:
                        self.speed_y = 0
                    if self.speed_y < 0:
                        self.speed_y += 2
                    else:
                        if self.speed_y < 10:
                            self.speed_y += 1
                    self.player.y += self.speed_y
                if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                    if self.speed_y != 0 and self.speed_x > 0:
                        self.speed_x = 0
                    if self.speed_x == 1:
                        self.speed_x -= 1
                    if self.speed_x > 0:
                        self.speed_x -= 2
                    else:
                        if self.speed_x > -10:
                            self.speed_x -= 1
                    self.player.x += self.speed_x
                if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                    if self.speed_y != 0 and self.speed_x < 0:
                        self.speed_x = 0
                    if self.speed_x == -1:
                        self.speed_x += 1
                    if self.speed_x < 0:
                        self.speed_x += 2
                    else:
                        if self.speed_x < 10:
                            self.speed_x += 1
                    self.player.x += self.speed_x
                if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                    if self.speed_x != 0 and self.speed_y > 0:
                        self.speed_y = 0
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

    def check_for_movement_keys_being_pressed(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            return True
        return False

    def draw_gl_scene(self, dungeon_rooms, current_room, party, dungeon_enemies):
        #glLoadIdentity()
        #glTranslatef(0.0,0.0,-10.0)

        self.blit_bg_camera(dungeon_rooms[current_room][0], False)
        self.map_rect = self.camera.apply_rect(self.map_rect)
        blit_image(size, 0, 0, self.map_img, 1,1,1)
        
        self.player.rect = self.camera.apply(self.player)
        self.enemy.rect = self.camera.apply(self.enemy)
        if dungeon_enemies[current_room][1] == None:
            self.player.draw()
        elif self.player.y < self.enemy.y:
            self.enemy.draw()
            self.player.draw()
        else:
            self.player.draw()
            self.enemy.draw()

        # Draw Party Info START
        top = cgls(height-100, height)
        bot = cgls(height-10, height)
        nums = [[width-400, width-310, width-220, width-130],[height-100]]

        glBegin(GL_QUADS)
        # "party text"
        #rect_ogl("BLACK", cgls(nums[0][0], width), cgls(nums[0][3]+90, width), cgls(height-110, height), cgls(height-160, height))

        # if the stats box is expanded:
        if self.expand != 4:
            
            # draw the stats box
            rect_ogl("BLACK", cgls(nums[0][0], width), cgls(nums[0][3]+90, width), cgls(height-170, height), cgls(height-810, height))

        glEnd()
        
        # party member portrait rects (for clicking)
        self.party_ports = []
        port1_rect = pygame.Rect(nums[0][0],height-850,90,90)
        self.party_ports.append(port1_rect)
        if self.party[1] != None:
            port2_rect = pygame.Rect(nums[0][1],height-850,90,90)
            self.party_ports.append(port2_rect)
        if self.party[2] != None:
            port3_rect = pygame.Rect(nums[0][2],height-850,90,90)
            self.party_ports.append(port3_rect)
        if self.party[3] != None:
            port4_rect = pygame.Rect(nums[0][3],height-850,90,90)
            self.party_ports.append(port4_rect)

        # party member portrait pics
        shape_color("BLACK")
        if party[0] != None:    
            blit_image([width, height], width-400,height-100, party[0].get_portrait().convert_alpha(), 1, 1, 1)
        if party[1] != None:  
            blit_image([width, height], width-310,height-100, party[1].get_portrait().convert_alpha(), 1, 1, 1)
        if party[2] != None:
            blit_image([width, height], width-220,height-100, party[2].get_portrait().convert_alpha(), 1, 1, 1)
        if party[3] != None:
            blit_image([width, height], width-130,height-100, party[3].get_portrait().convert_alpha(), 1, 1, 1)

        if self.expand == 0:
            self.write_details_gl(0, nums, party)
        if self.expand == 1:
            self.write_details_gl(1, nums, party)
        if self.expand == 2:
            self.write_details_gl(2, nums, party)
        if self.expand == 3:
            self.write_details_gl(3, nums, party)

        gl_text(self.font, "BLACK", cgls(nums[0][3]+90, width), cgls(nums[0][0], width), cgls(height-160, height), cgls(height-110, height), "PARTY", .91, .985)

        # Draw Party Text END

        # Handle Fades
        if self.into_combat_transfer == 1:
            blit_image([width, height], width-self.counter_x, 0, self.fade_image, 1, 1, 1)
            print(self.counter_x)
            if self.counter_x < 200:
                self.counter_x += 50
            elif self.counter_x < 500:
                self.counter_x += 75
            else:
                self.counter_x += 100
            if self.counter_x >= 1700:
                self.into_combat_transfer = 0
                self.move_to_match = 1

        if self.end_fade_transfer == 1:
            # Add in party members vs. enemies portraits on sliding black screen
            blit_image([width, height], 0-self.counter_x, 0, self.fade_image, 1, 1, 1)
            print(self.counter_x)
            self.counter_x += 100
            if self.counter_x >= 1700:
                self.end_fade_transfer = 0

        if self.into_combat_transfer == 1:
            blit_image([width, height], width-self.counter_x, 0, self.fade_image, 1, 1, 1)
            print(self.counter_x)
            if self.counter_x < 200:
                self.counter_x += 50
            elif self.counter_x < 500:
                self.counter_x += 75
            else:
                self.counter_x += 100
            if self.counter_x >= 1700:
                self.into_combat_transfer = 0
                self.move_to_match = 1

        status = False
        if self.fade_dir == "fade_left_finish" and self.transfer == 3:
            self.fade_finish_x(width, "fade_left")
        if self.fade_dir == "fade_right_finish" and self.transfer == 3:
            self.fade_finish_x(width, "fade_right")
        if self.fade_dir == "fade_up_finish" and self.transfer == 3:
            self.fade_finish_y(height, "fade_up")
        if self.fade_dir == "fade_down_finish" and self.transfer == 3:
            self.fade_finish_y(height, "fade_down")
        if self.fade_dir == "fade_left":
            status = self.fade_start_x(width, "fade_left")
        if self.fade_dir == "fade_right":
            status = self.fade_start_x(width, "fade_right")
        if self.fade_dir == "fade_up":
            status = self.fade_start_y(height, "fade_up")
        if self.fade_dir == "fade_down":
            status = self.fade_start_y(height, "fade_down")
        if status:
            self.transfer = 2
        if self.fade_dir == "fade_done":
            self.transfer = 0

        self.camera.update(self.player)
        pygame.display.flip()
        return
    
    def blit_bg_camera(self, bg="cave.png", move=True):
        background = pygame.image.load("images/backgrounds/" + bg).convert_alpha()
        blit_image([width, height], 0, 0, background, 1, 1, 1)

    def write_details_gl(self, party_member, nums, party):
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-210, height), cgls(height-160, height), self.get_actual_name(party[party_member].get_name()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-270, height), cgls(height-220, height), str(party[party_member].get_role()) + " " + str(party[party_member].get_level()), 1, 1)
        gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-330, height), cgls(height-280, height), "HP: " + str(party[party_member].get_hp()), 1, 1)
        if party[party_member].get_physical_attack() > 1000:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-390, height), cgls(height-340, height), "PA: " + str(party[party_member].get_physical_attack()), 1, 1)
        else:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-390, height), cgls(height-340, height), "PHYS ATTACK: " + str(party[party_member].get_physical_attack()), 1, 1)
        if party[party_member].get_magic_attack() > 1000:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-450, height), cgls(height-400, height), "MA: " + str(party[party_member].get_magic_attack()), 1, 1)
        else:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-450, height), cgls(height-400, height), "MAG ATTACK: " + str(party[party_member].get_magic_attack()), 1, 1)
        if party[party_member].get_magic_attack() > 1000:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-510, height), cgls(height-460, height), "PG: " + str(party[party_member].get_physical_guard()), 1, 1)
        else:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-510, height), cgls(height-460, height), "PHYS GUARD: " + str(party[party_member].get_physical_guard()), 1, 1)
        if party[party_member].get_magic_attack() > 1000:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-570, height), cgls(height-520, height), "MG: " + str(party[party_member].get_magical_guard()), 1, 1)
        else:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-570, height), cgls(height-520, height), "MAG GUARD: " + str(party[party_member].get_magical_guard()), 1, 1)
        if party[party_member].get_magic_attack() > 1000:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-630, height), cgls(height-580, height), "Q: " + str(party[party_member].get_quickness()), 1, 1)
        else:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-630, height), cgls(height-580, height), "QUICKNESS: " + str(party[party_member].get_quickness()), 1, 1)
        if party[party_member].get_magic_attack() > 1000:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-690, height), cgls(height-640, height), "H: " + str(party[party_member].get_healing()), 1, 1)
        else:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-690, height), cgls(height-640, height), "HEALING: " + str(party[party_member].get_healing()), 1, 1)
        if party[party_member].get_magic_attack() > 1000:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-750, height), cgls(height-700, height), "C: " + str(party[party_member].get_chutzpah()), 1, 1)
        else:
            gl_text(self.font, "BLACK", cgls(nums[0][3]+80, width), cgls(nums[0][0]+10, width), cgls(height-750, height), cgls(height-700, height), "CHUTZPAH: " + str(party[party_member].get_chutzpah()), 1, 1)
        
        

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
        else:
            return name
        
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
    
    def fade_start_y(self, y, direction):
        # up
        if direction == "fade_up":
            blit_image([width, y], 0, y-self.counter_y, self.fade_image, 1, 1, 1)
        # down
        if direction == "fade_down":
            blit_image([width, y], 0, -y+self.counter_y, self.fade_image, 1, 1, 1)
        finished = self.fade_counters_y(y)
        if finished:
            if direction == "fade_up":
                self.fade_dir = "fade_up_finish"
            elif direction == "fade_down":
                self.fade_dir = "fade_down_finish"
            return True
        else: return False

    def fade_finish_y(self, y, direction):
        # up
        if direction == "fade_up":
            blit_image([width, y], 0, 0-self.counter_y, self.fade_image, 1, 1, 1)
        # down
        if direction == "fade_down":
            blit_image([width, y], 0, 0+self.counter_y, self.fade_image, 1, 1, 1)
        finished = self.fade_counters_y(y)
        if finished:
            self.fade_dir = "fade_done"

    def fade_start_x(self, x, direction):
        # left
        if direction == "fade_left":
            blit_image([x, height], x-self.counter_x, 0, self.fade_image, 1, 1, 1)
        # right
        if direction == "fade_right":
            blit_image([x, height], -x+self.counter_x, 0, self.fade_image, 1, 1, 1)
        finished = self.fade_counters_x(x)
        if finished:
            if direction == "fade_left":
                self.fade_dir = "fade_left_finish"
            elif direction == "fade_right":
                self.fade_dir = "fade_right_finish"
            return True
        else: return False

    def fade_finish_x(self, x, direction):
        # left
        if direction == "fade_left":
            blit_image([x, height], 0-self.counter_x, 0, self.fade_image, 1, 1, 1)
        # right
        if direction == "fade_right":
            blit_image([x, height], 0+self.counter_x, 0, self.fade_image, 1, 1, 1)
        finished = self.fade_counters_x(x)
        if finished:
            self.fade_dir = "fade_done"

    def fade_counters_x(self, x):
        if self.counter_x < x/4.5:
            self.counter_x += x/18
        elif self.counter_x < x/1.8:
            self.counter_x += x/12
        else:
            self.counter_x += x/9
        if self.counter_x >= x:
            self.counter_x = 0
            return True

    def fade_counters_y(self, y):
        if self.counter_y < y/4.5:
            self.counter_y += y/18
        elif self.counter_y < y/1.8:
            self.counter_y += y/12
        else:
            self.counter_y += y/9
        if self.counter_y >= y:
            self.counter_y = 0
            return True

    def gl_show_map(self):
        glEnable(GL_TEXTURE_2D)
        rgb_surface = pygame.image.tostring( self.map_img, 'RGB')
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        surface_rect = self.map_img.get_rect()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 
                     surface_rect.width, surface_rect.height, 0, GL_RGB, 
                     GL_UNSIGNED_BYTE, rgb_surface)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(-1, 1)
        glTexCoord2f(0, 1); glVertex2f(-1, -1)
        glTexCoord2f(1, 1); glVertex2f(1, -1)
        glTexCoord2f(1, 0); glVertex2f(1, 1)
        glEnd()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)
    
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glDepthRange(0, 1)
    glMatrixMode(GL_PROJECTION)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    glClear(GL_COLOR_BUFFER_BIT)
    party = fill_party()
    party = boost_party(party)
    dungeon = "cave"

    # Start game
    state = Crawler(screen).play(party, get_dungeon(dungeon), dungeon)
    print("Your final result was: " + state)