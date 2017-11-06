# -*- coding:Utf8 -*-
from Utils import *
from math import log10
from math import sqrt


class GOR3:

    def __init__(self, prediction, testSeq):
        self.pred = prediction
        self.testSeq = testSeq
        self.result = ""

        self.calculGOR()
        self.getBestForPos()


    def calculGOR(self):
        self.matResult = []

        for iAA in range(len(self.testSeq)):
            aa = self.testSeq[iAA]

            self.matResult.append([])

            for iStruc in range(len(getStructure())):
                structure = list(getStructure())[iStruc]
        
                total = 0

                # Premier terme
                num1 = self.pred.getFreqStrucAA(structure, aa)
                div1 = self.pred.getFreqNotStrucAA(structure, aa)

                num2 = self.pred.getFreqNotStruc(structure)
                div2 = self.pred.getFreqStruc(structure)

                total += log10(num1 / div1) + log10(num2 / div2)

                # Second terme
                for i in range(-8, 9):
                    if(i != 0 and (iAA+i) >= 0 and (iAA+i) < len(self.testSeq)):
                        aaDecal = self.testSeq[iAA+i]

                        num1 = self.pred.getFreqStrucAAFene(structure, aaDecal, aa)
                        div1 = self.pred.getFreqNotStrucAAFene(structure, aaDecal, aa)

                        num2 = self.pred.getFreqNotStrucAA(structure, aa)
                        div2 = self.pred.getFreqStrucAA(structure, aa)

                        total += log10(num1 / div1) + log10(num2 / div2)

                self.matResult[iAA].append(total)

        # print(self.matResult)
    

    def getBestForPos(self):
        self.result = ""
        listeStruc = list(getStructure())

        for colonne in self.matResult:
            self.result += listeStruc[colonne.index(max(colonne))]


    def getResult(self):
        return self.result


    def calculQ3(self, correctStruc):
        res = 0
        if(len(self.result) != len(correctStruc)):
            print("Erreur, il faut que le résultat ai la même taille que la structure correcte (" 
                + str(len(self.result)) + " et " + str(len(correctStruc)))
        else:
            correct = 0
            for index in range(len(self.result)):
                if(self.result[index] == correctStruc[index]):
                    correct += 1
            res = correct / len(self.result)

        return res


    def increment(self, dictionnaire, niveau1, niveau2):
        if(niveau1 in dictionnaire):
            if(niveau2 in dictionnaire[niveau1]):
                dictionnaire[niveau1][niveau2] += 1
            else:
                dictionnaire[niveau1][niveau2] = 1
        else:
            dictionnaire[niveau1] = {niveau2: 1}

        return dictionnaire


    def calculTFandPN(self, correctStruc):
        # TrueFalse PositiveNegative
        self.tfpn = {}
        for index in range(len(self.result)):
            corrStruc = correctStruc[index]
            prediStruc = self.result[index]

            value = "T" if corrStruc == prediStruc else "F"

            for struc in getStructure():

                if(struc == prediStruc):
                    res = value + "P"
                elif(struc == corrStruc or value == "T"):
                    res = value + "N"
                else:
                    continue

                self.tfpn = self.increment(self.tfpn, struc, res)



        for struc in self.tfpn:
            for elem in self.tfpn[struc]:
                if(elem == 0):
                    print("Erreur")


    def calculMCC(self, correctStruc):
        self.calculTFandPN(correctStruc)

        res = {}
        if(len(self.result) != len(correctStruc)):
            print("Erreur, il faut que le résultat ai la même taille que la structure correcte (" 
                + str(len(self.result)) + " et " + str(len(correctStruc)))
        else:
            for struc in getStructure():
                total = (self.tfpn[struc]['TP'] * self.tfpn[struc]['TN']) - \
                            (self.tfpn[struc]['FP'] * self.tfpn[struc]['FN'])
                total /= sqrt((self.tfpn[struc]['TP'] + self.tfpn[struc]['FP']) * 
                                (self.tfpn[struc]['TP'] + self.tfpn[struc]['FN']) * 
                                (self.tfpn[struc]['TN'] + self.tfpn[struc]['FP']) * 
                                (self.tfpn[struc]['TN'] + self.tfpn[struc]['FN']))

                print("Stru: " + str(struc) + " total: " + str(total))
                res[struc] = total

        return res


