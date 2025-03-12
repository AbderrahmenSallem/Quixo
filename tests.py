"""Tests Quixo

Classes:
    * Quixo - Classe principale du jeu Quixo.
    * Plateau - Classe de gestion du plateau

Functions:
    * test_formater_le_damier_pour_une_nouvelle_partie - test le formattage du damier.
    * test_formater_le_jeu_pour_une_nouvelle_partie - test le formattage du partie.
    * test_formater_le_jeu_pour_une_partie_avancée - test le formattage du partie avancée.

Ce module contient des tests unitaires pour le projet Quixo.
"""

from plateau import Plateau
from quixo import Quixo
from quixo_error import QuixoError
from quixo_ia import QuixoIA


def test_formater_le_damier_pour_une_nouvelle_partie():
    """test le formattage du damier.
    """
    plateau = Plateau()

    attendu = (
        "   -------------------\n"
        "1 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "2 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "3 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "4 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "5 |   |   |   |   |   |\n"
        "--|---|---|---|---|---|\n"
        "  | 1   2   3   4   5 |\n"
    )

    résultat = str(plateau)
    assert résultat == attendu, "Échec du test de formater damier pour une nouvelle partie"


def test_formater_le_jeu_pour_une_nouvelle_partie():
    """test le formattage du partie.
    """
    joueurs = ["josmi42", "automate"]

    quixo = Quixo(joueurs)

    attendu = (
        "Légende:\n"
        "   X=josmi42\n"
        "   O=automate\n"
        "   -------------------\n"
        "1 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "2 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "3 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "4 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "5 |   |   |   |   |   |\n"
        "--|---|---|---|---|---|\n"
        "  | 1   2   3   4   5 |\n"
    )

    résultat = str(quixo)

    assert résultat == attendu, "Échec du test de formater le jeu pour une nouvelle partie"


def test_formater_le_jeu_pour_une_partie_avancée():
    """test le formattage du partie avancée.
    """
    joueurs = ["josmi42", "automate"]
    plateau = [
        [" ", " ", "X", " ", " "],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "O"],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " "],
    ]

    quixo = Quixo(joueurs, plateau)

    attendu = (
        "Légende:\n"
        "   X=josmi42\n"
        "   O=automate\n"
        "   -------------------\n"
        "1 |   |   | X |   |   |\n"
        "  |---|---|---|---|---|\n"
        "2 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "3 |   |   |   |   | O |\n"
        "  |---|---|---|---|---|\n"
        "4 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "5 |   |   |   |   |   |\n"
        "--|---|---|---|---|---|\n"
        "  | 1   2   3   4   5 |\n"
    )

    résultat = str(quixo)

    assert résultat == attendu, "Échec du test de formater le jeu pour une partie avancée"


def tester_plateau():
    '''
    test Plateau
    '''
    echec_msg = "Échec du test custom plateau"

    # __getitem__
    plateau = Plateau()
    x = [1, 5]
    y = [5, 1]
    for i, _ in enumerate(x):
        plateau.plateau[y[i]-1][x[i]-1] = 'X'
        assert plateau[x[i], y[i]] == 'X', echec_msg

    x, y = 2, 3
    plateau.plateau[y-1][x-1] = 'X'
    assert plateau[x, y] == 'X', echec_msg

    # __setitem__
    x, y = 1, 2
    plateau[x, y] = 'X'
    assert plateau.plateau[y-1][x-1] == 'X', echec_msg

    x, y = 2, 3
    plateau[x, y] = 'X'
    assert plateau.plateau[y-1][x-1] == 'X', echec_msg

    # insérer_une_cube
    plateau.insérer_un_cube('X', [1, 5], 'haut')
    plateau.insérer_un_cube('X', [1, 1], 'bas')
    plateau.insérer_un_cube('X', [5, 1], 'gauche')

    x, y = 1, 2
    entré_plateau = [[' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ']]
    plateau = Plateau(entré_plateau)
    plateau.insérer_par_le_haut('X', [1, 2])
    plateau.état_plateau()

    # Detection des erreurs
    try_quixoerror(lambda: plateau[1, 6])
    try_quixoerror(lambda: plateau[6, 1])

    def assign(position, valeur):
        plateau[position] = valeur

    try_quixoerror(assign, (1, 6), 'X')
    try_quixoerror(assign, (6, 1), 'X')
    try_quixoerror(assign, (1, 1), 'A')
    try_quixoerror(plateau.insérer_un_cube, ' ', [1, 1], 'droite')
    try_quixoerror(plateau.insérer_un_cube, 'X', [5, 1], 'droite')
    try_quixoerror(plateau.insérer_un_cube, 'O', [1, 1], 'haut')
    try_quixoerror(plateau.insérer_par_le_bas, 'X', [0, 1])


def test_ia():
    '''
    test QuixoIA
    '''

    echec_msg = "Échec du test custom QuixoIA"

    # Critère 1 (all memebers of teams must make a commit)
    # Critère 2 - P2P-8 (pylint 10/10 score)
    # Critère 3 - lister_les_coups_possibles
    plateau = Plateau([
        ['O', ' ', ' ', ' ', ' '],
        [' ', 'X', 'X', 'X', 'O'],
        [' ', 'O', 'X', ' ', 'O'],
        [' ', 'X', 'X', 'X', 'O'],
        ['O', ' ', ' ', ' ', 'O'],
    ])
    ia = QuixoIA([], plateau)
    coups = ia.lister_les_coups_possibles(plateau, 'X')
    assert len(coups) == 29, echec_msg
    coups = ia.lister_les_coups_possibles(plateau, 'O')
    assert len(coups) == 44, echec_msg
    # Critère 4 - analyser_le_plateau
    assert (ia.analyser_le_plateau(plateau) ==
            {'X': {2: 2, 3: 5, 4: 0, 5: 0},
             'O': {2: 4, 3: 0, 4: 1, 5: 0}}), echec_msg
    # Critère 5 - trouver_un_coup_vainqueur
    org_vinq, dir_vinq = ia.trouver_un_coup_vainqueur('O')
    assert org_vinq[1] == 1 and dir_vinq == 'droite', echec_msg
    # critère 6 - trouver_un_coup_bloquant
    org_bloq, dir_bloq = ia.trouver_un_coup_bloquant('X')
    assert org_bloq[1] == 1 and dir_bloq == 'droite', echec_msg
    # critère 7 - jouer_un_coup
    ia.jouer_un_coup('O')
    try_quixoerror(ia.jouer_un_coup, ' ')
    try_quixoerror(ia.jouer_un_coup, 'A')
    try_quixoerror(ia.jouer_un_coup, 'O')
    assert ia.plateau[5, 1] == 'O', echec_msg
    assert ia.partie_terminée() == 'O', echec_msg
    ia = QuixoIA([], plateau)
    ia.jouer_un_coup('X')
    assert ia.plateau[5, 1] == 'X', echec_msg
    assert ia.partie_terminée() is None, echec_msg
    ia = QuixoIA([])
    ia.jouer_un_coup('X')  # coup aléatoire
    # Critère 8 - insertion cube error
    plateau8 = Plateau(plateau)
    try_quixoerror(plateau8.insérer_un_cube, 'A', [1, 1], 'droite')
    try_quixoerror(plateau8.insérer_un_cube, ' ', [1, 1], 'droite')
    plateau8.insérer_un_cube('X', [5, 1], 'bas')
    try_quixoerror(plateau8.insérer_un_cube, 'O', [3, 5], 'bas')
    try_quixoerror(plateau8.insérer_un_cube, 'O', [3, 1], 'haut')
    try_quixoerror(plateau8.insérer_un_cube, 'O', [1, 1], 'gauche')
    try_quixoerror(plateau8.insérer_un_cube, 'O', [5, 1], 'droite')
    try_quixoerror(plateau8.insérer_un_cube, 'X', [3, 4], 'droite')


def try_quixoerror(callback, *args):
    '''
    Méthode utilitaire pour tester les erreurs
    '''
    try:
        callback(*args)
    except QuixoError:
        assert True
    else:
        assert False


if __name__ == "__main__":
    test_formater_le_damier_pour_une_nouvelle_partie()
    print("Test de formater le damier pour une nouvelle partie réussi")
    test_formater_le_jeu_pour_une_nouvelle_partie()
    print("Test de formater le jeu pour une nouvelle partie réussi")
    test_formater_le_jeu_pour_une_partie_avancée()
    print("Test de formater le jeu pour une partie avancée réussi")

    # custom tests (phase 2)
    tester_plateau()
    print("Test custom classe plateau réussi")

    # custom tests (phase 3)
    test_ia()
    print("Test custom ia réussi")
