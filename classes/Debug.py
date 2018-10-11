import json

def get_id_prodigy(name):
    with open('data.json') as json_data:
        d = json.load(json_data)
        for i in range(len(d)):
            if d[i]['name'] == name:
                return i
    return -1
