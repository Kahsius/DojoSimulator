import random
import json
import pdb

class Game:
    def __init__(self):
        self.players = []
        self.voies = []
        self.round = 0

        for i in range(2):
            self.players.append(Player(i))

        with open('../data.json') as json_data:
            d = json.load(json_data)
            selected = d[random.sample(range(len(d), 8))]
            self.players[0].prodigies = selected[0:4]
            self.players[1].prodigies = selected[4:8]


