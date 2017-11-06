class Align:
    
    # Creation de l'objet
    def __init__(self, chaineA, pssm, debug = False):


        # Initialisation des variables
        self.chaineA = chaineA
        self.pssm = pssm
        self.debug = debug
        
        # Initialisation des matrices de calcul
        self.S = []
        # Creation d'une matrice ou la liste en ij permettra d'indiquer dans quel
        # direction on peut se deplacer (Horizontale, Vertical ou Diagonal)
        self.deplacement = []
        
        # Valeur maximum du tableau
        self.maxValue = 0
        # Coordonnees ou l'on peut trouver cette valeur
        self.maxI = [] 
        self.maxJ = []

        self.initMatrice()       # Initialisation de la matrice
        self.remplisageMatrice() # Remplissage de la matrice

        # print("------------------ Matrice S ------------------")
        # self.printMatrice(self.S)
        # print("")
        # print("")
        self.res = []   # Resultat final
        self.minIJ = [] # Coordonnees les plus petites atteintes
        
        # # Parcours de la matrice pour trouver le plus cours chemin
        for allMax in range(len(self.maxI)): # Parcourt toutes les valeurs maximum
            self.res += (self.findMinPath(self.maxI[allMax], self.maxJ[allMax], [], []))


    # Permet d'initialiser la matrice
    def initMatrice(self):
        
        for i in range(len(self.chaineA)+1):
            # Initialisation des lignes
            self.S.append([])
            self.deplacement.append([])

            for j in range(len(self.pssm)+1):
                if(i == 0): # Si l'on est sur la premiere ligne
                    # Initialisation de la matrice
                    self.S[i].append(0)
                    self.deplacement[i].append([])

                elif(j == 0): # Si l'on est sur la premiere colonne
                    # Initialisation de la matrice
                    self.S[i].append(0)
                    self.deplacement[i].append([])
                    
                else: # Sinon on remplit juste la liste des deplacements
                    self.deplacement[i].append([])


    # Permet de remplir la matrice
    def remplisageMatrice(self):
        # On parcourt toute la matrice
        for i in range(1, len(self.chaineA)+1):        # ligne
            for j in range(1, len(self.pssm)+1): # colonne

                valeur1 = self.S[i-1][j-1] + self.pssm[j-1][self.chaineA[i-1]]
                valeur2 = self.S[i-1][j] + self.pssm[j-1]['-']
                valeur3 = self.S[i][j-1] + self.pssm[j-2]['-']

                maximum = max(valeur1, valeur2, valeur3, 0)

                self.S[i].append(maximum)

                if(self.S[i][j] == valeur1):
                    self.deplacement[i-1][j-1].append("D") # Diagonal

                if(self.S[i][j] == valeur2):
                    self.deplacement[i-1][j].append("V") # Vertical

                if(self.S[i][j] == valeur3):
                    self.deplacement[i][j-1].append("H") # Horizontal


                # Enregistrement de la valeur maximum
                # Si la valeur est la meme que le max actuel
                if(self.maxValue == maximum):
                    self.maxI.append(i)
                    self.maxJ.append(j)

                # Si le max est plus grand que la valeur actuelle
                elif(maximum > self.maxValue):
                    self.maxI = [i]
                    self.maxJ = [j]
                    self.maxValue = maximum
                

        
        if(self.debug): # Si on veut débug, on affiche les matrices intermédiaire
            self.printMatrice(self.S)
            print()
            self.printMatrice(self.deplacement)
    
    


    # Permet d'afficher une matrice
    def printMatrice(self, matrice):
        for i in range(len(matrice)):
            # Ligne avec les indices
            if(i == 0):
                print("     ", end="")
                for j in range(len(matrice[i])):
                    print('{:4}|'.format(j), end="")
                print()
            
            # Affichage des lignes
            for j in range(len(matrice[i])):
                if(j == 0):
                    # Affiche l'indice
                    print('{:4}|'.format(i), end="")

                if(isinstance(matrice[i][j], list)):
                    print('{:4}|'.format("".join(matrice[i][j])), end="")
                else:
                    print('{:4}|'.format(str(round(matrice[i][j], 2))), end="")
            print() # Retour à la ligne

    
    # Permet de trouver le(s) bon(s) chemin(s) dans la matrice
    def findMinPath(self, i, j, current=[], sol=[]):
        if(i == 0 and j == 0): # Si on à fini le parcours
            sol.append(list(reversed(current)))
            self.minIJ.append((i, j))

        else:
            continuer = False # Est-il possible de continuer
            
            # Si on peut encore monter et que ce déplacement est possible
            if(i > 0 and "V" in self.deplacement[i-1][j]):
                continuer = True
                current.append("V") # Construction d'une solution
                sol = self.findMinPath(i-1, j, current[:], sol)
                current = current[:-1] # Déconstruction
            
            # Test a gauche cette fois
            if(j > 0 and "H" in self.deplacement[i][j-1]):
                continuer = True
                current.append("H")
                sol = self.findMinPath(i, j-1, current[:], sol)
                current = current[:-1]

            # Et enfin en diagonal
            if(i > 0 and j > 0 and "D" in self.deplacement[i-1][j-1]):
                continuer = True
                current.append("D")
                sol = self.findMinPath(i-1, j-1, current[:], sol)
                current = current[:-1]
            
            # Si il n'est plus possible de continuer et qu'on est en local
            if(not continuer):
                # On enregistre donc la solution
                sol.append(list(reversed(current)))
                self.minIJ.append((i, j))

        return sol


    # Permet d'afficher toutes les solutions
    def printResult(self):
        # Parcours de toutes les solutions
        for indexDeplacement in range(len(self.res)):

            position = ""
            resSeq = "     "
            modification = "     "

            # colonne et ligne de début à 0 sauf si on est en local
            col, ligne = self.minIJ[indexDeplacement]

            position += str(col)+" | "

            # On affiche le premier (celui qui match dès le début)

            # On parcours le resultat
            for dep in self.res[indexDeplacement]:
                if((col % 10 == 0) and dep == 'D'):
                    if(col < 10):
                        position += "  " + str(col)
                    elif(col < 100):
                        position += " " + str(col)
                    else:
                        position += str(col)
                else:
                    position += "  "


                if(dep == "D"):
                    resSeq += " " + self.chaineA[col-1]
                    modification += "  "
                    # On déplace le curseur
                    ligne += 1
                    col += 1

                elif(dep == "V"):
                    resSeq += " " + self.chaineA[col-1]
                    modification += " +"
                    col += 1

                elif(dep == "H"):
                    resSeq += "  "
                    modification += " -"
                    ligne += 1

            position += "| "+str(col)

            # Affichage des solutions
            print(position)
            print(resSeq)
            print(modification)
            print("")
            

    def getResult(self):
        return self.res