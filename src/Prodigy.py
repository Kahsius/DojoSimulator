from Capacity import Capacity

class Prodigy:
    def __init__(self, json, owner):
        self.owner = owner
        self.name = json['name']
        self.power = 0
        self.power_base = json['power']
        self.damage = 0
        self.damage_base = json['damage']
        self.talent = Capacity(json['talent'], owner = owner)
        self.mastery = Capacity(json['mastery'], owner =  owner)
        self.turn = [] + self.talent.turn + self.mastery.turn
        self.turn = [] if len(self.turn) == 4 else self.turn
        self.element = json['element']
        self.protected = False
        self.advantaged = False
        self.initiative = False
        self.is_played = False

    def get_p(self):
        return(self.power_base + self.power)

    def get_d(self):
        return(self.damage_base + self.damage)
