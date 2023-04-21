########
# Used in character generator. Defines the following classes:
# Character
# Fighter
# Paladin
########
import pygame
import random

class Character:
    def __init__(self) -> None:
        self.level = 1
        self.hp = 0
        self.current_hp = 0
        self.physical_guard = 0
        self.magic_guard = 0
        self.physical_attack = 0
        self.quickness = 0
        self.heartiness = 0
        self.magic_attack = 0
        self.healing = 0
        self.chutzpah = 0
        self.name = ""
        self.background = ""
        self.dialog_picture = ""
        self.portrait = "images/"
        self.portrait_dungeon = "images/"
        self.portrait_dialog = "images/"
        self.stats_picture = "images/"
        self.role = ""
        self.xp = 0
        self.bonds = [[0,0] for _ in range(22)]
        self.buff = 0
        self.willpower = 0
        self.stat_spread = None
        self.recruited = False
        self.num = 0
        self.bonds_to_next = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000, 10000000000, 100000000000]
        self.rom_bond_rank = 0
        self.romanced = False
        self.conversation_completeness = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0] for x in range(22)]

        # bonds list:
        # [0] - Main Character (M/F)
        # [1] - Bear N. Steen (M)
        # [2] - Radish Rabbit (F)
        # [3] - Gil Grapefart (M)
        # [4] - Lam'baste Lamb (F)
        # [5] - Sunny Spider (F)
        # [6] - Victor (M)
        # [7] - Donkey Hote (M)
        # [8] - Sidney Shark (F)
        # [9] - Romance NPC 9
        # [10] - Hollow
        # [11] - Henrietta
        # [12] - Grilla
        # [13] - Dane
        # [14] - Rayna
        # [15] - Ranch NPC
        # [16] - Story NPC
        # [17] - Story NPC
        # [18] - Story NPC
        # [19] - Story NPC
        # [20] - Ward N. Steen
        # [21] - Juliette

    def get_level(self):
        return self.level
    
    def get_hp(self):
        return self.hp
    
    def get_chp(self):
        return self.current_hp
    
    def get_physical_guard(self):
        return self.physical_guard
    
    def get_magical_guard(self):
        return self.magic_guard

    def get_physical_attack(self):
        return self.physical_attack

    def get_magic_attack(self):
        return self.magic

    def get_quickness(self):
        return self.quickness

    def get_heartiness(self):
        return self.heartiness

    def get_healing(self):
        return self.healing

    def get_chutzpah(self):
        return self.chutzpah
    
    def get_willpower(self):
        return self.willpower

    def get_background(self):
        return self.background
    
    def get_name(self):
        return self.name
    
    def get_dialog_picture(self):
        return self.dialog_picture
    
    def get_portrait(self):
        return self.portrait
    
    def get_portrait_dialog(self):
        return self.portrait_dialog
    
    def get_stats_picture(self):
        return self.stats_picture
    
    def get_portrait_dungeon(self):
        return self.portrait_dungeon
    
    def get_portrait_dungeon_name(self):
        return self.portrait_dungeon_name
    
    def get_role(self):
        return self.role
    
    def get_buff(self):
        return self.buff
    
    def get_xp(self):
        return self.xp
    
    def get_bonds(self):
        return self.bonds
    
    def get_bond_rank(self, char_num):
        return self.bonds[char_num][0]
    
    def get_bond_points(self, char_num):
        return self.bonds[char_num][1]
    
    def get_needed_to_next_rank(self, rank):
        return self.bonds_to_next[rank]
    
    def get_recruited(self):
        return self.recruited
    
    def get_num(self):
        return self.num
    
    def get_level(self):
        return self.level
    
    def get_romanced(self):
        return self.romanced
    
    def get_rom_bond_rank(self, rom):
        if rom == True:
            return self.rom_bond_rank
        else:
            return 0

    def set_hp(self, value):
        self.hp = value

    def set_chp(self, value):
        self.current_hp = value

    def set_physical_guard(self, value):
        self.physical_guard = value

    def set_magical_guard(self, value):
        self.magic_guard = value

    def set_physical_attack(self, value):
        self.physical_attack = value

    def set_quickness(self, value):
        self.quickness = value

    def set_heartiness(self, value):
        self.heartiness = value

    def set_magic_attack(self, value):
        self.magic = value

    def set_healing(self, value):
        self.healing = value

    def set_chutzpah(self, value):
        self.chutzpah = value

    def set_willpower(self, value):
        self.willpower = value

    def set_background(self, value):
        self.background = value

    def set_name(self, value):
        self.name = value

    def set_buff(self, value):
        self.buff = value

    def set_level(self, value):
        self.level = value

    def set_dialog_picture(self, value):
        pic = pygame.image.load("images/" + value).convert_alpha()
        self.dialog_picture = pic

    def set_portrait(self, value):
        self.portrait = pygame.image.load("images/" + value).convert_alpha()
        self.portrait_name = "images/" + value
        
    def set_portrait_dialog(self, value):
        self.portrait_dialog = pygame.image.load("images/" + value + ".png").convert_alpha()

    def set_stats_picture(self, value):
        self.stats_picture = pygame.image.load("images/" + value + ".png").convert_alpha()

    def set_portrait_dungeon(self, value):
        portrait = pygame.image.load("images/" + value + ".png").convert_alpha()
        portrait = pygame.transform.scale(portrait,(60,120))
        self.portrait_dungeon = portrait
        self.portrait_dungeon_name = "images/" + value

    def set_recruited(self, value):
        self.recruited = value

    def set_xp(self, value):
        self.xp = value

    def set_bonds(self, value):
        self.bonds = value

    def distribute_stats(self, spread, stats):
        temp = stats
        for i in range(6):
            if spread[i] == "phys":
                self.set_physical_attack(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "quick":
                self.set_quickness(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "heart":
                self.set_heartiness(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "magic":
                self.set_magic_attack(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "heal":
                self.set_healing(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "chutz":
                self.set_chutzpah(max(temp))
                stats.remove(max(temp))

    def calculate_stats(self):
        armor_phys = 0
        armor_mag = 0
        #physical guard
        self.set_physical_guard(armor_phys + self.get_heartiness())
        #magical guard
        self.set_magical_guard(armor_mag + self.get_magic_attack())
        #health
        self.set_hp(10*self.get_heartiness())
        self.set_chp(10*self.get_heartiness())
       # self.set_willpower(self.get_chutzpah() - self.get_heartiness())
        self.set_willpower(10)

    def print_stats(self):
        print("PHYSATT: " + str(self.physical_attack) +
              " QUICK: " + str(self.quickness) +
                " MAGATT: " + str(self.magic_attack) +
                 " HEART: " + str(self.heartiness) +
                  " HEAL: " + str(self.healing) +
                   " CHUTZ: " + str(self.chutzpah))
    
    def level_up(self, spread):
        self.level += 1
        temp = [random.randint(2, 3), random.randint(1, 2), random.randint(1, 2), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
        for i in range(6):
            if spread[i] == "phys":
                self.set_physical_attack(self.get_physical_attack()+temp[i])
            elif spread[i] == "quick":
                self.set_quickness(self.get_quickness()+temp[i])
            elif spread[i] == "heart":
                self.set_heartiness(self.get_heartiness()+temp[i])
            elif spread[i] == "magic":
                self.set_magic_attack(self.get_magic_attack()+temp[i])
            elif spread[i] == "heal":
                self.set_healing(self.get_healing()+temp[i])
            elif spread[i] == "chutz":
                self.set_chutzpah(self.get_chutzpah()+temp[i])
        self.calculate_stats()

    def add_support_points(self, target, points, mcname):
        p = self.which_num_party_member_bonds(target, mcname)
        
        self.bonds[p][1] += points
        
        if self.bonds[p][1] >= self.bonds_to_next[self.bonds[p][0]]:
            self.bonds[p][1] = 0
            self.bonds[p][0] += 1
            print("Bond has ranked up to rank " + str(self.bonds[p][0]))

    def boost(self, target, spread):
        for x in range(0, target):
            self.level_up(spread)

    def add_xp(self, amount):
        self.xp += amount

    def fill_xp_array(self):
        self.xp_tiers = [0] * 9998
        y = 0
        for x in self.xp_tiers:
            x = 100 + 100*y
            y+=1
    
    def has_xp_to_level_up(self):
        if self.level < 9999:
            if self.xp >= self.xp_tiers[self.level-1]:
                self.level_up(self.stat_spread)
                return True
            else:
                return False
        else:
            return False
        
    def which_num_party_member_bonds(self, m_n, mc_name):
        # bonds list:
            # [0] - Main Character (M/F)
            # [1] - Bear N. Steen (M)
            # [2] - Radish Rabbit (F)
            # [3] - Gil Grapefart (M)
            # [4] - Lam'baste Lamb (F)
            # [5] - Sunny Spider (F)
            # [6] - Oscar Lion (M)
            # [7] - Hans Horse (M)
            # [8] - Sidney Shark (F)
            # [9] - None
            # [10] - Hollow
            # [11] - Henrietta
            # [12] - Grilla
            # [13] - Dane
            # [14] - Rayna
            # [15] - None
            # [16] - None
            # [17] - None
            # [18] - None
            # [19] - None
            # [20] - None
            # [21] - None
        if m_n == mc_name:
            return 0
        if m_n == "N. Steen":
            return 1
        if m_n == "Radish":
            return 2
        if m_n == "Grapefart":
            return 3
        if m_n == "Lam'baste":
            return 4
        if m_n == "Sunny":
            return 5
        if m_n == "Oscar":
            return 6
        if m_n == "Hans":
            return 7
        if m_n == "Sidney":
            return 8
        if m_n == "TBH":
            return 9
        if m_n == "Hollow":
            return 10
        if m_n == "Henrietta":
            return 11
        if m_n == "Grilla":
            return 12
        if m_n == "Dane":
            return 13
        if m_n == "Rayna":
            return 14
        if m_n == "TBH":
            return 15
        if m_n == "TBH":
            return 16
        
    def get_conversation_completeness(self, name, mc_name):
        p = self.which_num_party_member_bonds(name, mc_name)
        return self.conversation_completeness[p]
    
    def get_all_conv_comp(self):
        return self.conversation_completeness
    
    def set_conversation_completeness(self, name, mc_name, rank):
        p = self.which_num_party_member_bonds(name, mc_name)
        self.conversation_completeness[p][rank-1] = 1

    def set_all_conv_comp(self, comp):
        self.conversation_completeness = comp

class MainCharacter(Character):
    def __init__(self, stats, poss_image=None, name=None) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "LEADER"
        self.stat_spread = ["phys", "heart", "quick", "heal", "chutz", "magic"]
        self.fill_xp_array()
        if name != None:
            self.set_name(name)
        if poss_image != None:
            self.set_pictures_mc(poss_image)
        self.set_recruited(True)
        

    def spread(self, stats):
        self.distribute_stats(["phys", "heart", "quick", "heal", "chutz", "magic"], stats)
        self.calculate_stats()

    def set_pictures_mc(self, poss_image):
        self.set_dialog_picture(poss_image + "_port.png")
        self.set_portrait(poss_image + "_port_100.png")
        self.set_portrait_dungeon(poss_image)
        self.set_portrait_dialog(poss_image + "_portrait")
        self.set_stats_picture(poss_image + "_port_stats")

class Martial(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "MARTIAL ADEPT"
        self.stat_spread = ["phys", "heart", "quick", "heal", "chutz", "magic"]
        self.fill_xp_array()

    def spread(self, stats):
        Character.distribute_stats(self, ["phys", "heart", "quick", "heal", "chutz", "magic"], stats)
        self.calculate_stats(self)

class BearNSteen(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.set_portrait("bear_portrait_100.png")
        self.set_dialog_picture("bear.png")
        self.set_portrait_dungeon("bear")
        self.set_portrait_dialog("bear_portrait")
        self.set_stats_picture("bear_port_stats")
        self.role = "BEAR KNIGHT"
        self.stat_spread = ["chutz", "phys", "heart", "quick", "heal", "magic"]
        self.fill_xp_array()
        self.num = 1
        self.set_name("N. Steen")
        self.set_portrait_dungeon("bear")
        self.recruited = True

    def spread(self, stats):
        Character.distribute_stats(self, ["chutz", "phys", "heart", "quick", "heal", "magic"], stats)
        self.calculate_stats()

    def set_dialog_picture(self, value):
        image = pygame.image.load("images/" + value).convert_alpha()
        image = pygame.transform.scale(image, (700, 1021))
        self.dialog_picture = image

class Radish(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "BOOKKEEPER"
        self.set_portrait("rabbit_portrait_100.png")
        self.stat_spread = ["magic", "quick", "heal", "heart", "chutz", "phys"]
        self.fill_xp_array()
        self.set_stats_picture("rabbit_port_stats")
        self.num = 2
        self.set_name("Radish")
        self.set_portrait_dungeon("bear")

    def spread(self, stats):
        Character.distribute_stats(self, ["magic", "quick", "heal", "heart", "chutz", "phys"], stats)
        self.calculate_stats()

class Grapefart(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "MERCHANT"
        self.set_portrait("grapefart_portrait_100.png")
        self.stat_spread = ["quick", "heal", "chutz", "phys", "heart", "magic"]
        self.fill_xp_array()
        self.set_stats_picture("grapefart_port_stats")
        self.set_name("Grapefart")
        self.num = 3

    def spread(self, stats):
        Character.distribute_stats(self, ["quick", "heal", "chutz", "phys", "heart", "magic"], stats)
        self.calculate_stats()

class Cleric(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "APOTHECARY"
        self.set_portrait("cinna_portrait_100.png")
        self.stat_spread = ["heal", "phys", "magic", "heart", "quick", "chutz"]
        self.fill_xp_array()

    def spread(self, stats):
        Character.distribute_stats(self, ["heal", "phys", "magic", "heart", "quick", "chutz"], stats)
        self.calculate_stats()

class Henrietta(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "INNKEEPER"
        self.set_portrait("hippo_port_100.png")
        self.stat_spread = ["phys", "heal", "chutz", "quick", "heart", "magic"]
        self.fill_xp_array()
        self.set_stats_picture("hippo_port_stats")
        self.set_name("Henrietta")
        self.num = 11

    def spread(self, stats):
        Character.distribute_stats(self, ["phys", "heal", "chutz", "quick", "heart", "magic"], stats)
        self.calculate_stats()

class Dane(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "DETECTIVE"
        self.set_portrait("dane_port_100.png")
        self.stat_spread = ["quick", "phys", "chutz", "heal", "heart", "magic"]
        self.fill_xp_array()
        self.set_name("Dane")
        self.set_stats_picture("dane_port_stats")
        self.num = 13

    def spread(self, stats):
        Character.distribute_stats(self, ["quick", "phys", "chutz", "heal", "heart", "magic"], stats)
        self.calculate_stats()

class Rayna(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "HABERDASHER"
        self.set_portrait("rayna_port_100.png")
        self.stat_spread = ["magic", "chutz", "phys", "heal", "quick", "heart"]
        self.fill_xp_array()
        self.set_name("Rayna")
        self.set_stats_picture("rayna_port_stats")
        self.num = 14

    def spread(self, stats):
        Character.distribute_stats(self, ["magic", "chutz", "phys", "heal", "quick", "heart"], stats)
        self.calculate_stats()

class BlankCharacter(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "NONE"
        self.set_portrait("blank.png")
        self.stat_spread = ["magic", "chutz", "phys", "heal", "quick", "heart"]
        self.fill_xp_array()
        self.set_name("BLANK")
        self.set_stats_picture("blank")

    def spread(self, stats):
        Character.distribute_stats(self, ["magic", "chutz", "phys", "heal", "quick", "heart"], stats)
        self.calculate_stats()

class Enemy():
    def __init__(self, name, health, att, gua, quickness, maggua, xp):
        self.name = name
        self.hp = health #Max Health
        self.chp = health
        self.attack = att
        self.guard = gua
        self.quickness = quickness
        self.magguard = maggua
        self.xp = xp

    def get_name(self):
        return self.name
    
    def get_hp(self):
        return self.hp
    
    def get_chp(self):
        return self.chp
    
    def get_attack(self):
        return self.attack
    
    def get_guard(self):
        return self.guard 
    
    def get_quickness(self):
        return self.quickness
    
    def get_magical_guard(self):
        return self.magguard
    
    def get_xp(self):
        return self.xp
    
    def set_chp(self, value):
        self.chp = value