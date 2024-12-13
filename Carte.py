class Carte:
    COULEURS = {"h": "♥", "d": "♦", "c": "♣", "s": "♠"}

    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur

    def __repr__(self):
        couleur_symbole = self.COULEURS.get(self.couleur, self.couleur)
        return f"{self.valeur}{couleur_symbole}"

    def to_treys_format(self):
        return f"{self.valeur}{self.couleur}"