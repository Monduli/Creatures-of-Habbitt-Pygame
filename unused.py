
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