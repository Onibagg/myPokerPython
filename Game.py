from treys import Card, Evaluator
from Table import Table
from Joueur import Joueur

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BRIGHT = '\033[1m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_error(message):
    print(RED + message + RESET)

def print_event(message):
    print(BLUE + message + RESET)

def print_success(message):
    print(GREEN + message + RESET)

def print_phase(message):
    print(YELLOW + message + RESET)

def print_bright(message):
    print(BRIGHT + message + RESET)

def jouer_partie():
    table = Table()
    table.melanger_paquet()

    try:
        nombre_joueurs = int(input("Combien de joueurs ? "))
        while nombre_joueurs < 2:
            print_error("Il doit y avoir au moins" + BOLD + " 2 joueurs." + RESET)
            nombre_joueurs = int(input("Combien de joueurs ? "))

        nombre_jetons = int(input("Combien de jetons pour chaque joueur ? "))
        for i in range(nombre_joueurs):
            while True:
                nom = input(f"Nom du joueur {i + 1} : ")
                if any(joueur.nom == nom for joueur in table.joueurs):
                    print_error("Le nom du joueur doit être unique.")
                else:
                    table.joueurs.append(Joueur(nom, nombre_jetons))
                    break

    except ValueError:
        print_error("Entrée invalide. Veuillez entrer un nombre valide.")

    continuer = True
    while continuer:
        table.melanger_paquet()
        table.distribuer_cartes()

        print_event("Cartes distribuées !")
        for joueur in table.joueurs:
            if joueur.actif:
                print_bright(f"{joueur.nom} : {', '.join(map(str, joueur.main))}")

        phases = [("Flop", 3), ("Turn", 1), ("River", 1)]
        for nom_phase, nombre_cartes in phases:
            if len([joueur for joueur in table.joueurs if joueur.actif]) == 1:
                break
            print_phase(f"Phase : {nom_phase}")
            table.ajouter_cartes_communes(nombre_cartes)
            print(BOLD + "Cartes communes : " + RESET + ', '.join(map(str, table.cartes_communes)))
            table.tour_de_mise()

        joueurs_actifs = [joueur for joueur in table.joueurs if joueur.actif]
        if len(joueurs_actifs) == 1:
            gagnant = joueurs_actifs[0].nom
            print_success(f"Tous les autres joueurs se sont couchés. {gagnant} remporte le pot !")
            table.distribuer_pot(gagnant)
        else:
            evaluator = Evaluator()
            mains = {}
            for joueur in table.joueurs:
                if joueur.actif:
                    main = [Card.new(carte.to_treys_format()) for carte in joueur.main]
                    communes = [Card.new(carte.to_treys_format()) for carte in table.cartes_communes]
                    score = evaluator.evaluate(communes, main)
                    mains[joueur.nom] = score

            gagnant = min(mains, key=mains.get)
            print_success(f"Le gagnant est {gagnant} avec un score de {mains[gagnant]} !")
            table.distribuer_pot(gagnant)

        table.afficher_jetons_joueurs()
        table.nettoyer_table()

        joueurs_actifs = [joueur for joueur in table.joueurs if joueur.jetons > 0]
        if len(joueurs_actifs) <= 1:
            continuer = False
            print_success("----------------------------------------------------------------")
            print_success("La partie est terminée ! Le vainqueur est " + joueurs_actifs[0].nom)
            print_success("----------------------------------------------------------------")
        else:
            print_success("Un nouveau tour commence !")