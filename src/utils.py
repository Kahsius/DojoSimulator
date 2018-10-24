import json
from numpy import zeros

def get_names():
    names = []
    with open('data/prodigies.json') as json_data:
        d = json.load(json_data)
        for prodigy in d:
            names = names + [prodigy['name']]

    return(names)

def get_list_ids(prodigies):
    names = get_names()
    list_ids = zeros(len(names))
    for p in prodigies:
        index = names.index(p.name)
        list_ids[index] = 1
    return list_ids
