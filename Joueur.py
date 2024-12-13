class Joueur:
    def __init__(self, nom, jetons):
        self.nom = nom
        self.jetons = jetons
        self.main = []
        self.actif = True
        self.all_in = False

    def miser(self, montant):
        if montant > self.jetons:
            montant = self.jetons  # All-in si mise supérieure aux jetons
            self.all_in = True
            print(f"{self.nom} fait un ALL-IN avec {montant} jetons !")
        self.jetons -= montant
        return montant

    def se_coucher(self):
        self.actif = False

    def ajouter_cartes(self, cartes):
        self.main.extend(cartes)

    def __repr__(self):
        return f"Joueur({self.nom}, Jetons: {self.jetons}, Actif: {self.actif})"
