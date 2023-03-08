
def thread_process_action(self):
    global curr_match
    party_current = 0
    while True:
        if self.event.is_set():
            break
        state = "COMBAT"
        enemy_turns = self.enemy_turns
        player_active = self.player_active
        enemy_active = self.enemy_active
        enemy = self.enemy
        party_turns = self.party_turns
        if len(curr_match) > 0:
            print("Match made, running player process thread")
            for item in curr_match:
                print(curr_match)
                action = item
                update_text = None
                if enemy_active not in self.enemy:
                    enemy_active = self.enemy[0]
                if action == "red":
                    # do physical damage
                    return self.red_attack(self.player_active, enemy_active, self.enemy, enemy_turns)
                elif action == "blue":
                    # deal magic damage
                    att = player_active.get_magic()
                    gua = enemy_active.get_maggua()
                    dmg = att - gua
                    if dmg < 0:
                        dmg = 0
                    enemy_active.set_chp(enemy_active.get_chp() - dmg)
                    update_text = player_active.get_name() + " attacked " + enemy_active.get_name() + " for " + str(dmg) + " damage!"
                    self.party_text.append(update_text)
                    if enemy_active.get_chp() <= 0:
                        update_text = enemy_active.get_name() + " has fallen!"
                        self.party_text.append(update_text)
                        self.enemy_turns = find_and_remove_from_turn(self.enemy_turns, enemy_active)
                        enemy.remove(enemy_active)
                        print(self.enemy_turns)
                        print(enemy)
                elif action == "green":
                    # heal active party member
                    heal = player_active.get_magic()
                    if player_active.get_hp() < player_active.get_chp() + heal:
                        player_active.set_chp(player_active.get_hp())
                    else:
                        player_active.set_chp(player_active.get_chp() + heal)
                    update_text = player_active.get_name() + " healed for " + str(heal) + " damage."
                    self.party_text.append(update_text)
                elif action == "orange":
                    return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
                    # grant support points with this unit
                elif action == "purple":
                    return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
                    # grant support points with next in line?
                elif action == "yellow":
                    return self.red_attack(player_active, enemy_active, enemy, enemy_turns)
                    # recover action points
                if len(enemy) == 0:
                            update_text = player_active.get_name() + "'s party is victorious!"
                            self.party_text.append(update_text)
                            state = "WIN"
                curr_match.remove(curr_match[0])
                if state == "WIN":
                    self.draw(party, self.enemy, self.player_active, "Your party was victorious!", "Your enemies skulk away.", flash_red, xp=exp)
                    self.pyg_wait(5)
                    return "WIN"
            if len(curr_match) == 0:
                if party_current+1 < len(party_turns):
                    party_current += 1
                else:
                    party_current = 0
                self.player_active = party_turns[party_current][0]
                self.party_text.append("It is " + self.player_active.get_name() + "'s turn.")
                curr_match = []
            print("Player process thread concluded.")

"""
def draw_old(self, party, enemy, active, p_text, e_text, flash_red, xp=None, update_text=None):
    if p_text == "Your party was victorious!":
        xp_count = 0
        while True:
            self.display.blit(background, (0,0))
            victory_rect = pygame.Rect(width-1600,height-450,1600,50)
            drawText(self.display, p_text, WHITE, victory_rect, self.font, center=True)
            xp_rect = pygame.Rect(width-1600,height-550,1600,50)
            xp_count += 1
            drawText(self.display, "XP: " + str(xp_count), WHITE, xp_rect, self.font, center=True)
            self.pyg_wait(.01)
            if xp_count == xp:
                self.pyg_wait(3)
                return "WIN"
    if e_text == "Your party was wiped out...":
        self.display.blit(background, (0,0))
        victory_rect = pygame.Rect(width-1600,height-450,1600,50)
        drawText(self.display, e_text, WHITE, victory_rect, self.font, center=True)
        return "DEAD"
    
    color_0 = color_passive
    color_1 = color_passive
    color_2 = color_passive
    color_3 = color_passive

    if flash_red != None:
        if flash_red == 0:
            color_0 = pygame.Color('Red') 
        if flash_red == 1:
            color_1 = pygame.Color('Red') 
        if flash_red == 2:
            color_2 = pygame.Color('Red') 
        if flash_red == 3:
            color_3 = pygame.Color('Red')    

    screen.blit(background, (width+self.i,0))
    screen.blit(background, (self.i, 0))
    if (self.i == -width):
        screen.blit(background, (width+self.i, 0))
        self.i=0
    self.i-=1
    self.board.draw(self.display)
    color_return = BLACK

    if self.timing == 1:
        self.debug_timer = debug_timing("DREW BACKGROUND", self.debug_timer)

    #self.draw_time()
    self.draw_cursor()
    return_rect = pygame.Rect(width-600,height-50,600,50)
    party_1_rect = pygame.Rect(width-500,height-900,500,50)
    party_1_hp_rect = pygame.Rect(width-500,height-850,500,50)
    party_1_portrait_rect = pygame.Rect(width-600,height-900,100,100)
    party_2_rect = pygame.Rect(width-500,height-800,500,50)
    party_2_hp_rect = pygame.Rect(width-500,height-750,500,50)
    party_2_portrait_rect = pygame.Rect(width-600,height-800,100,100)
    party_3_rect = pygame.Rect(width-500,height-700,500,50)
    party_3_hp_rect = pygame.Rect(width-500,height-650,500,50)
    party_3_portrait_rect = pygame.Rect(width-600,height-700,100,100)
    party_4_rect = pygame.Rect(width-500,height-600,500,50)
    party_4_hp_rect = pygame.Rect(width-500,height-550,500,50)
    party_4_portrait_rect = pygame.Rect(width-600,height-600,100,100)

    ability_1_rect = pygame.Rect(width-600,height-500,300,75)
    ability_2_rect = pygame.Rect(width-300,height-500,300,75)
    ability_3_rect = pygame.Rect(width-600,height-425,300,75)
    ability_4_rect = pygame.Rect(width-300,height-425,300,75)

    if self.timing == 1:
        self.debug_timer = debug_timing("MADE RECTS", self.debug_timer)

    pygame.draw.rect(screen, pygame.Color('red'), ability_1_rect)
    pygame.draw.rect(screen, pygame.Color('blue'), ability_2_rect)
    pygame.draw.rect(screen, pygame.Color('green'), ability_3_rect)
    pygame.draw.rect(screen, pygame.Color('purple'), ability_4_rect)

    if self.timing == 1:
        self.debug_timer = debug_timing("DREW ABILITY RECTS", self.debug_timer)

    if return_rect.collidepoint(pygame.mouse.get_pos()):
        color_return = pygame.Color(200,0,0)

    pygame.draw.rect(screen, color_return, return_rect)
    pygame.draw.rect(screen, color_0, party_1_rect)
    pygame.draw.rect(screen, color_0, party_1_hp_rect)
    #pygame.draw.rect(screen, color_passive, party_1_portrait_rect)
    if len(party) > 1:
        pass
        pygame.draw.rect(screen, color_1, party_2_rect)
        pygame.draw.rect(screen, color_1, party_2_hp_rect)
        #pygame.draw.rect(screen, color_passive, party_2_portrait_rect)
    if len(party) > 2:
        pass
        pygame.draw.rect(screen, color_2, party_3_rect)
        pygame.draw.rect(screen, color_2, party_3_hp_rect)
        #pygame.draw.rect(screen, color_passive, party_3_portrait_rect)
    if len(party) > 3:
        pass
        pygame.draw.rect(screen, color_3, party_4_rect)
        pygame.draw.rect(screen, color_3, party_4_hp_rect)
        #pygame.draw.rect(screen, color_passive, party_4_portrait_rect)

    if self.timing == 1:
        self.debug_timer = debug_timing("DREW PARTY RECTS", self.debug_timer)

    port1 = get_portrait(party[0].get_name())
    self.display.blit(port1, party_1_portrait_rect)

    drawText(self.display, party[0].get_name(), WHITE, party_1_rect, self.font, center=True)
    drawText(self.display, "HEALTH: " + str(party[0].get_chp()) + "/" + str(party[0].get_hp()), WHITE, party_1_hp_rect, self.font, center=True)
    
    if len(party) > 1:
        port2 = get_portrait(party[1].get_name())
        self.display.blit(port2, party_2_portrait_rect)
        drawText(self.display, party[1].get_name(), WHITE, party_2_rect, self.font, center=True)
        drawText(self.display, "HEALTH: " + str(party[1].get_chp()) + "/" + str(party[1].get_hp()), WHITE, party_2_hp_rect, self.font, center=True)
    
    if len(party) > 2:
        port3 = get_portrait(party[2].get_name())
        self.display.blit(port3, party_3_portrait_rect)
        drawText(self.display, party[2].get_name(), WHITE, party_3_rect, self.font, center=True)
        drawText(self.display, "HEALTH: " + str(party[2].get_chp()) + "/" + str(party[2].get_hp()), WHITE, party_3_hp_rect, self.font, center=True)
    
    if len(party) > 3:
        port4 = get_portrait(party[3].get_name())
        self.display.blit(port4, party_4_portrait_rect)
        drawText(self.display, party[3].get_name(), WHITE, party_4_rect, self.font, center=True)
        drawText(self.display, "HEALTH: " + str(party[3].get_chp()) + "/" + str(party[3].get_hp()), WHITE, party_4_hp_rect, self.font, center=True)

    if self.timing == 1:
        self.debug_timer = debug_timing("PARTY DONE", self.debug_timer)

    # Enemies
    enemy_1_rect = pygame.Rect(width-300,height-150,300,50)
    enemy_1_hp_rect = pygame.Rect(width-300,height-100,300,50)
    enemy_1_portrait_rect = pygame.Rect(width-400,height-150,100,100)

    #next_rect = pygame.Rect(width-500,height-300,100,100)
    #enemy_2_rect = pygame.Rect(width-300,height-300,300,50)
    #enemy_2_hp_rect = pygame.Rect(width-300,height-250,300,50)
    enemy_2_portrait_rect = pygame.Rect(width-500,height-150,100,100)
    enemy_3_portrait_rect = pygame.Rect(width-600,height-150,100,100)

    pygame.draw.rect(screen, color_passive, enemy_1_rect)
    pygame.draw.rect(screen, color_passive, enemy_1_hp_rect)
    #pygame.draw.rect(screen, color_passive, enemy_1_portrait_rect)

    port_e1 = get_portrait(enemy[0].get_name())
    self.display.blit(port_e1, enemy_1_portrait_rect)
    drawText(self.display, enemy[0].get_name(), WHITE, enemy_1_rect, self.font, center=True)
    if enemy[0].get_chp() > 10:
        drawText(self.display, str(enemy[0].get_chp()) + "/" + str(enemy[0].get_hp()), WHITE, enemy_1_hp_rect, self.font, center=True) 
    else:
        drawText(self.display, "HEALTH: " + str(enemy[0].get_chp()) + "/" + str(enemy[0].get_hp()), WHITE, enemy_1_hp_rect, self.font, center=True) 
    
    if len(enemy) > 1:
        #pygame.draw.rect(screen, color_passive, next_rect)
        port_e2 = get_portrait(enemy[1].get_name())
        #pygame.draw.rect(screen, color_passive, enemy_2_rect)
        #pygame.draw.rect(screen, color_passive, enemy_2_hp_rect)
        #pygame.draw.rect(screen, color_passive, enemy_2_portrait_rect)
        self.display.blit(port_e2, enemy_2_portrait_rect)
        #drawText(self.display, enemy[1].get_name(), WHITE, enemy_2_rect, self.font, center=True)
        #drawText(self.display, "HEALTH: " + str(enemy[1].get_chp()) + "/" + str(enemy[1].get_hp()), WHITE, enemy_2_hp_rect, self.font, center=True)
        #drawText(self.display, "NEXT", WHITE, next_rect, self.font, center=True)

    if len(enemy) > 2:
        #pygame.draw.rect(screen, color_passive, next_rect)
        port_e3 = get_portrait(enemy[2].get_name())
        #pygame.draw.rect(screen, color_passive, enemy_2_rect)
        #pygame.draw.rect(screen, color_passive, enemy_2_hp_rect)
        #pygame.draw.rect(screen, color_passive, enemy_3_portrait_rect)
        self.display.blit(port_e3, enemy_3_portrait_rect)
    
    if self.timing == 1:
        self.debug_timer = debug_timing("ENEMY DONE", self.debug_timer)

    drawText(self.display, "Return", WHITE, return_rect, self.font, center=True) 
    party_box = pygame.Rect(width-600,height-350,600,100) 
    enemy_box = pygame.Rect(width-600,height-250,600,100)
    self.update_box(p_text, party_box)
    self.update_box(e_text, enemy_box)

    #Highlight whose turn it is
    if party[0] == active:
        drawStyleRect(screen, width-500, height-900)
    elif party[1] == active:
        drawStyleRect(screen, width-500, height-800)
    elif party[2] == active:
        drawStyleRect(screen, width-500, height-700)
    elif party[3] == active:
        drawStyleRect(screen, width-500, height-600)

    if self.timing == 1:
        self.debug_timer = debug_timing("HIGHLIGHT DONE", self.debug_timer)

    if self.board.busy == True:
        busy_rect = pygame.Rect(width-350,height-475,200,50)
        pygame.draw.rect(screen, color_passive, busy_rect)  
        drawText(self.display, "Please Wait...", WHITE, busy_rect, self.font, center=True)

    if self.timing == 1:
        self.debug_timer = debug_timing("PLEASE WAIT", self.debug_timer) 

    #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    pygame.display.flip()
    if self.timing == 1:
        self.debug_timer = debug_timing("DRAW DONE", self.debug_timer)
    return return_rect

def update_box_old(self, text, box):
    pygame.draw.rect(screen, color_passive, box)
    self.gl_text("WHITE", text, WHITE, box, self.font, center=True)

"""