"""
Ce module implémente une intelligence artificielle (IA) pour le jeu Quixo.

Classes:
- QuixoIA: Une sous-classe de Quixo qui permet de calculer les coups possibles,
  d'analyser le plateau, et de jouer de manière autonome.

Fonctionnalités principales:
- Lister les coups possibles pour un symbole donné ('X' ou 'O').
- Analyser le plateau pour déterminer les séquences de symboles alignés.
- Identifier les coups gagnants ou bloquants pour un joueur.
- Jouer un coup optimal ou aléatoire en fonction de l'état du jeu.
- Déterminer si la partie est terminée.

Exceptions:
- QuixoError: Soulevée lorsque des conditions invalides sont rencontrées,
  comme un symbole de cube incorrect ou une tentative de jeu après la fin de la partie.
"""

import random
from plateau import Plateau
from quixo import Quixo, directions_valides
from quixo_error import QuixoError


class QuixoIA(Quixo):
    '''
    Classe qui hérite de Quixo qui peut jouer de facon autonome 
    '''

    def lister_les_coups_possibles(self, plateau, cube):
        """
        Liste tous les coups possibles pour un joueur donné sur un plateau.

        Args:
            plateau (Plateau): L'état actuel du plateau de jeu.
            cube (str): Le symbole du joueur ('X' ou 'O').

        Returns:
            list: Une liste de dictionnaires représentant les coups possibles.
                  Chaque dictionnaire contient :
                  - "origine" (list): Les coordonnées du cube à déplacer.
                  - "direction" (str): La direction du déplacement (haut, bas, gauche, droite).

        Raises:
            QuixoError: Si le symbole du cube est invalide ou si la partie est déjà terminée.
        """
        if cube not in ['X', 'O']:
            raise QuixoError("Symbole du cube est invalide")
        if self.partie_terminée():
            raise QuixoError("La partie est terminé")

        points = []

        for x_range in [range(1, 6), range(1, 6), [1]*3, [5]*3]:
            for x in x_range:
                points.append((x, 0))

        index = 0
        for y_range in [[1]*5, [5]*5, range(2, 5), range(2, 5)]:
            for y in y_range:
                points[index] = (points[index][0], y)
                index += 1

        coups = []
        # coins
        for p in points:
            if plateau[p[0], p[1]] in [cube, ' ']:
                for direction in directions_valides(p):
                    coups.append(
                        {
                            "origine": [p[0], p[1]],
                            "direction": direction
                        })
        return coups

    def analyser_le_plateau(self, plateau):
        """
        Analyse le plateau pour compter les séquences alignées de symboles.

        Args:
            plateau (Plateau): L'état actuel du plateau de jeu.

        Returns:
            dict: Un dictionnaire contenant les séquences alignées pour chaque symbole
                  ('X' et 'O'), classées par longueur (2, 3, 4, ou 5).
                  Exemple :
                  {
                      "X": {2: 1, 3: 0, 4: 2, 5: 0},
                      "O": {2: 0, 3: 1, 4: 0, 5: 1}
                  }
        """

        result = {
            "X": {2: 0, 3: 0, 4: 0, 5: 0},
            "O": {2: 0, 3: 0, 4: 0, 5: 0}
        }

        def add_count(xo, count):
            if count > 1:
                result[xo][count] += 1

        for xo in ['X', 'O']:
            # ligne
            for line in plateau.plateau:
                count = sum(1 for cube in line if cube == xo)
                add_count(xo, count)
            # colonne
            for i in range(1, 6):
                count = sum((1 for j in range(1, 6)
                             if plateau[i, j] == xo))
                add_count(xo, count)
            # diagonale
            diagonals = [
                [plateau[i, i] for i in range(1, 6)],  # Diagonale principale
                [plateau[i, 6-i] for i in range(1, 6)]  # Diagonale inversée
            ]
            for diagonal in diagonals:
                count = sum(1 for cube in diagonal if cube == xo)
                add_count(xo, count)
        return result

    def partie_terminée(self):
        """
        Vérifie si la partie est terminée.

        Returns:
            str: Le symbole du joueur gagnant ('X' ou 'O') si un joueur a gagné.
            None: Si la partie n'est pas encore terminée.
        """
        score = self.analyser_le_plateau(self.plateau)
        for xo, counts in score.items():
            if counts[5] > 0:
                return xo
        return None

    def trouver_un_coup_vainqueur(self, xo):
        """
        Trouve un coup qui permettrait de gagner immédiatement.

        Args:
            xo (str): Le symbole du joueur ('X' ou 'O').

        Returns:
            dict: Un dictionnaire représentant le coup gagnant avec :
                  - "origine" (list): Les coordonnées du cube à déplacer.
                  - "direction" (str): La direction du déplacement.
            None: Si aucun coup gagnant n'est possible.
        """

        source = Plateau(self.plateau)
        for coup in self.lister_les_coups_possibles(self.plateau, xo):
            plateau = Plateau(source)
            plateau.insérer_un_cube(xo, coup['origine'], coup['direction'])
            score = self.analyser_le_plateau(plateau)
            if score[xo][5] > 0:
                return [coup['origine'], coup['direction']]

        return None

    def trouver_un_coup_bloquant(self, xo):
        """
        Trouve un coup pour bloquer un coup gagnant de l'adversaire.

        Args:
            xo (str): Le symbole du joueur ('X' ou 'O').

        Returns:
            dict: Un dictionnaire représentant le coup bloquant avec :
                  - "origine" (list): Les coordonnées du cube à déplacer.
                  - "direction" (str): La direction du déplacement.
            None: Si aucun coup bloquant n'est trouvé.
        """
        xo_adverse = 'X' if xo == 'O' else 'O'
        return self.trouver_un_coup_vainqueur(xo_adverse)

    def jouer_un_coup(self, xo):
        """
        Joue un coup pour le joueur en utilisant une stratégie optimale.

        Args:
            xo (str): Le symbole du joueur ('X' ou 'O').

        Returns:
            dict: Un dictionnaire représentant le coup joué avec :
                  - "origine" (list): Les coordonnées du cube déplacé.
                  - "direction" (str): La direction du déplacement.
        """
        coup = self.trouver_un_coup_vainqueur(xo)
        if coup is None:
            coup = self.trouver_un_coup_bloquant(xo)
            if coup is None:
                coups = self.lister_les_coups_possibles(self.plateau, xo)
                rand_coup = coups[random.randint(0, len(coups)-1)]
                coup = [rand_coup['origine'], rand_coup['direction']]
        self.plateau.insérer_un_cube(xo, coup[0], coup[1])
        return coup
