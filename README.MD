# Quixo

<img src="https://pax.ulaval.ca/static/GLO-1901/images/quixo.jpg" style="display: block; margin-left: auto; margin-right: auto;" alt="Quixo" width="50%" height="auto">

## Objectifs

Pour ce projet, vous allez réaliser un premier programme qui interagit avec la **ligne de commande** et qui accède à **Internet**. Vous allez aussi vous familiariser avec la logistique des projets, c'est-à-dire installer sur votre ordinateur un environnement de développement [VS Code](https://code.visualstudio.com/) et vous initier à un logiciel de gestion des révisions [Git](https://git-scm.com/).

## Prérequis

- [Git](https://git-scm.com/downloads/)
- [Python pour _macOS_](https://www.python.org/downloads/) ou [Python pour _Windows_](https://apps.microsoft.com/detail/9NCVDN91XZQP)
- [VS Code](https://code.visualstudio.com/download/)

**Avant de télécharger Python ou Git**, assurez-vous de vérifier s'il est déjà installé sur votre ordinateur depuis un terminal. Notez que pour Python, toutes les versions supérieure ou égale à 3.8 sont compatibles. Donc si vous avez déjà une de ces versions, inutile d'en installer une autre.

### _Windows_

Depuis le menu _« Démarrer »_, cherchez Powershell et exécutez-y la commande:

```powershell
python --version
```

Ça devrait afficher une information ressemblant à `Python 3.12.1` avec le numéro de **votre** version au lieu de `3.12.1`.

Si ça ne fonctionne pas, essayez la commande:

```powershell
python3 --version
```

Si aucune de ces 2 commandes ne fonctionne, vous devez télécharger Python depuis le Microsoft Store.

Pour Git vous pouvez vérifier avec la commande:

```powershell
git --version
```

### _macOS_

Depuis _« Finder »_, cherchez `Terminal`, ouvrez l'application puis exécuter la commande:

```zsh
python3 --version
```

L'information similaire à `Python 3.12.1` devrait s'afficher avec le numéro de **votre** version au lieu de `3.12.1`.

N'utilisez **jamais** la commande `python` sans le `3` sur _macOS_ car il fera référence à Python 2.

## Extension VS Code

Voici la liste des extensions **VS Code** que nous vous conseillons d'ajouter à votre configuration:

- Python (celui de Microsoft)
- GitLens — Git supercharged

## Commandes utiles

Exécuter les tests que nous vous avons fournis:

```bash
python3 tests.py
```

Installer un module externe **Python**:

```bash
pip3 install nom-du-module
```

Sous _macOS_ il sera important d'utiliser `pip3` et non pas `pip`.

Créer un bundle depuis un terminal:

```bash
git bundle create quixo.bundle --all
```

Vérifier que le bundle a été créé avec succès:

```bash
git bundle verify quixo.bundle
```

Ouvrir un bundle:

```bash
git clone quixo.bundle
```

**N'oubliez pas de supprimer les fichiers créés lors de l'ouverture du bundle pour ne pas vous embourber de fichiers inutiles.**

## Liens utile

- [Aide-mémoire Github Git](https://github.github.com/training-kit/downloads/fr/github-git-cheat-sheet.pdf)
