from math import log2

class Score:

    # Lettres utilisées pour représenter des acides aminés dans les matrices BLOSUM
    BLOSUM_LETTER = "ARNDCQEGHILKMFPSTWYVBZX"
    
    
    #Création de l'objet Score à partir d'une liste de blocs
    def __init__(self, listBloc, debug = False):
        self.listBloc = listBloc
        self.debug = debug

        # Si la liste des blocs est vide, impossible de calculer un score
        if(len(listBloc) == 0):
            raise ValueError("La liste des blocs ne peut pas être vide")
        
        if(self.debug):
            print("Calcul du Score avec " + str(len(listBloc)) + 
                " bloc" + ("s" if len(listBloc) > 1 else "") + "\n")

        self.initMatriceFreqPondere()
        self.calculMatriceFreqPond()
        self.calculProbaOccurence()

        self.calculListProbaResidu()
        self.calculMatriceScore()


    # Permet d'initialiser une matrice des fréquences pondéré
    def initMatriceFreqPondere(self):
        # Pour éviter de faire des calcules inutiles, on ne va utilisé qu'une demi matrice
        # En effet, celle-ci est symétrique
        self.matFreqPond = [[0 for i in range(j+1)] for j in range(len(Score.BLOSUM_LETTER))]


    # On calcule les fréquences pondéré à mettre dans la matrice
    def calculMatriceFreqPond(self):
        if(self.debug): # Si on est en mode debug, on affiche les groupes
            for bloc in self.listBloc:
                bloc.printGroupe()

        # Pour chaque ligne, chaque colonne et chaque groupe
        for ligne in range(len(self.matFreqPond)):
            for col in range(len(self.matFreqPond[ligne])):
                for bloc in self.listBloc:
                    self.matFreqPond[ligne][col] += bloc.getProportionLettre(Score.BLOSUM_LETTER[ligne], \
                                                                             Score.BLOSUM_LETTER[col])
        if(self.debug):
            self.printMatrice(self.matFreqPond)


    # Calcule des probabilités d'occurrence
    def calculProbaOccurence(self):
        sumDemiMatrice = sum([sum(elem) for elem in self.matFreqPond])

        if(self.debug):
            print("\nSomme de la demi-matrice: " + str(sumDemiMatrice))

        for ligne in range(len(self.matFreqPond)):
            for colonne in range(len(self.matFreqPond[ligne])):
                self.matFreqPond[ligne][colonne] = (self.matFreqPond[ligne][colonne] / sumDemiMatrice)


    # Pour calculer le taux de log-chance on calcul la probabilité d'occurence pour un
    # acide aminé.  Cela forme donc une liste
    def calculListProbaResidu(self):
        if(self.debug):
            strDebug = ""

        self.listFreqResidu = []
        for lettre in range(len(Score.BLOSUM_LETTER)):
            total = 0
            for index in range(len(Score.BLOSUM_LETTER)):
                if(index != lettre):
                    total += self.matFreqPond[max(index, lettre)][min(index, lettre)]

            self.listFreqResidu.append(self.matFreqPond[lettre][lettre] + (total/2))
            if(self.debug):
                strDebug += (Score.BLOSUM_LETTER[lettre] + "=" 
                        + str(round(self.listFreqResidu[-1], 2)) + " ")

        if(self.debug):
            print("\nListe de la probabilité d'occurence d'un alignement:")
            print(strDebug)


    # Permet de calculer la matrice score avec toutes les informations faites précédemment
    def calculMatriceScore(self):
        self.resMatrice = [] # resMatric contiendra la matrice final
        for ligne in range(len(Score.BLOSUM_LETTER)):
            self.resMatrice.append([])
            for colonne in range(ligne+1):
                currentMatrice = self.matFreqPond[ligne][colonne]

                if(currentMatrice != 0):
                    if(ligne == colonne):
                        valeur = (self.listFreqResidu[ligne]**2)
                    else:
                        valeur = (2 * self.listFreqResidu[ligne] * self.listFreqResidu[colonne])

                    self.resMatrice[ligne].append(2*log2(currentMatrice / valeur))
                else:
                    self.resMatrice[ligne].append(0)


    # Permet d'afficher une matrice
    def printMatrice(self, matrice, max_nbr = 6):
        for i in range(len(matrice)):
            # Ligne avec les indices
            if(i == 0):
                print((" " * (max_nbr+1)), end="")
                for j in range(len(Score.BLOSUM_LETTER)):
                    print(Score.BLOSUM_LETTER[j].center(max_nbr, ' '), end="|")
                print()
            
            # Affichage des lignes
            for j in range(len(matrice[i])):
                if(j == 0):
                    # Affiche l'indice
                    print(Score.BLOSUM_LETTER[i].center(max_nbr, ' '), end="|")

                print(str(round(matrice[i][j])).center(max_nbr, ' '), end="|")
            print() # Retour à la ligne
            
    
    # Permet d'afficher le résultat (la matrice de substitution)
    def printResMatrice(self):
        self.printMatrice(self.resMatrice)