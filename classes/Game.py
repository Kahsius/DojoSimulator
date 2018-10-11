import random
import json
import pdb
from pdb import set_trace
from classes.Player import Player
from classes.Card import Card
from classes.Log import Log
from classes.Voie import Voie

import classes.Debug as debug
DEBUG_PRODIGES = ['Aurore']


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

        # Définition des opposants
        for i in range(2):
            self.players[i].opp = self.players[(i+1)%2]

        # Generate Prodigies for each player
        with open('data.json') as json_data:
            d = json.load(json_data)
            selected = [d[i] for i in random.sample(range(len(d)), 8)]

            # Pour debugger des persos en particulier
            for i in range(len(DEBUG_PRODIGES)):
                selected[i] = d[debug.get_id_prodigy(DEBUG_PRODIGES[i])]

            self.players[0].prodigies = selected[0:4]
            self.players[1].prodigies = selected[4:8]
            for i in range(4):
                self.players[0].prodigies[i] = Card(
                    self.players[0].prodigies[i], owner=self.players[0])
                self.players[1].prodigies[i] = Card(
                    self.players[1].prodigies[i], owner=self.players[1])

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
            #TODO priorité des stop talents et maitrise
            for p in self.players:
                p.played_prodigy.talent.execute_capacity()

            # Choix des Glyphes
            for p in self.players:
                p.get_choosen_glyphs()

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
            set_trace()
            winner = self.get_winner()
            if winner < 2:
                self.log.values['winners'].append(
                    self.players[winner].played_prodigy.name)
            self.players[winner % 2].winner = True
            self.players[(
                winner + 1) % 2].winner = False if winner != 2 else True

            #TODO Debug à partir d'ici @p :0
            # Application des Talents éventuels
            for p in self.players:
                if p.played_prodigy.talent.need_winner:
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
                        # S'il peut activer sa maîtrise
                        if v.element == p.played_prodigy.element:
                            p.played_prodigy.mastery.execute_capacity()
                        # Sinon
                        else:
                            v.capacity.owner = p
                            v.capacity.execute_capacity()

            # Dégâts du ou des gagnant
            p1, p2 = self.players
            if p1.winner:
                p2.hp = p2.hp - p1.played_prodigy.get_d()
            if p2.winner:
                p1.hp = p1.hp - p2.played_prodigy.get_d()

            self.clean_round(winner)

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
            p.played_glyphs = []
            p.played_prodigy = None

        # Si le second joueur a gagné ou s'il y a égalité
        if winner in [1, 2]:
            p1, p2 = self.players
            self.players = [p2, p1]
            p2.order = 0
            p1.order = 1

    def get_winner(self):
        winner = sum(self.score_voies)
        p1, p2 = self.players

        # Qui a gagné le plus de Voies
        if winner < 0:
            return(0)
        elif winner > 0:
            return(1)
        else:
            # Est-ce qu'un joueur a l'avantage
            if p1.played_prodigy.advantaged:
                return(0)
            elif p2.played_prodigy.advantaged:
                return(1)
            else:
                # Est-ce qu'un joueur a moins de pv que son opp
                if p1.hp < p2.hp:
                    return(0)
                elif p1.hp > p2.hp:
                    return(1)
                else:
                    # Si jamais il y a une parfaite égalité
                    return(2)

    def generate_voies(self):
        with open('voies.json') as json_data:
            d = json.load(json_data)
            for i in range(len(d)):
                self.voies = self.voies + [Voie(d[i])]
