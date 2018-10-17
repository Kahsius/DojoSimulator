import Debug as debug
import settings
from pdb import set_trace
from copy import deepcopy
from random import randint


class Capacity:
    def __init__(self, json, owner=None):
        methods = globals().copy()
        methods.update(locals())

        self.owner = owner
        self.target = None if not json.get('target') else json['target']
        self.condition = "none" if not json.get('condition') else json[
            'condition']
        self.need_winner = False
        if json.get('condition'):
            if json['condition'] in ['victoire', 'defaite']:
                self.need_winner = True
        self.modification = "none" if not json.get('modification') else json[
            'modification']
        self.turn = []
        if self.modification == 'patience':
            self.turn = [2,3]
        elif self.modification == 'acharnement':
            self.turn = [0,1]
        self.cost = False if not json.get('cost') else json['cost']
        self.cost_type = "none" if not json.get('cost_type') else json[
            'cost_type']
        self.cost_value = 0 if not json.get('cost_value') else json[
            'cost_value']
        self.effect = None if not json.get('effect') else methods.get(
            json['effect'])
        self.need_victory = True if json.get('effect') == "modif_damage" else False
        self.priority = False if json['effect'] != 'stop_talent' else True
        self.value = 0 if not json.get('value') else json['value']
        self.contrecoup = False if not json.get('contrecoup') else json[
            'contrecoup']
        self.stopped = False
        self.data = json

    def execute_capacity(self):
        if self.stopped:
            debug.verbose("\t(stoppée)")
        if self.check_condition(self.owner) and not self.stopped:
            if self.cost:
                if self.cost_type == "glyph":
                    index = self.owner.get_random_glyphe_index(feinte_allowed=False)
                    if index != -1:
                        del self.owner.hand[index]
                    else:
                        return
                elif self.cost_type == "hp":
                    self.owner.hp = self.owner.hp - self.cost_value
            self.set_target(self.owner)
            debug.verbose(self.get_string_effect())
            for i in range(self.get_modification(self.owner)):
                self.effect(self)

    def set_target(self, owner):
        # Target definition
        c = self.contrecoup
        t = self.target
        if t == "opp":
            self.target = owner if c else owner.opp
        elif t == "owner":
            self.target = owner.opp if c else owner

    def check_condition(self, owner):
        victoire = self.condition == "victoire" and owner.winner
        defaite = self.condition == "defaite" and not owner.winner
        courage = self.condition == "courage" and owner.order == 0
        riposte = self.condition == "riposte" and owner.order == 1
        none = self.condition == "none"
        if victoire or defaite or courage or riposte or none:
            return True
        else:
            return False

    def get_modification(self, owner):
        if self.modification == "patience":
            return 3 - len(owner.prodigies)
        elif self.modification == "acharnement":
            return len(owner.prodigies)
        elif self.modification == "par_glyphe":
            count = 0
            for glyph in owner.played_glyphs:
                if glyph == 0:
                    count = count + 1
            return count
        else:
            return 1

    def get_string_effect(self):
        string = "\t"
        d = self.data
        string = string if not d.get(
            'contrecoup') else string + "Contrecoup" + " "
        if d.get('cost'):
            string = string + str(d['cost_value']) + " " + d['cost_type'] + " "
        string = string if not d.get(
            'condition') else string + d['condition'] + " "
        string = string if not d.get(
            'modification') else string + d['modification'] + " "
        string = string +  d['effect'] + " "
        string = string if not d.get('value') else string + str(d['value'])
        return (string)


# -------------------------------------------------------------------


# Définition de tous les effets possibles
def recuperation(capa):
    v = capa.value
    t = capa.target
    l = len(t.played_glyphs) - 1
    count = 0
    debug.verbose("\tmain avant : " + str(t.hand))
    for i in range(l):
        if count == v:
            break
        index = l - i
        if t.played_glyphs[index] not in (0, 5):
            debug.verbose("\tglyph choisi : " + str(t.played_glyphs[index]))
            t.hand = t.hand + [t.played_glyphs[index]]
            del t.played_glyphs[index]
            count = count + 1
    debug.verbose("\tmain apres : " + str(t.hand))


def modif_damage(capa):
    p = capa.target.played_prodigy
    v = capa.value
    p.damage = p.damage if p.protected and v < 0 else p.damage + v


def modif_power(capa):
    p = capa.target.played_prodigy
    v = capa.value
    p.power = p.power if p.protected and v < 0 else p.power + v


def modif_power_damage(capa):
    modif_power(capa)
    modif_damage(capa)


def modif_hp(capa):
    p = capa.target
    debug.verbose("\tP" + str(capa.owner.id) + " avant: " + str(p.hp))
    p.hp = p.hp + capa.value
    debug.verbose("\tP" + str(capa.owner.id) + " apres: " + str(p.hp))


def stop_talent(capa):
    p = capa.target.played_prodigy
    if not p.protected:
        p.talent.stopped = True


def stop_mastery(capa):
    p = capa.target.played_prodigy
    if not p.protected:
        p.mastery.stopped = True


def protection(capa):
    capa.target.played_prodigy.protected = True


def echange_p(capa):
    p1 = capa.target.played_prodigy
    p2 = capa.target.opp.played_prodigy
    pp1 = p1.power_base
    p1.power_base = p2.power_base
    p2.power_base = pp1


def echange_d(capa):
    p1 = capa.target.played_prodigy
    p2 = capa.target.opp.played_prodigy
    dp1 = p1.damage_base
    p1.damage_base = p2.damage_base
    p2.damage_base = dp1


def copy_talent(capa):
    p1 = capa.target.played_prodigy
    p2 = capa.target.opp.played_prodigy
    p2.talent = deepcopy(p1.talent)


def copy_mastery(capa):
    p1 = capa.target.played_prodigy
    p2 = capa.target.opp.played_prodigy
    p2.mastery = deepcopy(p1.mastery)


def oppression(capa):
    v = capa.value
    t = capa.target
    l = len(t.hand)
    count = 0
    for i in range(l):
        if count == v:
            break
        index = l - i - 1
        if t.hand[index] != 0:
            del t.hand[index]
            count = count + 1


def pillage(capa):
    v = capa.value
    t = capa.target
    l = len(t.hand)
    count = 0
    for i in range(l):
        if count == v:
            break
        index = l - i - 1
        if t.hand[index] != 0:
            t.opp.hand = t.opp.hand + [t.hand[index]]
            del t.hand[index]
            count = count + 1


def initiative(capa):
    capa.target.played_prodigy.initiative = True


def avantage(capa):
    capa.target.played_prodigy.advantaged = True


def vampirism(capa):
    v = capa.value
    t = capa.target
    t.hp = t.hp - v
    t.opp.hp = t.opp.hp + v


def regard(capa):
    capa.target.has_regard = True


def nothing(capa):
    pass
