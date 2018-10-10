from Capacity import Capacity

class Card:
    def __init__(self, json):
        self.name = json['name']
        self.power = 0
        self.power_base = json['power']
        self.damage = 0
        self.damage_base = json['damage']
        self.talent = Capacity(json['talent'])
        self.mastery = Capacity(json['mastery'])
        self.element = json['element']
        self.protected = False
        self.advantaged = False
        self.initiative = False

    def get_p(self):
        return(self.power_base + self.power)

    def get_d(self):
        return(self.damage_base + self.damage)
