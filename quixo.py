"""Module Quixo

Classes:
    * Quixo - Classe principale du jeu Quixo.
    * Plateau - Classe de gestion du plateau
    * argparse - Classe argparse

Functions:
    * interpréter_la_commande - Génère un interpréteur de commande.
    * formater_entête - Formater la représentation graphique de la légende.
"""

import argparse
from plateau import Plateau
from quixo_error import QuixoError


class Quixo:
    """Main Game Class

    Attributs:
        * joueurs : players
        * plateau : game board
    Methods :
    ...

    """

    def __init__(self, joueurs, plateau=None) -> None:
        """Constructeur de la classe Quixo

        Vous ne devez rien modifier dans cette méthode.

        Args:
            joueurs (list[str]): La liste des deux joueurs.
                Le premier joueur possède le symbole "X" et le deuxième "O".
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.joueurs = joueurs
        self.plateau = Plateau(plateau)

    def état_partie(self):
        """Retourne une copie du jeu

        Retourne une copie du jeu pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            dict: La représentation du jeu tel que retourné par le serveur de jeu.
        """
        return {
            "joueurs": self.joueurs,
            "plateau": self.plateau.état_plateau(),
        }

    def __str__(self):
        """Retourne une représentation en chaîne de caractères de la partie

        Déplacer le code de vos fonctions formater_légende et formater_jeu ici.
        Adaptez votre code en conséquence et faites appel à Plateau
        pour obtenir la représentation du plateau.

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        return formater_entête(self.état_partie()["joueurs"]) + '\n' + Plateau.__str__(self.plateau)

    def déplacer_pion(self, pion, origine, direction):
        """Déplacer un pion dans une direction donnée.

        Applique le changement au Plateau de jeu

        Args:
            pion (str): Le pion à déplacer, soit "X" ou "O".
            origine (list[int]): La position (x, y) du pion sur le plateau.
            direction (str): La direction du déplacement, soit "haut", "bas", "gauche" ou "droite".
        """
        self.plateau.insérer_un_cube(pion, origine, direction)

    def choisir_un_coup(self):
        """Demander le prochain coup à jouer au joueur.

        Déplacer le code de votre fonction récupérer_le_coup ici et ajuster le en conséquence.
        Vous devez maintenant valider les entrées de l'utilisateur.

        Returns:
            tuple: Tuple de 2 éléments composé de l'origine du bloc à déplacer et de sa direction.
                L'origine est une liste de 2 entiers [x, y].
                La direction est une chaîne de caractères.

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
            QuixoError: La direction doit être "haut", "bas", "gauche" ou "droite".

        Examples:
            Donnez la position d'origine du bloc (x,y) :
            Quelle direction voulez-vous insérer? ('haut', 'bas', 'gauche', 'droite') :
        """
        origine = [int(x) for x in input("Donnez la position d'origine du cube (x,y) : ").split(',')
                   ]
        direction = input(
            "Quelle direction voulez-vous insérer? ('haut', 'bas', 'gauche', 'droite') : "
        )

        if not (origine[0] in [1, 5] or origine[1] in [1, 5]):
            raise QuixoError(
                'Les positions x et y doivent être entre 1 et 5 inclusivement.')
        if direction not in ['haut', 'bas', 'gauche', 'droite']:
            raise QuixoError(
                'La direction doit être "haut", "bas", "gauche" ou "droite".')

        return (origine, direction)


def interpréter_la_commande():
    """Génère un interpréteur de commande.
    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
            Cet objet aura l'attribut «idul» représentant l'idul du joueur
            et l'attribut «parties» qui est un booléen True/False.
    """
    parser = argparse.ArgumentParser(
        description="Quixo"
    )
    parser.add_argument(
        "idul",
        help="IDUL du joueur"
    )
    parser.add_argument(
        "-a", "--autonome",
        action="store_true",
        help="Jouer de façon autonome"
    )

    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)

    return parser.parse_args()


def formater_entête(joueurs):
    """Formater la représentation graphique de la légende.

    Args:
        joueurs (list): Liste des joueurs.

    Returns:
        str: Chaîne de caractères représentant la légende.
    """
    return f"Légende:\n   X={joueurs[0]}\n   O={joueurs[1]}"


def directions_valides(origine):
    """
    Détermine les directions valides pour déplacer un cube à partir d'une position donnée.

    Args:
        origine (tuple): Les coordonnées (x, y) du cube d'origine.

    Returns:
        list: Une liste de directions valides ('haut', 'bas', 'gauche', 'droite').
    """
    directions = []
    if origine[0] < 5:
        directions.append("droite")
    if origine[0] > 1:
        directions.append("gauche")
    if origine[1] < 5:
        directions.append("bas")
    if origine[1] > 1:
        directions.append("haut")
    return directions
