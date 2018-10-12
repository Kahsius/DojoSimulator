import settings
import random
import json
import pdb
from pdb import set_trace
from classes.Player import Player
from classes.Card import Card
from classes.Log import Log
from classes.Voie import Voie

import classes.Debug as debug


class Game:
    def __init__(self):
        self.players = []
        self.score_voies = []
        self.voies = []
        self.round = 0
        self.log = Log()

        # Creation des joueurs
        for i in range(2):
            self.players.append(Player(i))
            self.players[i].order = i
            self.players[i].id = i

        # Définition des opposants
        for i in range(2):
            self.players[i].opp = self.players[(i + 1) % 2]

        # Generate Prodigies for each player
        with open('data.json') as json_data:
            d = json.load(json_data)
            selected = [d[i] for i in random.sample(range(len(d)), 8)]

            # Pour debugger des persos en particulier
            for i in range(len(settings.DEBUG_PRODIGES)):
                selected[i] = d[debug.get_id_prodigy(settings.DEBUG_PRODIGES[i])]

            self.players[0].prodigies = selected[0:4]
            self.players[1].prodigies = selected[4:8]
            for i in range(4):
                self.players[0].prodigies[i] = Card(
                    self.players[0].prodigies[i], owner=self.players[0])
                self.players[1].prodigies[i] = Card(
                    self.players[1].prodigies[i], owner=self.players[1])

            if settings.VERBOSE:
                for p in self.players:
                    for i in range(4):
                        print("P" + str(p.id) + " a " + p.prodigies[i].name)
                    print('-'*30)
                

        # Génère les voies
        self.generate_voies()

    def run(self):
        while self.round_can_start():

            # Choix des Prodiges
            self.log.values['duels'].append([])
            for p in self.players:
                p.choose_prodigy()
                dim = len(self.log.values['duels'])
                self.log.values['duels'][dim - 1].append(p.played_prodigy.name)

            # Application des Talents
            for p in self.players:
                if p.played_prodigy.talent.priority:
                    print(p.played_prodigy.name + "_" + str(p.id) + " utilise Talent")
                    p.played_prodigy.talent.execute_capacity()

            for p in self.players:
                t = p.played_prodigy.talent
                if not t.priority and not t.need_winner:
                    print(p.played_prodigy.name + "_" + str(p.id) + " utilise Talent")
                    p.played_prodigy.talent.execute_capacity()

            # Choix des Glyphes
            #TODO prendre en compte le regard
            for p in self.players:
                p.get_choosen_glyphs()
                print(p.played_prodigy.name + "_" + str(p.id) + " joue " + str(p.played_glyphs))

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
                    print(p.played_prodigy.name + "_" + str(p.id) + " utilise Talent")
                    p.played_prodigy.talent.execute_capacity()

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
                        print(p.played_prodigy.name + "_" + str(p.id) + " remporte " + v.element)
                        # S'il peut activer sa maîtrise
                        if v.element == p.played_prodigy.element:
                            print("\tet applique sa Maitrise")
                            p.played_prodigy.mastery.execute_capacity()
                        # Sinon
                        else:
                            print("\tet applique son effet")
                            v.capacity.owner = p
                            v.capacity.execute_capacity()

            # Dégâts du ou des gagnant
            p1, p2 = self.players
            if p1.winner:
                print(p1.played_prodigy.name + "_" + str(p1.id) + " inflige " + str(p1.played_prodigy.get_d()))
                p2.hp = p2.hp - p1.played_prodigy.get_d()
            if p2.winner:
                print(p2.played_prodigy.name + "_" + str(p2.id) + " inflige " + str(p2.played_prodigy.get_d()))
                p1.hp = p1.hp - p2.played_prodigy.get_d()

            self.clean_round()
            print("P"+ str(p1.id) + " : " + str(p1.hp) + " hp - " + str(len(p1.hand)) + " glyphs")
            print("P"+ str(p2.id) + " : " + str(p2.hp) + " hp - " + str(len(p2.hand)) + " glyphs")
            print('-'*30)

        p1, p2 = self.players
        if p1.hp > p2.hp:
            self.log.values['winner'] = p1.id
        elif p1.hp < p2.hp:
            self.log.values['winner'] = p2.id
        self.log.values['hp'] = [p1.hp, p2.hp]
        set_trace()
        return (self.log)

    def round_can_start(self):
        # S'il y a un KO
        for p in self.players:
            if p.hp <= 0:
                self.log.values['ko'] = True
                return False

        # Si les 4 Prodiges ont été joués
        if not len(self.players[0].prodigies):
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

        # Si le second joueur a gagné ou s'il y a égalité
        if self.players[1].winner:
            p1, p2 = self.players
            self.players = [p2, p1]
            p2.order = 0
            p1.order = 1

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
        with open('voies.json') as json_data:
            d = json.load(json_data)
            for i in range(len(d)):
                self.voies = self.voies + [Voie(d[i])]
