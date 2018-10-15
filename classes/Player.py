import classes.Debug as debug
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
            debug.verbose("Player " + str(self.id) + " joue " + self.played_prodigy.name)

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

        p = self.played_prodigy.get_p()
        # Prend en compte le cas où un Glyphe est déjà joué à cause du regard
        sum_g = sum(self.played_glyphs)
        g = self.played_glyphs
        # Récupère le glyphe éventuellement joué à cause du Regard
        g_regard = g[0] if self.opp.has_regard else -1
        
        if self.has_regard:
            g_opp = self.opp.played_glyphs[self.get_index_maitrise()]
            # Si a le glyphe juste au dessus sinon feinte
            g_maitrise = g_opp+1 if g_opp+1 in self.hand else 0
            g.append(g_maitrise)
            del self.hand[self.hand.index(g_maitrise)]
            sum_g = sum_g + g_maitrise

        # On complète la main avec des Glyphes non Feinte
        l = len(self.hand)
        for i in range(l):
            if sum_g + self.hand[l-i-1] <= p and self.hand[l-i-1] != 0 :
                g = g + [self.hand[l-i-1]]
                sum_g = sum_g + self.hand[l-i-1]
                del self.hand[l-i-1]
            # Dans 80% des cas, le dernier Glyphe sera une feinte
            if len(g) == 3 and random.random() > .2:
                break
        
        # Quand on peut plus, on complète ce qui manque avec des Feintes
        for i in range(4-len(g)):
            index = self.hand.index(0)
            g = g + [self.hand[index]]
            del self.hand[index]

        # On mélange les Glyphes joués pour que les Feintes bougent
        random.shuffle(g)

        # Regard appliqué par l'adversaire, donc max sur Maîtrise self
        if self.opp.has_regard:
            # On récupère les index qui faut
            index_elem_opp = self.opp.get_index_maitrise()
            index_g_regard = g.index(g_regard)
            # On cherche le max hors regard
            index_g = g.index(max(g[0:index_g_regard] + [-1] + g[index_g_regard+1:4]))
            index_m = self.get_index_maitrise()
            # On met le max de ce qui reste sur notre maîtrise
            g[index_g], g[index_m] = g[index_m], g[index_g]
            # On reprend l'index du regard au cas où
            index_g_regard = g.index(g_regard)
            # On met le glyphe de regard sur la bonne voie
            g[index_elem_opp], g[index_g_regard] = g[index_g_regard], g[index_elem_opp]
        # Si on a le regard, on met notre glyphe sur notre maitrise
        elif self.has_regard:
            index_g = g.index(g_maitrise)
            index_m = self.get_index_maitrise()
            g[index_g], g[index_m] = g[index_m], g[index_g]
            self.has_regard = False
        # Si personne n'a le regard
        else:
            index_g = g.index(max(g))
            index_m = self.get_index_maitrise()
            index_m_opp = self.opp.get_index_maitrise()
            index = index_m if random.random() < .5 else index_m_opp
            g[index], g[index_g] = g[index_g], g[index]

        self.played_glyphs = g

    def get_index_maitrise(self):
        elements = ['anar', 'sulimo', 'ulmo', 'wilwar']
        return(elements.index(self.played_prodigy.element))
