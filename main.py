from pdb import set_trace
import json
import settings
from classes.Game import Game

# Import options
settings.init()

N_TEST = 2

for i in range(N_TEST):
    g = Game()
    results = g.run()
    with open("results.json", "a") as outputfile:
        json.dump(results.values, outputfile)
