from math import sqrt
from math import log10


SWISS_PROT = {'A':0.0826, 'R':0.0553, 'N':0.0406, 'D':0.0546, 'C':0.0137,
              'Q':0.0393, 'E':0.0674, 'G':0.0708, 'H':0.0227, 'I':0.0593, 
              'L':0.0965, 'K':0.0582, 'M':0.0241, 'F':0.0386, 'P':0.0472, 
              'S':0.0660, 'T':0.0534, 'W':0.0109, 'Y':0.0292, 'V':0.0687}


class Profil:

    def __init__(self, listeSeq, penalite = -1):
        self.listeSeq = listeSeq
        self.pseudoCountBeta = sqrt(len(listeSeq))

        self.penalite = penalite

        print("Taille: "+str(len(listeSeq)))
        self.freqPosition()
        self.calculProbabilite()
        self.calculPSSM()


    def freqPosition(self):
        self.totalElemCol = [0]

        # Nombre de lettres par colonne
        self.listeFreq = [{}]
        for seq in self.listeSeq:
            col = 0
            for lettre in seq:
                if(len(self.listeFreq) <= col):
                    self.listeFreq.append({})
                    self.totalElemCol.append(0)

                if(lettre in self.listeFreq[col]):
                    self.listeFreq[col][lettre] += 1
                    self.totalElemCol[col] += 1

                elif(lettre != '-'):
                    self.listeFreq[col][lettre] = 1
                    self.totalElemCol[col] += 1
                    
                col += 1


        # Calcul de la fréquence
        total = len(self.listeSeq)
        for colonne in self.listeFreq:
            # total = sum([elem for elem in colonne.values()])
            for lettre in colonne:
                colonne[lettre] = colonne[lettre]/total


    def calculProbabilite(self):
        self.listeProba = [{}]
        col = 0
        
        for colonne in self.listeFreq:
            if(len(self.listeProba) <= col):
                self.listeProba.append({})

            for lettre in SWISS_PROT:
                self.listeProba[col][lettre] = self.makeCalcul(lettre, colonne, col)
            # for lettre in colonne:
            #     self.listeProba[col][lettre] = self.makeCalcul(lettre, colonne)

            col += 1

        # print_solution(self.listeProba)
        # print("Taille proba " + str(len(self.listeProba)))


    def makeCalcul(self, lettre, colonne, nbrColonne):
        # \frac{\alpha F(i,j) + \beta p(i)}{\alpha + \beta}

        valeurColonne = 0
        if(lettre in colonne):
            valeurColonne = colonne[lettre]

        pseudoCountAlpha = self.totalElemCol[nbrColonne]

        # Numérateur
        num = pseudoCountAlpha * valeurColonne + self.pseudoCountBeta * SWISS_PROT[lettre]
        # Dénominateur
        den = pseudoCountAlpha + self.pseudoCountBeta

        return (num / den)


    def calculPSSM(self):
        # m(i,j) = log \frac{q(i,j)}{p(i)}
        self.pssm = [{}]

        col = 0
        for colonne in self.listeProba:
            if(len(self.pssm) <= col):
                self.pssm.append({})

            for lettre in colonne:
                self.pssm[col][lettre] = log10(colonne[lettre]/SWISS_PROT[lettre])
            self.pssm[col]['-'] = self.penalite

            col += 1

        # print(self.pssm)

    def getPSSM(self):
        return self.pssm;

