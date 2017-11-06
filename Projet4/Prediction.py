# -*- coding:Utf8 -*-
from Utils import *

class Prediction:

    def __init__(self):
        self.freqStruc = {}
        self.freqStrucAA = {}
        self.freqStrucAAFen = {}


    def addSeqAndStruc(self, seq, struc):
        for indice in range(len(seq)):
            aa = seq[indice]
            structure = struc[indice]

            # Frequence d'une structure
            self.calculFreqStruc(structure)

            # Fréquence d'une structure associée à un AA
            self.calculFreqStrucAA(structure, aa)

            # Fréquence d'une structure associée à un AA et avec un aa étant à un certain décalage
            if(not (structure in self.freqStrucAAFen)):
                self.freqStrucAAFen[structure] = {aa: {}}

            elif(not (aa in self.freqStrucAAFen[structure])):
                self.freqStrucAAFen[structure][aa] = {}

            for var in range(-8, 9):
                if(var != 0 and (indice+var) >= 0 and (indice+var) < len(seq)):
                    aaDec = seq[indice+var]
                    if(aaDec in self.freqStrucAAFen[structure][aa]):
                        self.freqStrucAAFen[structure][aa][aaDec] += 1
                    else:
                        self.freqStrucAAFen[structure][aa][aaDec] = 1


    def calculFreqStruc(self, structure):
        if(structure in self.freqStruc):
            self.freqStruc[structure] += 1
        else:
            self.freqStruc[structure] = 1


    def calculFreqStrucAA(self, structure, aa):
        if(structure in self.freqStrucAA):
            if(aa in self.freqStrucAA[structure]):
                self.freqStrucAA[structure][aa] += 1
            else:
                self.freqStrucAA[structure][aa] = 1
        else:
            self.freqStrucAA[structure] = {aa: 1}


    def saveInFile(self, fileName):
        fichier = open(fileName, 'w')
        fichier.write(str(self.freqStruc))
        fichier.write("\n")
        fichier.write(str(self.freqStrucAA))
        fichier.write("\n")
        fichier.write(str(self.freqStrucAAFen))
        fichier.close()
        print("Base de donnée enregistrée")


    def loadSaveFile(self, fileName):
        fichier = open(fileName, 'r')
        i = 0
        for ligne in fichier:
            ligne = ligne.strip()
            if(ligne != ""):
                if(i == 0):
                    self.freqStruc = eval(ligne)
                elif(i == 1):
                    self.freqStrucAA = eval(ligne)
                else:
                    self.freqStrucAAFen = eval(ligne)
                i += 1

        fichier.close()


    def getFreqStruc(self, structure):
        res = 0
        if(structure in self.freqStruc):
            res = self.freqStruc[structure]
        return res;

    def getFreqNotStruc(self, structure):
        res = 0
        for struc in getStructure():
            if(struc != structure):
                res += self.getFreqStruc(struc)
        return res


    def getFreqStrucAA(self, structure, AA):
        res = 0
        if(structure in self.freqStrucAA and AA in self.freqStrucAA[structure]):
            res = self.freqStrucAA[structure][AA]
        return res

    def getFreqNotStrucAA(self, structure, aa):
        res = 0
        for struc in getStructure():
            if(struc != structure):
                res += self.getFreqStrucAA(struc, aa)
        return res


    def getFreqStrucAAFene(self, structure, aaFenetre, aa):
        res = 0
        if(structure in self.freqStrucAAFen and aa in self.freqStrucAAFen[structure] and
                aaFenetre in self.freqStrucAAFen[structure][aa]):
            res = self.freqStrucAAFen[structure][aa][aaFenetre]
        return res

    def getFreqNotStrucAAFene(self, structure, aaFenetre, aa):
        res = 0
        for struc in getStructure():
            if(struc != structure):
                res += self.getFreqStrucAAFene(struc, aaFenetre, aa)
        return res

