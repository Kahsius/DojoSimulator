import random
import json
import pdb

class Game:
    def __init__(self):
        self.players = []
        self.score_voies = []
        self.voies = []
        self.round = 0

        for i in range(2):
            self.players.append(Player(i))

        # Generate Prodigies for each player
        with open('../data.json') as json_data:
            d = json.load(json_data)
            selected = d[random.sample(range(len(d), 8))]
            self.players[0].prodigies = selected[0:4]
            self.players[1].prodigies = selected[4:8]
            for i in range(4):
                self.players[0].prodigies[i] = Card(self.players[0].prodigies[i])
                self.players[1].prodigies[i] = Card(self.players[1].prodigies[i])

        # Génère les voies
        self.generate_voies()


    def run(self):
        while self.round_can_start() :

            # Choix des Prodiges
            for p in self.players:
                p.choose_prodigy()

            # Application des Talents
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
            winner = self.get_winner()
            self.players[winner%2].winner = True
            self.players[(winner+1)%2].winner = False if winner != 2 else True

            # Application des Talents éventuels
            for p in players:
                if p.played_prodigy.talent.need_winner:
                    p.played_prodigy.talent.execute_capacity()

            # Application des effets des Voies
            for i in range(2):
                p = self.players[i]
                # On étudie toutes les voies
                for j in range(4)
                    v = self.voies[j]
                    # Un des joueurs a remporté la voie
                    p1_win = self.score_voies[j] < 0 and i = 0
                    p2_win = self.score_voies[j] > 0 and i = 1
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

            self.clean_round()

        #TODO finir la partie



    def round_can_start(self):
    #TODO round_can_start

    def clean_round(self):
    #TODO clean_round

    def get_winner(self):
        winner = sum(self.score_voies)

        # Qui a gagné le plus de Voies
        if winner < 0:
            winner = 0
        elif winner > 0:
            winner = 1
        else:
            # Est-ce qu'un joueur a l'avantage
            if p1.played_prodigy.advantaged:
                winner = 0
            elif p2.played_prodigy.advantaged:
                winner = 1
            else:
                # Est-ce qu'un joueur a moins de pv que son opp
                if p1.hp < p2.hp:
                    winner = 0
                elif p1.hp > p2.hp:
                    winner = 1
                else:
                    # Si jamais il y a une parfaite égalité
                    winner = 2

    def generate_voies(self):
        with open('../voies.json') as json_data:
            d = json.load(json_data)
            for i in range(len(d)):
                self.voies = self.voies + [Voie(d[i])]
