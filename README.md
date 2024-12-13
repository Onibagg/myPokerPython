# Poker Texas Hold'em - Python

## Description
Ce projet implémente un jeu de Poker Texas Hold'em en Python, avec des fonctionnalités complètes pour gérer les règles de base du poker, y compris :

- Distribution des cartes
- Actions des joueurs : miser, suivre, relancer, se coucher, all-in
- Gestion des cartes communes (Flop, Turn, River)
- Détermination du gagnant avec la bibliothèque `treys`

## Fonctionnalités principales

- **Mécanique des mises** :
  - Gestion des mises personnelles pour chaque joueur.
  - Vérifications des règles du poker pour les actions (miser, suivre, checker, relancer).
  - Gestion du all-in.

- **Cartes et Communes** :
  - Distribution de cartes aléatoires aux joueurs.
  - Ajout progressif des cartes communes : Flop, Turn, River.

- **Calcul des mains** :
  - Utilisation de la bibliothèque `treys` pour évaluer les meilleures mains.

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Onibagg/myPokerPython.git
   ```
2. Accédez au répertoire :
   ```bash
   cd myPokerPython
   ```

## Utilisation

1. Lancez le script principal :
   ```bash
   python app.py
   ```
2. Suivez les instructions affichées pour configurer la partie (nombre de joueurs, jetons de départ).
3. Jouez en respectant les règles affichées à l'écran.

## Règles du jeu

- **Actions disponibles** :
  - `Miser` : Ajoute un montant supérieur ou égal à la mise actuelle.
  - `Suivre` : Ajoute le montant nécessaire pour égaler la mise actuelle.
  - `Relancer` : Augmente la mise actuelle d'un montant supplémentaire.
  - `Se coucher` : Quitte la manche en cours.

- **Phases** :
  - Flop : Distribution des 3 premières cartes communes.
  - Turn : Distribution de la 4ème carte commune.
  - River : Distribution de la 5ème carte commune.

## Dépendances

- Python 3.8+
- [treys](https://github.com/ihendley/treys) : Bibliothèque pour évaluer les mains de poker.

## Contribuer

1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`).
3. Effectuez vos modifications et committez-les (`git commit -m 'Ajout de nouvelle fonctionnalité'`).
4. Poussez la branche (`git push origin feature/nouvelle-fonctionnalite`).
5. Ouvrez une pull request.

## Auteurs

- **Gabin Demé & Victor Gillet** - Développeurs principaux
