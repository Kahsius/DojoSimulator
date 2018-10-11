from pdb import set_trace
import json
from classes.Game import Game

N_TEST = 2

for i in range(N_TEST):
    g = Game()
    results = g.run()
    with open("results.json", "a") as outputfile:
        json.dump(self.log.values, outputfile)
