import json
import settings

def get_id_prodigy(name):
    with open('data/prodigies.json') as json_data:
        d = json.load(json_data)
        for i in range(len(d)):
            if d[i]['name'] == name:
                return i
    return -1

def verbose(string):
    if settings.VERBOSE:
        print(string)
