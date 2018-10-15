#!/usr/bin/python3

from pdb import set_trace
import json
import subprocess
import sys
import settings
import classes.Debug as debug
from classes.Game import Game
import classes.analyzer as anzr

# Import options
settings.init()

N_TEST = 10000
if(len(sys.argv)) > 1:
    N_TEST = int(sys.argv[1])

# Open file
datafile = open("results.json", "a")
datafile.write('[')

# Run games
print("Test running...")
for i in range(N_TEST):
    g = Game()
    results = g.run()
    json.dump(results.values, datafile)
    if i != N_TEST-1:
        datafile.write(',')
print("... done")


datafile.write(']')
datafile.close()
    
# Start analysis
print("Win Rate par round")
with open("results.json", "r") as json_data:
    results = json.load(json_data)
    wr = anzr.win_rates(results)
    for i in range(len(wr['names'])):
        print(wr['names'][i] + " - " + str(wr['rates'][i]))

print("-"*30)
print("Win Rate par partie")
with open("results.json", "r") as json_data:
    results = json.load(json_data)
    wr = anzr.win_rates_global(results)
    for i in range(len(wr['names'])):
        print(wr['names'][i] + " - " + str(wr['rates'][i]))

# Delete data
subprocess.Popen(["rm", "results.json"])
