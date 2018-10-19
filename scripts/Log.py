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
        self.values['end_turn'] = 0
        self.values['mastery_activated'] = [[False]*4, [False]*4]
