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
        self.background = ""
    
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

    def get_background(self):
        return self.background

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

    def set_background(self, value):
        self.background = value

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
            elif spread[i] == "int":
                self.set_int(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "wis":
                self.set_wis(max(temp))
                stats.remove(max(temp))
            elif spread[i] == "cha":
                self.set_cha(max(temp))
                stats.remove(max(temp))


class Martial(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.stats = stats

    def spread(stats):
        Character.distribute_stats(["str", "con", "dex", "wis", "cha", "int"], stats)

class Paladin(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.stats = stats

    def spread(stats):
        Character.distribute_stats(["cha", "str", "con", "dex", "wis", "int"], stats)

class Bookish(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.stats = stats

    def spread(stats):
        Character.distribute_stats(["int", "con", "dex", "wis", "cha", "str"], stats)

class Ranger(Character):
    def __init__(self, stats) -> None:
        super().__init__()
        self.stats = stats

    def spread(stats):
        Character.distribute_stats(["dex", "wis", "con", "str", "cha", "int"], stats)