import random
from Carte import Carte

class Table:
    def __init__(self):
        self.paquet = self.creer_paquet()
        self.cartes_communes = []
        self.pot = 0
        self.joueurs = []
        self.mise_actuelle = 0
        self.index_small_blind = 0
        self.small_blind_value = 10

    def creer_paquet(self):
        valeurs = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        couleurs = ["h", "d", "c", "s"]
        return [Carte(valeur, couleur) for valeur in valeurs for couleur in couleurs]

    def melanger_paquet(self):
        random.shuffle(self.paquet)

    def distribuer_cartes(self):
        for joueur in self.joueurs:
            joueur.ajouter_cartes([self.paquet.pop(), self.paquet.pop()])

    def ajouter_cartes_communes(self, nombre):
        for _ in range(nombre):
            self.cartes_communes.append(self.paquet.pop())

    def appliquer_blinds(self):
        small_blind_joueur = self.joueurs[self.index_small_blind]
        big_blind_joueur = self.joueurs[(self.index_small_blind + 1) % len(self.joueurs)]

        # Small Blind
        small_blind_mise = small_blind_joueur.miser(self.small_blind_value)
        print(f"{small_blind_joueur.nom} pose la Small Blind de {small_blind_mise} jetons.")
        self.pot += small_blind_mise

        # Big Blind
        big_blind_mise = big_blind_joueur.miser(self.small_blind_value * 2)
        print(f"{big_blind_joueur.nom} pose la Big Blind de {big_blind_mise} jetons.")
        self.pot += big_blind_mise

        # Ajuster la mise actuelle
        self.mise_actuelle = self.small_blind_value * 2

        # Rotation des blinds
        self.index_small_blind = (self.index_small_blind + 1) % len(self.joueurs)

    def tour_de_mise(self):
        joueurs_actifs = [joueur for joueur in self.joueurs if joueur.actif and not joueur.all_in]

        while len(joueurs_actifs) > 1:
            for joueur in joueurs_actifs[:]:
                if len(joueurs_actifs) == 1:
                    break

                print(f"Pot actuel : {self.pot} | Mise actuelle : {self.mise_actuelle}")
                print(f"{joueur.nom}, vous avez {joueur.jetons} jetons et une mise personnelle de {joueur.mise_personnelle} jetons.")

                if joueur.mise_personnelle < self.mise_actuelle:
                    print(f"{joueur.nom}, vous devez au moins égaler la mise actuelle de {self.mise_actuelle} jetons.")
                    action = "suivre"
                else:
                    action = input("Action (miser, suivre, relancer, se_coucher) : ").lower()

                if action == "miser":
                    while True:
                        try:
                            mise = int(input("Montant à miser : "))
                            if mise > 0:
                                self.mise_actuelle = max(self.mise_actuelle, joueur.mise_personnelle + mise)
                                self.pot += joueur.miser(mise)
                                break
                            else:
                                print("La mise doit être supérieure à 0.")
                        except ValueError:
                            print("Entrée invalide. Veuillez entrer un montant valide.")

                elif action == "suivre":
                    mise_a_suivre = self.mise_actuelle - joueur.mise_personnelle
                    self.pot += joueur.miser(mise_a_suivre)

                elif action == "relancer":
                    while True:
                        try:
                            relance = int(input("Montant de la relance : "))
                            if relance > 0:
                                mise_totale = self.mise_actuelle + relance
                                self.mise_actuelle = mise_totale
                                self.pot += joueur.miser(mise_totale - joueur.mise_personnelle)
                                break
                            else:
                                print("La relance doit être supérieure à 0.")
                        except ValueError:
                            print("Entrée invalide. Veuillez entrer un montant valide.")

                elif action == "se_coucher":
                    joueur.se_coucher()
                    joueurs_actifs.remove(joueur)

                else:
                    print("Action invalide. Réessayez.")
                    continue

    def distribuer_pot(self, gagnant):
        for joueur in self.joueurs:
            if joueur.nom == gagnant:
                joueur.jetons += self.pot
        print(f"{gagnant} remporte {self.pot} jetons !")
        self.pot = 0

    def nettoyer_table(self):
        self.cartes_communes = []
        for joueur in self.joueurs:
            joueur.main = []
            joueur.actif = joueur.jetons > 0
            joueur.all_in = False
            joueur.mise_personnelle = 0

    def afficher_jetons_joueurs(self):
        for joueur in self.joueurs:
            print(f"{joueur.nom} : {joueur.jetons} jetons")

    def __repr__(self):
        return f"Table(Pot: {self.pot}, communes: {self.cartes_communes})"