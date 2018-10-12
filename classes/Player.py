import settings
from pdb import set_trace
import random

class Player:
    def __init__(self, order):
        self.pseudo = "Default"
        self.hand = 4 * [0] + 3 * [1] + 3 * [2] + 2 * [3] + [4]
        self.played_glyphs = []
        self.played_prodigy = None
        self.prodigies = []
        self.hp = 10
        self.has_regard = False
        self.winner = False
        self.id = -1
        
        glyph = 5 if order == 0 else 4
        self.hand = self.hand + [glyph]
        random.shuffle(self.hand)


    def choose_prodigy(self):
        index = random.randint(0,len(self.prodigies)-1)
        self.played_prodigy = self.prodigies[index]
        del self.prodigies[index]
        if settings.VERBOSE:
            print("Player " + str(self.id) + " joue " + self.played_prodigy.name)

    def get_random_glyphe_index(self, feinte_allowed = True):
        h = self.hand
        if feinte_allowed:
            return random.randint(0,len(h)-1)
        else :
            for i in range(len(h)-1):
                if h[i] != 0:
                    return i
        return -1

    def get_choosen_glyphs(self):
        #TODO faire en sorte que la somme des choix soit proche de P
        p = self.played_prodigy.get_p()
        sum_g = 0
        g = []
        l = len(self.hand)
        
        # On complète la main avec des Glyphes non Feinte
        for i in range(l):
            if sum_g + self.hand[l-i-1] <= p and self.hand[l-i-1] != 0 :
                g = g + [self.hand[l-i-1]]
                sum_g = sum_g + self.hand[l-i-1]
                del self.hand[l-i-1]
            # Dans 80% des cas, le dernier Glyphe sera une feinte
            if len(g) == 3 and random.random() > .2 or len(g) == 4:
                break
        
        # Quand on peut plus, on complète ce qui manque avec des Feintes
        for i in range(4-len(g)):
            index = self.hand.index(0)
            g = g + [self.hand[index]]
            del self.hand[index]

        # On mélange les Glyphs joués pour que les Feintes bougent
        random.shuffle(g)

        # On met le max sur la Maîtrise
        index_g = g.index(max(g))
        index_m = self.get_index_maitrise()
        tmp = g[index_g]
        g[index_g] = g[index_m]
        g[index_m] = tmp

        self.played_glyphs = g

    def get_index_maitrise(self):
        elements = ['anar', 'sulimo', 'ulmo', 'wilwar']
        return(elements.index(self.played_prodigy.element))
