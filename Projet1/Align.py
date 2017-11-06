class Align:    
    
    # Creation de l'objet
    def __init__(self, chaineA, chaineB, score, openPenal = -12, extendPenal = -2, \
                 local = False, semiGlobal = False, debug = False):


        # Initialisation des variables
        self.chaineA = chaineA
        self.chaineB = chaineB
        self.score = score
        self.openPenal = openPenal     # Coût pour ouvrir un trou
        self.extendPenal = extendPenal # Coût pour prolonger un trou
        self.local = local
        self.semiGlobal = semiGlobal and not local
        self.debug = debug
        
        # Initialisation des matrices de calcul
        self.S = []
        self.V = []
        self.W = []
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
        self.res = []   # Resultat final
        self.minIJ = [] # Coordonnees les plus petites atteintes
        
        # Parcours de la matrice pour trouver le plus cours chemin
        if(self.local or self.semiGlobal): # Si c'est une recherche locale ou semiGlobal
            for allMax in range(len(self.maxI)): # Parcourt toutes les valeurs maximum
                self.res += (self.findMinPath(self.maxI[allMax], self.maxJ[allMax], [], []))

        else: # Sinon on fait une simple recherche
            self.res = self.findMinPath(len(chaineA), len(chaineB))



    # Permet d'initialiser la matrice
    def initMatrice(self):
        
        for i in range(len(self.chaineA)+1):
            # Initialisation des lignes
            self.S.append([])
            self.V.append([])
            self.W.append([])
            self.deplacement.append([])
            
            for j in range(len(self.chaineB)+1):
                if(i == 0): # Si l'on est sur la premiere ligne
                    if(self.local or self.semiGlobal):
                        valeur = 0
                        self.deplacement[i].append([])
                    else:
                        # La valeur va etre egal a la colonne fois l'ouverture d'une penalite si
                        # on est en colonne 0 ou 1, sinon ce sera egale a la ligne precedente 
                        # plus le prolongement de la penalite
                        valeur = j*self.openPenal if j <= 1 else self.S[i][j-1] + self.extendPenal
                        # Les deplacements se font horizontalement sauf en 0,0
                        self.deplacement[i].append(["H"] if j != 0 else ["H", "V"])
                        
                    # Initialisation des 3 matrices
                    self.S[i].append(valeur)
                    self.V[i].append(valeur)
                    self.W[i].append(valeur)

                elif(j == 0): # Si l'on est sur la premiere colonne
                    if(self.local or self.semiGlobal):
                        valeur = 0 # par defaut on met 0 partout
                        self.deplacement[i].append([])
                    else:
                        # Pareil que pour la ligne 0 mais ici c'est la colonne
                        valeur = i*self.openPenal if i <= 1 else self.S[i-1][j] + self.extendPenal
                        self.deplacement[i].append(["V"])
                    
                    # Initialisation des 3 matrices
                    self.S[i].append(valeur)
                    self.V[i].append(valeur)
                    self.W[i].append(valeur)

                else: # Sinon on remplit juste la liste des deplacements
                    self.deplacement[i].append([])

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
                    print('{:4}|'.format(str(matrice[i][j])), end="")
            print() # Retour à la ligne

    
    # Permet de trouver le(s) bon(s) chemin(s) dans la matrice
    def findMinPath(self, i, j, current=[], sol=[]):
        if(i == 0 and j == 0 or (self.semiGlobal and (i == 0 or j == 0))): # Si on à fini le parcours
            sol.append(list(reversed(current)))
            self.minIJ.append([i, j])

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
            if(not continuer and self.local):
                # On enregistre donc la solution
                sol.append(list(reversed(current)))
                self.minIJ.append([i, j])

        return sol


    # Permet de remplir la matrice
    def remplisageMatrice(self):
        # On parcourt toute la matrice
        for i in range(1, len(self.chaineA)+1):
            for j in range(1, len(self.chaineB)+1):
                
                # V(i, j) = max((S[i-1][j]-I), V[i-1][j]-E)
                choixV1 = self.S[i-1][j]+self.openPenal
                choixV2 = self.V[i-1][j]+self.extendPenal

                self.V[i].append(max(choixV1, choixV2))

                # W(i, j) = max((S[i][j-1]-I), W[i][j-1]-E)
                choixW1 = self.S[i][j-1]+self.openPenal
                choixW2 = self.W[i][j-1]+self.extendPenal

                self.W[i].append(max(choixW1, choixW2))

                # S(i, j) = max((S[i-1][j-1] + score), (V[i][j]), (W[i][J]))
                choixS1 = self.S[i-1][j-1] + int(self.score.get(self.chaineA[i-1], self.chaineB[j-1]))
                choixS2 = self.V[i][j]
                choixS3 = self.W[i][j]

                # Si on cherche les sequences local
                if(self.local):
                    maximum = max(choixS1, choixS2, choixS3, 0)
                else:
                    maximum = max(choixS1, choixS2, choixS3)

                # Enregistrement de la valeur maximum si l'on est pas en
                # semiGlobal ou que l'on est sur la dernière ligne
                if(not self.semiGlobal or i == len(self.chaineA)):
                    # Si la valeur est la meme que le max actuel
                    if(self.maxValue == maximum):
                        self.maxI.append(i)
                        self.maxJ.append(j)

                    # Si le max est plus grand que la valeur actuelle
                    elif(maximum > self.maxValue):
                        self.maxI = [i]
                        self.maxJ = [j]
                        self.maxValue = maximum


                # On ajout le maximum dans la matrice
                self.S[i].append(maximum)

                
                if(self.S[i][j] == choixS1):
                    self.deplacement[i-1][j-1].append("D") # Diagonal

                if(self.S[i][j] == choixS2):
                    self.deplacement[i-1][j].append("V") # Horizontal

                if(self.S[i][j] == choixS3):
                    self.deplacement[i][j-1].append("H") # Vertical
        
        if(self.debug): # Si on veut débug, on affiche les matrices intermédiaire
            self.printMatrice(self.S)
            print()
            self.printMatrice(self.deplacement)
    
    
    # Permet d'afficher toutes les solutions
    def printResult(self):
        # Parcours de toutes les solutions
        for indexDeplacement in range(len(self.res)):
            # Initialisation des variables de travail
            resSeq1 = self.chaineA.getNom()
            separation = " "
            resSeq2 = self.chaineB.getNom()

            # Aligne les 3 champs
            tailleEspace = max(len(resSeq1), len(resSeq2))
            resSeq1 += (tailleEspace - len(resSeq1))*separation + ": "
            resSeq2 += (tailleEspace - len(resSeq2))*separation + ": "
            separation = " "*tailleEspace + "  "

            
            # colonne et ligne de début à 0 sauf si on est en local
            col = 0 if(not self.local and not self.semiGlobal) else self.minIJ[indexDeplacement][0]
            ligne =  0 if(not self.local and not self.semiGlobal) else self.minIJ[indexDeplacement][1]

            if(self.debug):
                print("Solution: " + str(self.res[indexDeplacement]))

            # On parcours le resultat
            for dep in self.res[indexDeplacement]:

                if dep == "D":
                    resSeq1 += self.chaineA[col]
                    resSeq2 += self.chaineB[ligne]
                    # Affiche une bar si les lettres sont les mêmes
                    if(self.chaineA[col] == self.chaineB[ligne]):
                        separation += ":"   
                    elif(int(self.score.get(self.chaineA[col], self.chaineB[ligne])) >=  0):
                        separation += "."
                    else:
                        separation += " "
                    # On déplace le curseur
                    ligne += 1
                    col += 1

                elif dep == "H":
                    resSeq1 += "-"
                    resSeq2 += self.chaineB[ligne]
                    separation += " "
                    ligne += 1

                elif dep == "V":
                    resSeq1 += self.chaineA[col]
                    resSeq2 += "-"
                    separation += " "
                    col += 1

            # Affichage des solutions
            print(resSeq1)
            print(separation)
            print(resSeq2)
            print("")
            

    def getResult(self):
        return self.res