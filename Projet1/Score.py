class Score:

    # Creation de l'objet
    def __init__(self, nom_fichier):
        # Initialisation des variables
        self.listLettre = {}
        self.matrice = []

        # Ouverture du fichier
        fichier = open(nom_fichier, 'r')

        nbrLigne = 0
        for ligne in fichier:
            if(len(ligne) > 0 and ligne[0] != '#'):
                ligne = ligne.strip().split() # Separer la ligne et supprime les espaces

                # On verifie que la liste des lettres est definie
                if(len(self.listLettre) == 0):
                    # Si le premier caractere est une lettre
                    if(ligne[0].isalpha()):
                        self.listLettre = dict(enumerate(ligne))
                        self.listLettre = {v: k for k, v in self.listLettre.items()}

                    # Sinon, le fichier n'est pas correcte
                    else:
                        raise SyntaxError("Fichier invalide (debug ligne: %s )" % ligne)

                else:
                    self.matrice.append(ligne)
                    ++nbrLigne

    # Permet de récupérer le score en fonction de deux lettres
    def get(self, lettre1, lettre2):
        number1 = self.listLettre[lettre1]
        number2 = self.listLettre[lettre2]
        return self.matrice[max(number1, number2)][min(number1, number2)]

