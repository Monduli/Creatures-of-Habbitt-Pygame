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
        self.portrait = "images/"
        self.portrait_dungeon = "images/"
        self.role = ""
        # bonds list:
        # [0] - Main Character
        # [1] - Bear N. Steen
        # [2] - Radish Rabbit
        # [3] - Gil Grapefart
        # [4] - None
        # [5] - None
        # [6] - Cinnamon Bun
        # [7] - None
        # [8] - None
        self.bonds = [0, 0, 0, 0, 0, 0, 0]
    
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

    def get_quickness(self):
        return self.quickness

    def get_heartiness(self):
        return self.heartiness

    def get_magic_attack(self):
        return self.magic

    def get_healing(self):
        return self.healing

    def get_chutzpah(self):
        return self.chutzpah

    def get_background(self):
        return self.background
    
    def get_name(self):
        return self.name
    
    def get_portrait(self):
        return self.portrait
    
    def get_portrait_dungeon(self):
        return self.portrait_dungeon
    
    def get_portrait_dungeon_name(self):
        return self.portrait_dungeon_name
    
    def get_role(self):
        return self.role

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

    def set_background(self, value):
        self.background = value

    def set_name(self, value):
        self.name = value

    def set_portrait(self, value):
        self.portrait = pygame.image.load("images/" + value)
        self.portrait_name = "images/" + value

    def set_portrait_dungeon(self, value):
        portrait = pygame.image.load("images/" + value + ".png")
        portrait = pygame.transform.scale(portrait,(60,120))
        self.portrait_dungeon = portrait
        self.portrait_dungeon_name = "images/" + value

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

    def print_stats(self):
        print("PHYSATT: " + str(self.physical_attack) +
              " QUICK: " + str(self.quickness) +
                " MAGATT: " + str(self.magic_attack) +
                 " HEART: " + str(self.heartiness) +
                  " HEAL: " + str(self.healing) +
                   " CHUTZ: " + str(self.chutzpah))
    
    def level_up(self, spread):
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

    def add_support_points(self, target, points, mcname):
        if target == mcname:
            self.bonds[0] += points
        if target == "N. Steen":
            self.bonds[1] += points
        if target == "Radish":
            self.bonds[2] += points
        if target == "Grapefart":
            self.bonds[3] += points
        if target == "4":
            self.bonds[4] += points
        if target == "5":
            self.bonds[5] += points
        if target == "Cinna":
            self.bonds[6] += points
        if target == "7":
            self.bonds[7] += points
        if target == "8":
            self.bonds[8] += points

class MainCharacter(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "DISPLACED RULER"

    def spread(self, stats):
        self.distribute_stats(["phys", "heart", "quick", "heal", "chutz", "magic"], stats)
        self.calculate_stats()

class Martial(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "MARTIAL ADEPT"

    def spread(self, stats):
        Character.distribute_stats(self, ["phys", "heart", "quick", "heal", "chutz", "magic"], stats)
        self.calculate_stats(self)

class BearKnight(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.set_portrait("bear_portrait_100.png")
        self.set_portrait_dungeon("bear")
        self.role = "BEAR KNIGHT"

    def spread(self, stats):
        Character.distribute_stats(self, ["chutz", "phys", "heart", "quick", "heal", "magic"], stats)
        self.calculate_stats()

class Bookish(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "BOOKKEEPER"
        self.set_portrait("rabbit_portrait_100.png")

    def spread(self, stats):
        Character.distribute_stats(self, ["magic", "quick", "heal", "heart", "chutz", "phys"], stats)
        self.calculate_stats()

class Merchant(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "MERCHANT"
        self.set_portrait("grapefart_portrait_100.png")

    def spread(self, stats):
        Character.distribute_stats(self, ["quick", "heal", "chutz", "phys", "heart", "magic"], stats)
        self.calculate_stats()

class Cleric(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.role = "APOTHECARY"
        self.set_portrait("cinna_portrait_100.png")

    def spread(self, stats):
        Character.distribute_stats(self, ["heal", "phys", "magic", "heart", "quick", "chutz"], stats)
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