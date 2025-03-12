"""Jeu Quixo

Ce programme permet de joueur au jeu Quixo.
"""

from api import initialiser_partie, jouer_un_coup
from quixo import Quixo, interpréter_la_commande
from quixo_ia import QuixoIA

# Mettre ici votre secret récupérer depuis le site de PAX
SECRET = "0eb411a2-bbc9-471d-a2f2-58b3d7f71bfc"


if __name__ == "__main__":
    args = interpréter_la_commande()
    id_partie, joueurs, plateau = initialiser_partie(args.idul, SECRET)
    while True:
        # Créer une instance de Quixo
        if args.autonome:
            quixo = QuixoIA(joueurs, plateau)
            print(quixo)
            origine, direction = quixo.jouer_un_coup('X')

        else:
            quixo = Quixo(joueurs, plateau)
            # Afficher la partie
            print(quixo)
            # Demander au joueur de choisir son prochain coup
            origine, direction = quixo.choisir_un_coup()

        # Envoyez le coup au serveur
        id_partie, joueurs, plateau = jouer_un_coup(
            id_partie,
            origine,
            direction,
            args.idul,
            SECRET,
        )
