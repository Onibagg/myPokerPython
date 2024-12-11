import random
from treys import Card, Evaluator

class Carte:
    COULEURS = {"c": "♣", "d": "♦", "s": "♠", "h": "♥"}
    REVERSE_COULEURS = {v: k for k, v in COULEURS.items()}
    NOMS_VALEURS = {
        "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
        "T": "10", "J": "Valet", "Q": "Dame", "K": "Roi", "A": "As"
    }
    NOMS_COULEURS = {
        "c": "trèfle", "d": "carreau", "s": "pique", "h": "cœur"
    }

    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur

    def __repr__(self):
        return f"{self.valeur}{self.couleur}"

    def __str__(self):
        return f"{self.NOMS_VALEURS[self.valeur]} de {self.NOMS_COULEURS[self.couleur]}"

    def to_treys_format(self):
        return f"{self.valeur}{self.couleur}"


class Joueur:
    def __init__(self, nom, jetons):
        self.nom = nom
        self.jetons = jetons
        self.main = []
        self.actif = True
        self.all_in = False

    def miser(self, montant):
        if montant >= self.jetons:
            montant = self.jetons
            self.all_in = True
            print(f"{self.nom} fait all-in avec {montant} jetons.")
        self.jetons -= montant
        return montant

    def se_coucher(self):
        self.actif = False

    def ajouter_cartes(self, cartes):
        self.main.extend(cartes)

    def __repr__(self):
        return f"Joueur({self.nom}, Jetons: {self.jetons}, Actif: {self.actif}, All-in: {self.all_in})"


class Table:
    def __init__(self):
        self.paquet = self.creer_paquet()
        self.cartes_table = []
        self.pot = 0
        self.joueurs = []

    def creer_paquet(self):
        valeurs = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        couleurs = ["c", "d", "s", "h"]
        return [Carte(valeur, couleur) for valeur in valeurs for couleur in couleurs]

    def melanger_paquet(self):
        random.shuffle(self.paquet)

    def distribuer_cartes(self):
        for joueur in self.joueurs:
            joueur.ajouter_cartes([self.paquet.pop(), self.paquet.pop()])

    def ajouter_cartes_table(self, nombre):
        for _ in range(nombre):
            self.cartes_table.append(self.paquet.pop())

    def tour_de_mise(self):
        for joueur in self.joueurs:
            if joueur.actif and not joueur.all_in:
                try:
                    mise = int(input(f"{joueur.nom}, combien voulez-vous miser ? "))
                    self.pot += joueur.miser(mise)
                except ValueError:
                    print("Mise invalide. Vous vous couchez.")
                    joueur.se_coucher()

    def __repr__(self):
        return f"Table(Pot: {self.pot}, Table: {self.cartes_table})"

# Logique du jeu
def jouer_partie():
    # Initialisation
    table = Table()
    table.melanger_paquet()

    nombre_joueurs = int(input("Combien de joueurs ? "))
    for i in range(nombre_joueurs):
        nom = input(f"Nom du joueur {i + 1} : ")
        jetons = int(input(f"Jetons pour {nom} : "))
        table.joueurs.append(Joueur(nom, jetons))

    table.distribuer_cartes()

    print("Cartes distribuées !")
    for joueur in table.joueurs:
        print(f"{joueur.nom} : {', '.join(map(str, joueur.main))}")

    # Phases du jeu
    phases = [("Flop", 3), ("Turn", 1), ("River", 1)]
    for nom_phase, nombre_cartes in phases:
        print(f"Phase : {nom_phase}")
        table.ajouter_cartes_table(nombre_cartes)
        print("Cartes table :", ', '.join(map(str, table.cartes_table)))
        table.tour_de_mise()

    # Détermination du gagnant
    evaluator = Evaluator()
    mains = {}
    for joueur in table.joueurs:
        if joueur.actif:
            main = [Card.new(carte.to_treys_format()) for carte in joueur.main]
            table_cards = [Card.new(carte.to_treys_format()) for carte in table.cartes_table]
            score = evaluator.evaluate(table_cards, main)
            mains[joueur.nom] = score

    gagnant = min(mains, key=mains.get)
    print(f"Le gagnant est {gagnant} avec un score de {mains[gagnant]} !")

# Démarrage
if __name__ == "__main__":
    jouer_partie()
