########
# Used in character generator. Defines the following classes:
# Character
# Fighter
# Paladin
########

class Character:
    def __init__(self) -> None:
        self.hp = 0
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        self.name = ""
    
    def get_hp(self):
        return self.hp

    def get_str(self):
        return self.strength

    def get_dex(self):
        return self.dexterity

    def get_con(self):
        return self.constitution

    def get_int(self):
        return self.intelligence

    def get_wis(self):
        return self.wisdom

    def get_cha(self):
        return self.charisma

    def set_str(self, value):
        self.strength = value

    def set_dex(self, value):
        self.dexterity = value

    def set_con(self, value):
        self.constitution = value

    def set_int(self, value):
        self.intelligence = value

    def set_wis(self, value):
        self.wisdom = value

    def set_cha(self, value):
        self.charisma = value

class Fighter(Character):
    def __init__(self) -> None:
        super().__init__()

class Paladin(Character):
    def __init__(self) -> None:
        super().__init__()