import json
import numpy as np

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


def get_names():
    names = []
    with open('data.json') as json_data:
        d = json.load(json_data)
        for prodigy in d:
            names = names + [prodigy['name']]
    
    return(names)

# def glyphs_win_rate(results):

