class Log:
    def __init__(self):
        self.values = {}
        self.values['winners_prodigies'] = []
        self.values['winners_player'] = []
        self.values['winner'] = -1
        self.values['duels'] = []
        self.values['ko'] = False
        self.values['hp'] = [0, 0]
        self.values['glyphs'] = [[0,0,0,0],[0,0,0,0]]
        self.values['glyphs_winner'] = []
