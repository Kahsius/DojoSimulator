import Debug as debug
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
        self.prodigies_order = []
        self.hp = 10
        self.has_regard = False
        self.winner = False
        self.id = -1
        self.defense = False
        
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


    def get_random_glyphe_index(self, feinte_allowed = True, is_max = False):
        h = self.hand
        if feinte_allowed:
            return random.randint(0,len(h)-1)
        elif is_max:
            maxi = max(self.hand)
            return self.hand.index(maxi)
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
            index = index_m if random.random() > settings.P_COUNTER_OPP_MASTERY else index_m_opp
            g[index], g[index_g] = g[index_g], g[index]

        self.played_glyphs = g


    def get_index_maitrise(self):
        elements = ['anar', 'sulimo', 'ulmo', 'wilwar']
        return(elements.index(self.played_prodigy.element))

    def get_defense_glyphs(self):
        p = self
        if self.has_regard:
            if self.hand[0] == 0:
                max_glyph = min(max(p.hand), p.played_prodigy.get_p())
                range_list = list(range(max_glyph+1))
                range_list.reverse()
                for j in range_list:
                    if j in p.hand:
                        index = p.hand.index(j)
                        break
        else:
            max_glyph = min(max(p.hand), p.played_prodigy.get_p())
            range_list = list(range(max_glyph+1))
            range_list.reverse()
            for j in range_list:
                if j in p.hand:
                    index = p.hand.index(j)
                    self.played_glyphs += [j]
                    del self.hand[index]
                    break
        for _ in range(4-len(self.played_glyphs)):
            index_feinte = self.hand.index(0)
            self.played_glyphs += [0]
            del self.hand[index_feinte]

        index_glyph = self.played_glyphs.index(max(self.played_glyphs))
        index_maitrise = self.get_index_maitrise()
        tmp = self.played_glyphs[index_maitrise]
        self.played_glyphs[index_maitrise] = self.played_glyphs[index_glyph]
        self.played_glyphs[index_glyph] = tmp

