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
    return list_ids.astype(int).tolist()

def generate_all_action1():
    actions = []:
        total = 4
        for i0 in range(5):
            total = total - i0
            for i1 in range(min(total, 4)):
                total = total - i1
                for i2 in range(min(total, 4)):
                    total = total - i2
                    for i3 in range(min(total, 3)):
                        total = total - i3
                        for i4 in range(min(total, 3)):
                            total = total - i4
                            for i5 in range(min(total, 2):
                                if not (i4 == 2 and i5 == 1):
                                    actions.append([i0, i1, i2, i3, i4, i5])

