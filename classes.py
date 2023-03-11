########
# Used in character generator. Defines the following classes:
# Character
# Fighter
# Paladin
########
import pygame

class Character:
    def __init__(self) -> None:
        self.hp = 0
        self.current_hp = 0
        self.phys_guard = 0
        self.magic_guard = 0
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.magic = 0
        self.wisdom = 0
        self.charisma = 0
        self.name = ""
        self.background = ""
        self.portrait = "images/"
        self.portrait_dungeon = "images/"
        self.role = ""
    
    def get_hp(self):
        return self.hp
    
    def get_chp(self):
        return self.current_hp
    
    def get_phys_guard(self):
        return self.phys_guard
    
    def get_mag_guard(self):
        return self.magic_guard

    def get_str(self):
        return self.strength

    def get_dex(self):
        return self.dexterity

    def get_con(self):
        return self.constitution

    def get_mag(self):
        return self.magic

    def get_wis(self):
        return self.wisdom

    def get_cha(self):
        return self.charisma

    def get_background(self):
        return self.background
    
    def get_name(self):
        return self.name
    
    def get_portrait(self):
        return self.portrait
    
    def get_portrait_dungeon(self):
        return self.portrait_dungeon
    
    def get_role(self):
        return self.role

    def set_hp(self, value):
        self.hp = value

    def set_chp(self, value):
        self.current_hp = value

    def set_phys_guard(self, value):
        self.phys_guard = value

    def set_mag_guard(self, value):
        self.magic_guard = value

    def set_str(self, value):
        self.strength = value

    def set_dex(self, value):
        self.dexterity = value

    def set_con(self, value):
        self.constitution = value

    def set_mag(self, value):
        self.magic = value

    def set_wis(self, value):
        self.wisdom = value

    def set_cha(self, value):
        self.charisma = value

    def set_background(self, value):
        self.background = value

    def set_name(self, value):
        self.name = value

    def set_portrait(self, value):
        self.portrait = pygame.image.load("images/" + value)

    def set_portrait_dungeon(self, value):
        portrait = pygame.image.load("images/" + value)
        portrait = pygame.transform.scale(portrait,(60,120))
        self.portrait_dungeon = portrait

    def distribute_stats(self, spread, stats):
        temp = stats
        for i in range(6):
            if spread[i] == "str":
                self.set_str(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "dex":
                self.set_dex(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "con":
                self.set_con(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "mag":
                self.set_mag(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "wis":
                self.set_wis(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "cha":
                self.set_cha(max(temp))
                stats.remove(max(temp))

    def calculate_stats(self):
        armor_phys = 0
        armor_mag = 0
        #physical guard
        self.set_phys_guard(armor_phys + self.get_con())
        #magical guard
        self.set_mag_guard(armor_mag + self.get_mag())
        #health
        self.set_hp(10*self.get_con())
        self.set_chp(10*self.get_con())


    def print_stats(self):
        print("STR: " + str(self.strength) +
              " DEX: " + str(self.dexterity) +
                " MAG: " + str(self.magic) +
                 " CON: " + str(self.constitution) +
                  " WIS: " + str(self.wisdom) +
                   " CHA: " + str(self.charisma))

class MainCharacter(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.hp = 20
        self.current_hp = 20
        self.role = "DISPLACED RULER"

    def spread(self, stats):
        self.distribute_stats(["str", "con", "dex", "wis", "cha", "mag"], stats)
        self.calculate_stats()

    def get_magic(self):
        return self.get_mag()


class Martial(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.hp = 50
        self.current_hp = 50
        self.role = "MARTIAL ADEPT"

    def spread(self, stats):
        Character.distribute_stats(self, ["str", "con", "dex", "wis", "cha", "mag"], stats)
        self.calculate_stats(self)

    def get_magic(self):
        return self.get_mag()

class BearKnight(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.hp = 50
        self.current_hp = 50
        self.set_portrait("bear_portrait_100.png")
        self.set_portrait_dungeon("bear.png")
        self.role = "BEAR KNIGHT"

    def spread(self, stats):
        Character.distribute_stats(self, ["cha", "str", "con", "dex", "wis", "mag"], stats)
        self.calculate_stats()

    def get_magic(self):
        return self.get_cha()

class Bookish(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.hp = 20
        self.current_hp = 20
        self.role = "BOOKKEEPER"
        self.set_portrait("rabbit_portrait_100.png")

    def spread(self, stats):
        Character.distribute_stats(self, ["mag", "con", "dex", "wis", "cha", "str"], stats)
        self.calculate_stats()

    def get_magic(self):
        return self.get_mag()

class Merchant(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.hp = 30
        self.current_hp = 30
        self.role = "MERCHANT"
        self.set_portrait("grapefart_portrait_100.png")

    def spread(self, stats):
        Character.distribute_stats(self, ["dex", "wis", "con", "str", "cha", "mag"], stats)
        self.calculate_stats()
        
    def get_magic(self):
        return self.get_dex()

class Cleric(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.spread(stats)
        self.hp = 30
        self.current_hp = 30
        self.role = "APOTHECARY"
        self.set_portrait("cinna_portrait_100.png")

    def spread(self, stats):
        Character.distribute_stats(self, ["mag", "cha", "wis", "con", "dex", "str"], stats)
        self.calculate_stats()
        
    def get_magic(self):
        return self.get_mag()

class Enemy():
    def __init__(self, name, health, att, gua, dex, maggua, xp):
        self.name = name
        self.hp = health #Max Health
        self.chp = health
        self.attack = att
        self.guard = gua
        self.dex = dex
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
    
    def get_dex(self):
        return self.dex
    
    def get_maggua(self):
        return self.magguard
    
    def get_xp(self):
        return self.xp
    
    def set_chp(self, value):
        self.chp = value