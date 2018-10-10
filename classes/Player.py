class Player:
    def __init__(self, order):
        self.pseudo = "Default"
        self.hand = []
        self.played_glyphs = 4 * [0] + 3 * [1] + 3 * [2] + 2 * [3] + [4]
        self.played_prodigy = None
        self.prodigies = []
        self.hp = 10
        self.isFirst = True if order else False
        self.regard = False
        
        glyph = 5 if self.isFirst else 4
        self.played_glyphs = self.played_glyphs + [glyph]

    def get_random_glyphe_index(feinte_allowed = True):
        h = self.hand
        if feinte_allowed:
            return randint(0,len(h)-1)
        else :
            for i in range(len(h)-1):
                if h[i] != 0:
                    return i
        return -1

