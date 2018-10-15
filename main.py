#!/usr/bin/python3

from pdb import set_trace
import sys
import settings
from classes.Game import Game
import classes.analyzer as anzr

# Import options
settings.init()

N_TEST = 10000
if(len(sys.argv)) > 1:
    N_TEST = int(sys.argv[1])

results = []

# Run games
print("Test running...")
for i in range(N_TEST):
    g = Game()
    results.append(g.run().values)
print("... done")

# Start analysis
print("Win Rate par round")
wr = anzr.win_rates(results)
for i in range(len(wr['names'])):
    print(wr['names'][i] + " - " + str(wr['rates'][i]))

print("-"*30)
print("Win Rate par partie")
wr = anzr.win_rates_global(results)
for i in range(len(wr['names'])):
    print(wr['names'][i] + " - " + str(wr['rates'][i]))
