from pdb import set_trace
import json
import numpy as np

from utils import get_names

def win_rates(results):
    names = get_names()
    victory = []
    played = []

    victory = np.zeros(len(names))
    played = np.zeros(len(names))

    for match in results:
        for name in match['winners_prodigies']:
            index = names.index(name)
            victory[index] = victory[index] + 1
        for duel in match['duels']:
            for name in duel:
                index = names.index(name)
                played[index] = played[index] + 1

    results = {}
    results['names'] = names
    results['rates'] = victory/played

    return(results)

def win_rates_global(results):
    names = get_names()
    victory = []
    played = []

    victory = np.zeros(len(names))
    played = np.zeros(len(names))

    for match in results:
        id_winner = match['winner']
        for duel in match['duels']:
            index_win = names.index(duel[id_winner])
            index_lose = names.index(duel[(id_winner+1)%2])
            victory[index_win] = victory[index_win] + 1
            played[index_win] = played[index_win] + 1
            played[index_lose] = played[index_lose] + 1

    results = {}
    results['names'] = names
    results['rates'] = victory/played

    return(results)


def glyphs_win_rate(results):
    glyphs_winners = [r['glyphs'][r['winner']] for r in results]
    glyphs_winners = map(lambda r: np.array(r), glyphs_winners)
    glyphs_winners = np.mean(list(glyphs_winners), axis=0)

    glyphs_losers = [r['glyphs'][(r['winner']+1)%2] for r in results]
    glyphs_losers = map(lambda r: np.array(r), glyphs_losers)
    glyphs_losers = np.mean(list(glyphs_losers), axis=0)

    return([glyphs_winners, glyphs_losers])

def ko_rate(results):
    return(sum(map(lambda o: o['ko'], results))/len(results))

def prodigies_lead_to_ko(results):
    names = get_names()
    kos = np.zeros(len(names))
    totals = np.zeros(len(names))
    for r in results:
        for p in r['winners_prodigies']:
            index = names.index(p)
            totals[index] = totals[index] + 1
            if r['ko'] and r['winners_prodigies'].index(p) < r['end_turn']:
                kos[index] = kos[index] + 1
    return(kos/totals)

def rate_mastery(results):
    names = get_names()
    activated = np.zeros(len(names))
    totals = np.zeros(len(names))
    for r in results:
        for i in range(len(r['duels'])):
            for j in range(2):
                p = r['duels'][i][j]
                index = names.index(p)
                is_activated = r['mastery_activated'][j][i]
                activated[index] = activated[index] + is_activated
                totals[index] = totals[index] + 1
    return(activated/totals)

