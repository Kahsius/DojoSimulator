import random

class Player:
    def __init__(self, order):
        self.pseudo = "Default"
        self.hand = 4 * [0] + 3 * [1] + 3 * [2] + 2 * [3] + [4]
        self.played_glyphs = []
        self.played_prodigy = None
        self.prodigies = []
        self.hp = 10
        self.isFirst = True if order else False
        self.has_regard = False
        
        glyph = 5 if self.isFirst else 4
        self.hand = self.hand + [glyph]
        random.shuffle(self.hand)

    def get_random_glyphe_index(feinte_allowed = True):
        h = self.hand
        if feinte_allowed:
            return randint(0,len(h)-1)
        else :
            for i in range(len(h)-1):
                if h[i] != 0:
                    return i
        return -1

    def get_choosen_glyphs():
        p = self.played_prodigy.get_p()
        sum_g = 0
        g = []
        l = len(self.hand)
        
        # On complète la main avec des Glyphes non Feinte
        for i in range(l):
            if sum_g + hand[l-i-1] <= p and hand[l-i-1] != 0 :
                g = g + [hand[l-i-1]]
                sum_g = sum_g + [hand[l-i-1]]
                del hand[l-i-1]
            # Dans 80% des cas, le dernier Glyphe sera une feinte
            if len(g) == 3 and random.random() > .2 or len(g) == 4:
                break
        
        # Quand on peut plus, on complète ce qui manque avec des Feintes
        for i in range(4-len(g)):
            index = g.index(0)
            g = g + [hand[l-i-1]]
            del hand[l-i-1]

        # On mélange les Glyphs joués pour que les Feintes bougent
        self.played_glyphs = random.shuffle(g)
