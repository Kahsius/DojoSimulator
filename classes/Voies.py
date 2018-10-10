class Voie:
    def __init__(self, json):
        self.element = json['element']
        self.capacity = Capacity(json['capacity'])
