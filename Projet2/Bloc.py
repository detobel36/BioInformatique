class Bloc:

    # Création d'un bloc à partir d'une liste de séquence
    def __init__(self, list_seq, pourcIdentite = 0.5):
        self.list_seq = list_seq
        self.allGroupe = []
        self.pourcIdentite = pourcIdentite
        

        self.calculGroupe()
        print("Nombre de groupe: " + str(len(self.allGroupe)))
        self.calculProportion()


    # Permet de calculer les groupes
    def calculGroupe(self):
        # On parcourt toutes les séquences
        for testSeq in self.list_seq:
            groupeTrouve = False
            
            # On parcourt tous les blocs
            iGroupe = 0
            while iGroupe < len(self.allGroupe) and not groupeTrouve:
                groupe = self.allGroupe[iGroupe]
                iGroupe += 1
                
                # Mais également toutes les séquences de ce groupe
                iSeq = 0
                while iSeq < len(groupe) and not groupeTrouve:
                    seq = groupe[iSeq]
                    iSeq += 1
                    # On regarde si la sequence actuel est "identique" à la séquence de recherche
                    if(self.isSeqIdent(testSeq, seq)):
                        groupe.append(testSeq)
                        groupeTrouve = True
            
            # Si on a pas trouvé de groupe, on en créé un
            if(not groupeTrouve):
                self.allGroupe.append([testSeq])
    
    
    # On calcule la proportion de chaque lettre et leur combinaison dans ce bloc
    def calculProportion(self):
        # On divise le nombre d'occurence d'une lettre dans une colonne 
        # par le nombre d'élement dans le groupe
        allCacheLettre = []
        for groupe in self.allGroupe:
            cacheLettre = [{} for i in range(len(groupe[0]))]

            nbrSeq = len(groupe)
            for seq in groupe:
                for col in range(len(seq)):
                    lettre = seq[col]
                    
                    if(lettre in cacheLettre[col]):
                        cacheLettre[col][lettre] += 1/nbrSeq
                    else:
                        cacheLettre[col][lettre] = 1/nbrSeq

            allCacheLettre.append(cacheLettre)

        # On va ensuite combiner tous ces résultats pour former des paires
        self.resultDictionnary = {}

        for iGroupeUn in range(len(allCacheLettre)):
            for iGroupeDeux in range(len(allCacheLettre)):
                if(iGroupeUn != iGroupeDeux):
                    for col in range(len(allCacheLettre[iGroupeUn])):

                        for keyA, valeurA in allCacheLettre[iGroupeUn][col].items():

                            for keyB, valeurB in allCacheLettre[iGroupeDeux][col].items():
                                if(keyA != keyB or iGroupeDeux < iGroupeUn):
                                    dicKey = keyA+keyB
                                    if(dicKey in self.resultDictionnary):
                                        self.resultDictionnary[dicKey] += valeurA * valeurB
                                    else:
                                        self.resultDictionnary[dicKey] = valeurA * valeurB


    # Permet d'avoir la proportion pondéré de l'apparition d'une 
    # combinaison de lettre dans les différents groupes
    def getProportionLettre(self, lettreA, lettreB):
        key = lettreA+lettreB
        if(key in self.resultDictionnary):
            return self.resultDictionnary[key]
        else:
            return 0


    # Permet de savoir si deux séquences sont "identiques" 
    # (en fonction du paramètre donné lors de l'initialisation)
    def isSeqIdent(self, seq1, seq2):
        if(len(seq1) != len(seq2)):
            raise SyntaxError("Les séquences n'ont pas le même " \
                "nombre de caractère %d != %d " % (seq1, seq2))

        objectif = self.pourcIdentite*len(seq1)
        total = 0
        i = 0
        while i < len(seq1) and total < objectif:
            if(seq1[i] == seq2[i]):
                total += 1
            i += 1

        return total >= objectif


    # Permet d'afficher les groupes de ce bloc
    def printGroupe(self):
        i = 0
        for groupe in self.allGroupe:
            i += 1
            print("Groupe " + str(i) + ": " + " ".join(groupe))