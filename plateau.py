"""Module Plateau

Classes:
    * Plateau - Classe principale du plateau de jeu Quixo.
    * QuixoError - Classe d'erreur pour le jeu Quixo.
Functions:
    * make_data_line - Creates a data line.
    * make_sep_line - Creates a seperation line.
    * pos_error_check - Checks if X Y CORDS PROVIDED ARE CORRECT OR NOT.
"""

from copy import deepcopy

from quixo_error import QuixoError


class Plateau:
    """
    Représente le plateau de jeu Quixo.
    """

    def __init__(self, plateau=None):
        """Constructeur de la classe Plateau

        Vous ne devez rien modifier dans cette méthode.

        Args:
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        plateau = plateau.plateau if isinstance(plateau, Plateau) else plateau
        self.plateau = self.générer_le_plateau(deepcopy(plateau))

    def état_plateau(self):
        """Retourne une copie du plateau

        Retourne une copie du plateau pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            list[list[str]]: La représentation du plateau
            tel que retourné par le serveur de jeu.
        """
        return deepcopy(self.plateau)

    def __str__(self):
        """Retourne une représentation en chaîne de caractères du plateau

        Déplacer le code de votre fonction formater_plateau ici et ajuster le en conséquence.

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        ch = "   " + '-' * 19 + '\n'
        for i in range(5):
            ch += str(i+1)+" "+make_data_line(self.plateau[i])+'\n'
            if i != 4:
                ch += "  "+make_sep_line()+'\n'
            else:
                ch += "--"+make_sep_line()+'\n'
        ch += "  | 1   2   3   4   5 |\n"
        return ch

    def __getitem__(self, position):
        """Retourne la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le plateau.

        Returns:
            str: La valeur à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
        """
        if isinstance(position, int):
            print(position)

        pos_error_check(position)
        return self.plateau[position[1]-1][position[0]-1]

    def __setitem__(self, position, valeur):
        """Modifie la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le plateau.
            value (str): La valeur à insérer à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
            QuixoError: Valeur du cube invalide.
        """
        if valeur not in ['X', 'O', ' ']:
            raise QuixoError("Valur du cube invalide")
        pos_error_check(position)
        self.plateau[position[1] - 1][position[0] - 1] = valeur

    def générer_le_plateau(self, plateau):
        """Génère un plateau de jeu

        Si un plateau est fourni, il est retourné tel quel.
        Sinon, si la valeur est None, un plateau vide de 5x5 est retourné.

        Args:
            plateau (list[list[str]] | None): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None.

        Returns:
            list[list[str]]: La représentation du plateau
                tel que retourné par le serveur de jeu.

        Raises:
            QuixoError: Format du plateau invalide.
            QuixoError: Valeur du cube invalide.
        """
        if plateau is None:
            return [[' ' for _ in range(5)] for _ in range(5)]

        if (len(plateau) != 5 or
                not all(len(line) == 5 for line in plateau)):
            raise QuixoError("Format du plateau invalide.")

        for line in plateau:
            if any(cube not in ['X', 'O', ' '] for cube in line):
                raise QuixoError("Valeur du cube invalide.")
        return plateau

    def insérer_un_cube(self, cube, origine, direction):
        """Insère un cube dans le plateau

        Cette méthode appelle la méthode d'insertion appropriée selon la direction donnée.

        À noter que la validation des positions sont faites dans
        les méthodes __setitem__ et __getitem__. Vous devez donc en faire usage dans
        les diverses méthodes d'insertion pour vous assurez que les positions sont valides.

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
            direction (str): La direction de l'insertion, soit "haut", "bas", "gauche" ou "droite".

        Raises:
            QuixoError: La direction doit être "haut", "bas", "gauche" ou "droite".
            QuixoError: Le cube à insérer ne peut pas être vide.
        """
        if direction not in ("haut", "bas", "gauche", "droite"):
            raise QuixoError(
                "La direction doit être \"haut\", \"bas\", \"gauche\" ou \"droite\".")
        if cube == ' ':
            raise QuixoError("Le cube à insérer ne peut pas être vide.")
        if direction == "haut":
            self.insérer_par_le_haut(cube, origine)
        elif direction == "bas":
            self.insérer_par_le_bas(cube, origine)
        elif direction == "gauche":
            self.insérer_par_la_gauche(cube, origine)
        else:
            self.insérer_par_la_droite(cube, origine)

    def insérer_par_le_bas(self, cube, origine):
        """Insère un cube dans le plateau en direction du bas

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
        """
        self.insérer_direction(cube, origine, (0, -1))

    def insérer_par_le_haut(self, cube, origine):
        """Insère un cube dans le plateau en direction du haut

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
        """
        self.insérer_direction(cube, origine, (0, 1))

    def insérer_par_la_gauche(self, cube, origine):
        """Insère un cube dans le plateau en direction de la gauche

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
        """
        self.insérer_direction(cube, origine, (-1, 0))

    def insérer_par_la_droite(self, cube, origine):
        """Insère un cube dans le plateau en direction de la droite

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
        """
        self.insérer_direction(cube, origine, (1, 0))

    def insérer_direction(self, cube, origine, direction):
        """
        Insère un cube dans une direction spécifique à partir d'une position donnée
        sur le plateau.

        Args :
            - cube (str) : Le symbole du cube à insérer ('X' ou 'O').
            - origine (tuple) : La position de départ du cube sous forme de tuple (x, y)
              dans le plateau.
            - direction (tuple) : La direction dans laquelle déplacer le cube, sous forme
              de tuple (dx, dy),
            où dx et dy sont les changements respectifs sur les axes x et y.

        Raises :
            - QuixoError : Soulevée si le cube ne peut pas être inséré dans la direction
              donnée,
            par exemple si le mouvement dépasse les limites du plateau.
        """
        # vérification origine
        if not (origine[0] in [1, 5] or origine[1] in [1, 5]):
            raise QuixoError(
                'Le cube ne peut pas être inséré dans cette direction.')

        direction = (direction[0], direction[1]*-1)

        # vérification direction
        if not (1 <= origine[0] + direction[0] <= 5 and
                1 <= origine[1] + direction[1] <= 5):
            raise QuixoError(
                'Le cube ne peut pas être inséré dans cette direction.')

        dircoo = direction[0] if direction[0] != 0 else direction[1]
        coo = origine[0] if direction[0] != 0 else origine[1]
        itts = coo-1 if dircoo < 0 else 5-coo
        for i in range(itts):
            current = (origine[0] + direction[0]*i,
                       origine[1] + direction[1]*i)
            nextt = (origine[0] + direction[0]*(i+1),
                     origine[1] + direction[1]*(i+1))
            self[current] = self[nextt]
        current = (origine[0] + direction[0]*(itts),
                   origine[1] + direction[1]*(itts))
        self[current] = cube


def make_data_line(values):
    """Creates a data line for the function formater_le_damier.

    Args:
        values (list): A list of characters Either O, X or whitespace.

    Returns:
        str: String representing one line of the Data.
    """

    # initialiser une variable d'accumulation pour la ligne
    res = '|'

    # si aucune valeur, retourner une chaîne vide
    if len(values) == 0:
        return res

    # pour chaque valeur
    for x in values:
        # s'assurer que la valeur est sous la forme d'une chaîne
        if not isinstance(x, str):
            raise TypeError()

        # s'assurer que la chaîne est de longueur unitaire
        if len(x) != 1:
            raise ValueError()

        # ajouter la valeur courante
        res += f' {x} |'
    return res


def make_sep_line():
    """Creates a seperation line for the function formater_le_damier.

    Args:

    Returns:
        str: String representing one seperation line.
    """
    res = "|"
    res += "---|" * 5
    return res


def pos_error_check(position):
    """Checks if X Y CORDS PROVIDED ARE CORRECT OR NOT.

    Args:
        position (tuple): (x, y).

    Raises:
        QuixoError: Les Positions x et y doivent être entre 1 et 5 inclusivement.
    """
    if position[0] not in range(1, 6) or position[1] not in range(1, 6):
        raise QuixoError(
            f"{position} Les Positions x et y doivent être entre 1 et 5 inclusivement.")
