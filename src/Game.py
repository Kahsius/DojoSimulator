import settings
import random
import json
import pdb
from pdb import set_trace
from Player import Player
from Card import Card
from Log import Log
from Voie import Voie

import Debug as debug


class Game:
    def __init__(self):
        self.players = []
        self.score_voies = []
        self.voies = []
        self.turn = 0
        self.log = Log()

        # Creation des joueurs
        for i in range(2):
            self.players.append(Player(i))
            self.players[i].order = i
            self.players[i].id = i
            self.players[i].hp = settings.BASE_HP

        # Définition des opposants
        for i in range(2):
            self.players[i].opp = self.players[(i + 1) % 2]

        # Generate Prodigies for each player
        with open('data/prodigies.json') as json_data:
            d = json.load(json_data)
            selected = [d[i] for i in random.sample(range(len(d)), 8)]

            # Pour debugger des persos en particulier
            for i in range(len(settings.DEBUG_PRODIGES)):
                selected[i] = d[debug.get_id_prodigy(settings.DEBUG_PRODIGES[i])]
                random.shuffle(selected)

            self.players[0].prodigies = selected[0:4]
            self.players[1].prodigies = selected[4:8]
            for i in range(4):
                self.players[0].prodigies[i] = Card(
                    self.players[0].prodigies[i], owner=self.players[0])
                self.players[1].prodigies[i] = Card(
                    self.players[1].prodigies[i], owner=self.players[1])

            for p in self.players:
                p.define_prodigies_order()
                for i in range(4):
                    debug.verbose("P" + str(p.id) + " a " + p.prodigies[i].name)
                debug.verbose('-'*30)
                

        # Génère les voies
        self.generate_voies()

    def run(self):
        while self.round_can_start():

            debug.verbose("Round : " + str(self.turn))

            # Choix des Prodiges
            self.log.values['duels'].append(['',''])
            for p in self.players:
                p.choose_prodigy(self.turn)
                dim = len(self.log.values['duels'])
                self.log.values['duels'][dim - 1][p.id] = p.played_prodigy.name

            # Application des Talents
            for p in self.players:
                if p.played_prodigy.talent.priority:
                    debug.verbose(p.played_prodigy.name + "_" + str(p.id) + " utilise Talent")
                    p.played_prodigy.talent.execute_capacity(self.turn)

            for p in self.players:
                t = p.played_prodigy.talent
                if not t.priority and not t.need_winner:
                    debug.verbose(p.played_prodigy.name + "_" + str(p.id) + " utilise Talent")
                    p.played_prodigy.talent.execute_capacity(self.turn)

            # Determine player play style
            for i in range(2):
                p = self.players[i]
                p.defense = (random.random() < settings.P_DEFENSE)
                self.log.values['defense'][p.id].append(p.defense)

            # Joue Glyphe en cas de Regard
            p1, p2 = self.players
            for i in range(2):
                p = self.players[i]
                if p.opp.has_regard:
                    if p.defense :
                        if p.opp.get_index_maitrise() == p.get_index_maitrise():
                            max_glyph = min(max(p.hand), 
                                    p.played_prodigy.get_p())
                            range_list = list(range(max_glyph+1))
                            range_list.reverse()
                            for j in range_list:
                                if j in p.hand:
                                    index = p.hand.index(j)
                                    break
                        else:
                            index = p.hand.index(0)
                    else:
                        index = p.get_random_glyphe_index()                        

                    debug.verbose("Regard: P" + str(p.id)+ " " + 
                            str(p.hand[index]) + " sur voie " + 
                            str(p.opp.get_index_maitrise()))
                    p.played_glyphs = p.played_glyphs + [p.hand[index]]
                    del p.hand[index]
                    # On fait en sorte que le joueur avec Regard joue forcément deuxième
                    p1 = p
                    p2 = self.players[(i+1)%2]
                    break

            # Choix des Glyphes
            for p in [p1, p2]:
                if p.defense :
                    p.get_defense_glyphs()
                else:
                    p.get_choosen_glyphs()
                for i in range(4):
                    if p.played_glyphs[i] > 0:
                        self.log.values['glyphs'][p.id][i] = self.log.values['glyphs'][p.id][i] + 1
                debug.verbose(p.played_prodigy.name + "_" + str(p.id) + " joue " + str(p.played_glyphs))

            # Résolution des Voies
            p1, p2 = self.players
            for i in range(4):
                if p1.played_glyphs[i] > p2.played_glyphs[i]:
                    winner = -1
                elif p1.played_glyphs[i] < p2.played_glyphs[i]:
                    winner = 1
                else:
                    if p1.played_prodigy.initiative:
                        winner = -1
                    elif p2.played_prodigy.initiative:
                        winner = -1
                    else:
                        winner = 0
                self.score_voies = self.score_voies + [winner]

            # Détermination du gagnant
            winner = self.get_winner()
            if winner < 2:
                self.log.values['winners_prodigies'].append(
                    self.players[winner].played_prodigy.name)
                self.log.values['winners_player'].append(
                    self.players[winner].id)
            self.players[winner % 2].winner = True
            self.players[(
                winner + 1) % 2].winner = False if winner != 2 else True

            # Application des Talents éventuels
            for p in self.players:
                if p.played_prodigy.talent.need_winner:
                    debug.verbose(p.played_prodigy.name + "_" + str(p.id) + " utilise Talent")
                    p.played_prodigy.talent.execute_capacity(self.turn)

            # Application des effets des Voies
            for i in range(2):
                p = self.players[i]
                # On étudie toutes les voies
                for j in range(4):
                    v = self.voies[j]
                    # Un des joueurs a remporté la voie
                    p1_win = self.score_voies[j] < 0 and i == 0
                    p2_win = self.score_voies[j] > 0 and i == 1
                    if p1_win or p2_win:
                        debug.verbose(p.played_prodigy.name + "_" + str(p.id) + " remporte " + v.element)
                        # S'il peut activer sa maîtrise
                        element_ok = v.element == p.played_prodigy.element
                        damage = p.played_prodigy.mastery.need_victory
                        damage_and_winner = p.winner and damage
                        not_stopped = not p.played_prodigy.mastery.stopped
                        if element_ok and (damage_and_winner or not damage) and not_stopped:
                            debug.verbose("\tet applique sa Maitrise")
                            p.played_prodigy.mastery.execute_capacity(self.turn)
                            self.log.values['mastery_activated'][p.id][self.turn] = True
                        # Sinon
                        else:
                            debug.verbose("\tet applique son effet")
                            v.capacity.owner = p
                            v.capacity.execute_capacity(self.turn)

            # Dégâts du ou des gagnant
            p1, p2 = self.players
            if p1.winner:
                debug.verbose(p1.played_prodigy.name + "_" + str(p1.id) + " inflige " + str(p1.played_prodigy.get_d()))
                p2.hp = p2.hp - p1.played_prodigy.get_d()
            if p2.winner:
                debug.verbose(p2.played_prodigy.name + "_" + str(p2.id) + " inflige " + str(p2.played_prodigy.get_d()))
                p1.hp = p1.hp - p2.played_prodigy.get_d()

            self.clean_round()
            debug.verbose("P"+ str(p1.id) + " : " + str(p1.hp) + " hp - " + str(p1.hand))
            debug.verbose("P"+ str(p2.id) + " : " + str(p2.hp) + " hp - " + str(p2.hand))
            debug.verbose('-'*30)

        # +1HP/Glyphe restant en main
        for p in self.players:
            for v in p.hand:
                p.hp = p.hp + v/max(v,1)

        p1, p2 = self.players
        if p1.hp > p2.hp:
            self.log.values['winner'] = p1.id
        elif p1.hp < p2.hp:
            self.log.values['winner'] = p2.id

        self.log.values['hp'] = [p1.hp, p2.hp]
        self.log.values['glyphs_winner'] = self.log.values['glyphs'][self.log.values['winner']]
        self.log.values['end_turn'] = self.turn

        return (self.log)

    def round_can_start(self):
        # S'il y a un KO
        for p in self.players:
            if p.hp <= 0:
                self.log.values['ko'] = True
                return False

        # Si les 4 Prodiges ont été joués
        if self.turn == 4:
            return False

        # Sinon
        return True

    def clean_round(self):
        # Nettoyage des joueurs
        for p in self.players:
            for i in range(len(p.played_glyphs)):
                if p.played_glyphs[i] == 0:
                    p.hand = p.hand + [0]
            p.played_glyphs = []
            p.played_prodigy = None
            p.defense = False

        # Si le second joueur a gagné ou s'il y a égalité
        if self.players[1].winner:
            p1, p2 = self.players
            self.players = [p2, p1]
            p2.order = 0
            p1.order = 1

        self.turn = self.turn + 1
        self.score_voies = []

    def get_winner(self):
        winner = sum(self.score_voies)
        p1, p2 = self.players

        # Qui a gagné le plus de Voies
        if winner < 0:
            return (0)
        elif winner > 0:
            return (1)
        else:
            # Est-ce qu'un joueur a l'avantage
            if p1.played_prodigy.advantaged:
                return (0)
            elif p2.played_prodigy.advantaged:
                return (1)
            else:
                # Est-ce qu'un joueur a moins de pv que son opp
                if p1.hp < p2.hp:
                    return (0)
                elif p1.hp > p2.hp:
                    return (1)
                else:
                    # Si jamais il y a une parfaite égalité
                    return (2)

    def generate_voies(self):
        with open('data/voies.json') as json_data:
            d = json.load(json_data)
            for i in range(len(d)):
                self.voies = self.voies + [Voie(d[i])]
