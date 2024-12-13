from treys import Card, Evaluator
from Table import Table
from Joueur import Joueur

def jouer_partie():
    # Initialisation
    table = Table()
    table.melanger_paquet()

    nombre_joueurs = int(input("Combien de joueurs ? "))
    for i in range(nombre_joueurs):
        nom = input(f"Nom du joueur {i + 1} : ")
        jetons = int(input(f"Jetons pour {nom} : "))
        table.joueurs.append(Joueur(nom, jetons))

    continuer = True
    while continuer:
        table.melanger_paquet()
        table.distribuer_cartes()

        print("Cartes distribuées !")
        for joueur in table.joueurs:
            if joueur.actif:
                print(f"{joueur.nom} : {', '.join(map(str, joueur.main))}")

        # Phases du jeu
        phases = [("Flop", 3), ("Turn", 1), ("River", 1)]
        for nom_phase, nombre_cartes in phases:
            if len([joueur for joueur in table.joueurs if joueur.actif]) == 1:
                break
            print(f"Phase : {nom_phase}")
            table.ajouter_cartes_communautaires(nombre_cartes)
            print("Cartes communautaires :", ', '.join(map(str, table.cartes_communautaires)))
            table.tour_de_mise()

        # Vérification pour gagnant unique
        joueurs_actifs = [joueur for joueur in table.joueurs if joueur.actif]
        if len(joueurs_actifs) == 1:
            gagnant = joueurs_actifs[0].nom
            print(f"Tous les autres joueurs se sont couchés. {gagnant} remporte le pot !")
            table.distribuer_pot(gagnant)
        else:
            # Détermination du gagnant
            evaluator = Evaluator()
            mains = {}
            for joueur in table.joueurs:
                if joueur.actif:
                    main = [Card.new(carte.to_treys_format()) for carte in joueur.main]
                    communautaires = [Card.new(carte.to_treys_format()) for carte in table.cartes_communautaires]
                    score = evaluator.evaluate(communautaires, main)
                    mains[joueur.nom] = score

            gagnant = min(mains, key=mains.get)
            print(f"Le gagnant est {gagnant} avec un score de {mains[gagnant]} !")
            table.distribuer_pot(gagnant)

        table.afficher_jetons_joueurs()
        table.nettoyer_table()

        # Vérification pour un nouveau tour
        joueurs_actifs = [joueur for joueur in table.joueurs if joueur.jetons > 0]
        if len(joueurs_actifs) <= 1:
            continuer = False
            print("La partie est terminée ! Le vainqueur est " + joueurs_actifs[0].nom)
        else:
            print("Un nouveau tour commence !")
