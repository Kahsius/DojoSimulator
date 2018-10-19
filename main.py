#!/usr/bin/python3

import sys
from os import getcwd
sys.path.insert(0, getcwd()+'/scripts')

import settings
settings.init()

import analyzer as anzr

from subprocess import run
from pdb import set_trace
from multiprocessing import Pool
from Game import Game


def get_results(i):
    g = Game()
    results = g.run().values
    return(results)

if __name__ == '__main__':
    # run('clear')

    N_TEST = 10000
    if(len(sys.argv)) > 1:
        N_TEST = int(sys.argv[1])

    print("Test running...")
    pool = Pool()
    results = pool.map(get_results, range(N_TEST))
    print("... done\n")

    # Start analysis
    # print("Win Rate par round")
    # wr = anzr.win_rates(results)
    # for i in range(len(wr['names'])):
        # print(wr['names'][i] + " - " + str(wr['rates'][i]))

    print("Win Rate par partie")
    wr = anzr.win_rates_global(results)
    ok = []
    notok = []
    for i in range(len(wr['names'])):
        name = wr['names'][i]
        score = wr['rates'][i]
        if abs(score - .5) > settings.TOLERANCE_COLOR:
            color = settings.COLOR_RED
            string = '\t{} ' + '-'*(13-len(name)) + color + ' {:04.3f}' + settings.COLOR_BLACK
            string = string.format(name, score)
            notok.append(string)
        else:
            color = settings.COLOR_BLUE
            string = '\t{} ' + '-'*(13-len(name)) + color + ' {:04.3f}' + settings.COLOR_BLACK
            string = string.format(name, score)
            ok.append(string)
    ok.sort()
    notok.sort()
    print("-- OK")
    for s in ok:
        print(s)
    print("-- not OK")
    for s in notok:
        print(s)

    print("\nKo rate : {:03.2f}".format(anzr.ko_rate(results)))

    print("\nKo rate par Prodige :")
    names = anzr.get_names()
    kos_prodigies = anzr.prodigies_lead_to_ko(results)
    strings = []
    for i in range(len(names)):
        string = '\t{} ' + '-'*(13-len(names[i])) + ' {:04.3f}'
        string = string.format(names[i], kos_prodigies[i])
        strings.append(string)
    strings.sort()
    for s in strings:
        print(s)

    mean_glyphs = anzr.glyphs_win_rate(results)
    print("\nMean Glyphs par win status :")
    elements = ['anar', 'sulimo', 'ulmo', 'wilwar']
    print("\tElement" + " "*5 + "Winner" + " "*3 + "Loser")
    for i in range(4):
        elem = elements[i]
        string = '\t{}   ' + ' '*(9-len(elem)) + '{:03.2f}' + ' '*5 + '{:03.2f}'
        print(string.format(elem, mean_glyphs[0][i], mean_glyphs[1][i]))

