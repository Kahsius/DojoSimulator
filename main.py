#!/usr/bin/python3

from pdb import set_trace
from multiprocessing import Pool
import sys
import settings
from classes.Game import Game
import classes.analyzer as anzr

def get_results(i):
    g = Game()
    results = g.run().values
    return(results)

if __name__ == '__main__':
    settings.init()

    N_TEST = 10000
    if(len(sys.argv)) > 1:
        N_TEST = int(sys.argv[1])

    print("Test running...")
    pool = Pool()
    results = pool.map(get_results, range(N_TEST))
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
        name = wr['names'][i]
        score = wr['rates'][i]
        color = '\033[31m' if score > .5 else '\033[32m'
        string = '{} ' + '-'*(13-len(name)) + color + ' {:04.3f}\033[0m'
        string = string.format(name, score)
        print(string)
