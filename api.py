"""Module d'API du jeu Quixo

Attributes:
    URL (str): Constante représentant le début de l'url du serveur de jeu.

Functions:
    * initialiser_partie - Créer une nouvelle partie et retourne l'état de cette dernière.
    * jouer_un_coup - Exécute un coup et retourne le nouvel état de jeu.
    * récupérer_une_partie - Retrouver l'état d'une partie spécifique.
"""

import requests

URL = "https://pax.ulaval.ca/quixo/api/a24/"


def initialiser_partie(idul, secret):
    """Initialiser une partie

    Args:
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple de 3 éléments constitué de l'identifiant de la partie en cours,
            de la liste des joueurs et de l'état du plateau.
    """
    rep = requests.post(
    URL+'partie/',
    auth=(idul, secret))
    if rep.status_code == 200:
        return (rep.json()["id"], rep.json()["état"]["joueurs"], rep.json()["état"]["plateau"])
    if rep.status_code == 401:
        raise PermissionError(rep.json()['message'])
    if rep.status_code == 406:
        raise RuntimeError(rep.json()['message'])
    raise ConnectionError("Unknown")


def jouer_un_coup(id_partie, origine, direction, idul, secret):
    """Jouer un coup

    Args:
        id_partie (str): Identifiant de la partie.
        origine (list): La position [x, y] du bloc à déplacer.
        direction (str): La direction du déplacement du bloc.:
            'haut': Déplacement d'un bloc du bas pour l'insérer en haut.
            'bas': Déplacement d'un bloc du haut pour l'insérer en bas.
            'gauche': Déplacement d'un bloc de droite pour l'insérer à gauche,
            'droite': Déplacement d'un bloc de gauche pour l'insérer à droite,
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        StopIteration: Erreur levée lorsqu'il y a un gagnant dans la réponse du serveur.
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple de 3 éléments constitué de l'identifiant de la partie en cours,
            de la liste des joueurs et de l'état du plateau.
    """
    rep = requests.put(
    f"{URL}partie/{id_partie}/",
    auth=(idul, secret),
    json={
        "origine": origine,
        "direction": direction,
    })
    if rep.status_code == 200:
        if rep.json()["gagnant"] is not None:
            raise StopIteration(rep.json()["gagnant"])
        return (rep.json()["id"], rep.json()["état"]["joueurs"], rep.json()["état"]["plateau"])
    if rep.status_code == 401:
        raise PermissionError(rep.json()['message'])
    if rep.status_code == 406:
        raise RuntimeError(rep.json()['message'])
    raise ConnectionError("Unknown")

def récupérer_une_partie(id_partie, idul, secret):
    """Récupérer une partie

    Args:
        id_partie (str): identifiant de la partie à récupérer
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple de 4 éléments constitué de l'identifiant de la partie en cours,
            de la liste des joueurs, de l'état du plateau et du vainqueur.
    """
    rep = requests.get(
    f"{URL}partie/{id_partie}/",
    auth=(idul, secret))
    if rep.status_code == 200:
        if rep.json()["gagnant"] is not None:
            return (rep.json()["id"], rep.json()["état"]["joueurs"], rep.json()["état"]["plateau"]
                    ,rep.json()["gagnant"]
                    )
        return (rep.json()["id"], rep.json()["état"]["joueurs"], rep.json()["état"]["plateau"],None)
    if rep.status_code == 401:
        raise PermissionError(rep.json()['message'])
    if rep.status_code == 406:
        raise RuntimeError(rep.json()['message'])
    raise ConnectionError("Unknown")
