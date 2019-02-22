import Debug as debug
import settings
from pdb import set_trace
from copy import deepcopy
import random

class Player:
    def __init__(self, order):
        self.pseudo = "Default"
        self.hand = 4 * [0] + 3 * [1] + 3 * [2] + 2 * [3] + [4]
        self.played_glyphs = []
        self.played_prodigy = None
        self.prodigies = []
        self.prodigies_order = []
        self.hp = 10
        self.has_regard = False
        self.winner = False
        self.id = -1
        self.COMBINAISONS = {
            1: [[1]],
            2: [[2], [1, 1]],
            3: [[3], [2, 1], [1, 1, 1]],
            4: [[4], [3, 1], [2, 2], [2, 1, 1]],
            5: [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1]],
            6: [[5, 1], [4, 2], [3, 3], [4, 1, 1], [3, 2, 1], [2, 2, 2],
                [2, 2, 1, 1], [3, 1, 1, 1]],
            7: [[5, 2], [4, 3], [5, 1, 1], [4, 2, 1], [3, 3, 1], [3, 2, 2],
                [4, 1, 1, 1], [3, 2, 1, 1], [2, 2, 2, 1]],
            8: [[5, 3], [4, 4], [5, 2, 1], [4, 3, 1], [3, 3, 2], [4, 2, 2],
                [4, 2, 1, 1], [3, 3, 1, 1], [5, 1, 1, 1], [3, 2, 2, 1]],
            9: [[5, 4], [4, 4, 1], [4, 3, 2], [5, 2, 2], [5, 3, 1],
                [5, 2, 1, 1], [4, 3, 1, 1], [4, 2, 2, 1], [3, 2, 2, 2]]
        }
        for i in range(1, 10):
            random.shuffle(self.COMBINAISONS[i])

        glyph = 5 if order == 0 else 4
        self.hand = self.hand + [glyph]
        random.shuffle(self.hand)


    def define_prodigies_order(self):
        order = [-1]*4
        for turn in range(3,-1,-1):
            chosen = False
            for p in self.prodigies:
                index_p = self.prodigies.index(p)
                if turn in p.turn and not index_p in order:
                    order[turn] = self.prodigies.index(p)
                    chosen = True
                    break
            if not chosen:
                for p in self.prodigies:
                    index_p = self.prodigies.index(p)
                    if not index_p in order:
                        order[turn] = self.prodigies.index(p)
                        break
        self.prodigies_order = order


    def choose_prodigy(self, turn):
        # On récupère l'index
        index = self.prodigies_order[turn]
        self.played_prodigy = self.prodigies[index]
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
        length = len(g)
        diff = p - sum_g
        found = []
        ok = False
        for potential in reversed(range(1, diff+1)):
            for possibility in self.COMBINAISONS[potential]:
                if len(possibility) + length <= 4:
                    hand_copy = deepcopy(self.hand)
                    ok = True
                    for glyph in possibility:
                        if glyph in hand_copy:
                            hand_copy.remove(glyph)
                        else:
                            ok = False
                            break
                if ok:
                    found = possibility
                    break
            if ok:
                break

        for glyph in found:
            index = self.hand.index(glyph)
            g = g + [self.hand[index]]
            del self.hand[index]

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
            counter_opp_mastery = (random.random() > settings.P_COUNTER_OPP_MASTERY)
            index = index_m if counter_opp_mastery else index_m_opp
            g[index], g[index_g] = g[index_g], g[index]

        self.played_glyphs = g


    def get_index_maitrise(self):
        elements = ['anar', 'sulimo', 'ulmo', 'wilwar']
        return(elements.index(self.played_prodigy.element))
