import random
from Carte import Carte

class Table:
    def __init__(self):
        self.paquet = self.creer_paquet()
        self.cartes_communes = []
        self.pot = 0
        self.joueurs = []
        self.mise_actuelle = 0

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

    def tour_de_mise(self):
        self.mise_actuelle = 0
        joueurs_actifs = [joueur for joueur in self.joueurs if joueur.actif and not joueur.all_in]
        checks_consecutifs = 0

        while len(joueurs_actifs) > 1:
            for joueur in joueurs_actifs[:]:
                if len(joueurs_actifs) == 1:
                    break

                print(f"Pot actuel : {self.pot} | Mise actuelle : {self.mise_actuelle}")
                print(f"{joueur.nom}, vous avez {joueur.jetons} jetons.")
                action = input("Action (check, miser, suivre, relancer, fold) : ").lower()

                if action == "check":
                    checks_consecutifs += 1
                    if checks_consecutifs >= len(joueurs_actifs):
                        print("Tous les joueurs ont checké. Passage à la phase suivante.")
                        return

                elif action == "miser":
                    while True:
                        try:
                            mise = int(input("Montant à miser : "))
                            if mise >= self.mise_actuelle:
                                self.mise_actuelle = mise
                                self.pot += joueur.miser(mise)
                                checks_consecutifs = 0
                                if joueur.all_in:
                                    joueurs_actifs.remove(joueur)
                                break
                            else:
                                print("La mise doit être au moins égale à la mise actuelle.")
                        except ValueError:
                            print("Entrée invalide. Veuillez entrer un montant valide.")


                elif action == "suivre":
                    self.pot += joueur.miser(self.mise_actuelle)
                    checks_consecutifs = 0
                    if joueur.all_in:
                        joueurs_actifs.remove(joueur)

                elif action == "relancer":
                    while True:
                        relance = int(input("Montant de la relance : "))
                        total_mise = self.mise_actuelle + relance
                        if relance > 0:
                            self.mise_actuelle = total_mise
                            self.pot += joueur.miser(total_mise)
                            checks_consecutifs = 0
                            if joueur.all_in:
                                joueurs_actifs.remove(joueur)
                            break
                        else:
                            print("La relance doit être supérieure à 0.")

                elif action == "fold":
                    joueur.fold()
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

    def afficher_jetons_joueurs(self):
        for joueur in self.joueurs:
            print(f"{joueur.nom} : {joueur.jetons} jetons")

    def __repr__(self):
        return f"Table(Pot: {self.pot}, communes: {self.cartes_communes})"