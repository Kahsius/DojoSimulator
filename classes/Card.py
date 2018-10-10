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

