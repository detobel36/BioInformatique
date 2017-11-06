CONVERT_L_STRUCTURE = {'H':'H', 'G':'H', 'I':'H', # H,G,I -> H
                'E':'E', 'B':'E',                 # E,B -> E
                'T':'T',                          # T -> T
                'C':'C', 'S':'C', ' ':'C'}        # C,S,' ' -> C

def getStructure():
    return set(CONVERT_L_STRUCTURE.values())

def getAllStructure():
    return list(CONVERT_L_STRUCTURE.keys())

def convertStructure(lettreStructure):
    return CONVERT_L_STRUCTURE[lettreStructure]

def getAllAA():
    return ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']


# Class permettant d'encapsuler le parser
class Parser:
    
    # On indique au parser le fichier cath qu'il va utiliser ainsi que le dossier 
    # où se touves les fichiers DSSP
    def __init__(self, cathFile, dataFolder):
        self.cathFile = cathFile
        self.dataFolder = dataFolder

        self.seq = []
        self.struc = []


    # Générateur (via un yield) permettant d'avoir tous les fichiers DSSP
    def getDSSPFile(self, cathFile, dataFolder):
        # Ouverture du fichier
        fichier = open(cathFile, 'r')

        for ligne in fichier:
            ligne = ligne.strip()
            infos = ligne.split(' ')
            if(len(infos) >= 1):
                nomData = infos[0]

                extract = nomData[-1]
                nomData = nomData[:-1]

                yield (dataFolder + "/" + nomData), extract

    
    # Permet de traiter le contenu d'un fichier DSSP
    def loadDSSPFile(self, nomFichier, extractType):
        print("Traitement du fichier: " + str(nomFichier))

        resSeq = ""
        resStruc = ""

        fichier = open(nomFichier + ".dssp", 'r')
        for ligne in fichier:
            # Suppression des espaces
            ligne = ligne.strip()
            
            # Si la ligne est vide ou que c'est un commentaire
            if(len(ligne) > 0 and ligne[0] != '#' and ligne[len(ligne)-1] != '.'):
                ligneData = ligne.split()
                
                # Index de la colonne que l'on va lire
                index = 1
                
                # On regarde si la valeur dans la colonne 1 est un nombre.  Si ce n'est pas le cas c'est qu'il
                # manque un espace.  On décalle donc toutes les colonnes
                if(not ligneData[index].isdigit()):
                    tmp = ligneData[index]
                    residu = tmp[len(tmp)-1]
                    index -= 1
                else:
                    residu = ligneData[index+1]
                
                # Si le résidu ne fait pas partie du résidu que l'on doit lire dans ce fichier 
                if(not (residu in extractType)):
                    # on passe au suivant
                    continue

                aa = ligneData[index+2]
                aa = aa.upper()
                
                # Vérification que la variable est bien un acide aminé
                if(aa not in getAllAA()):
                    continue
                
                structure = ligneData[index+3]
                structure = structure.upper()
                
                # On vérifie que la structure existe et si ce n'est pas le cas
                # On la définit comme étant vide (la conversion se fait ensuite comme définit précédemment)
                if(not structure in getAllStructure()):
                    structure = ' '
                structure = convertStructure(structure)
                
                # On enregistre la structure et l'acide aminé
                resSeq += aa
                resStruc += structure
        fichier.close()

        return resSeq, resStruc
        
    
    # Permet de créer un objet Prediction (qui permettra par la suite de faire des prédictions)
    def createPrediction(self, saveFile = ""):
        prediction = Prediction()
        # On parcourt tous les fichiers
        for nameFile, extract in self.getDSSPFile(self.cathFile, self.dataFolder):
            resSeq, resStruc = self.loadDSSPFile(nameFile, extract)
            prediction.addSeqAndStruc(resSeq, resStruc)
        
        # On sauvegarde si cela à été précisé précédemment
        if(saveFile != ""):
            prediction.saveInFile(saveFile)

        return prediction

    
    # Permet de charger une structure et sa séquence
    def loadStrucAndSeq(self, saveFile = ""):
        fichier = None
        if(saveFile != ""):
            fichier = open(saveFile, 'w')
        
        for nameFile, extract in self.getDSSPFile(self.cathFile, self.dataFolder):
            resSeq, resStruc = self.loadDSSPFile(nameFile, extract)

            self.seq.append(resSeq)
            self.struc.append(resStruc)
            if(fichier != None):
                fichier.write("> " + nameFile + " | " + extract)
                fichier.write("\n")
                fichier.write(str(resSeq))
                fichier.write("\n")
                fichier.write(str(resStruc))
                fichier.write("\n")
                
        if(fichier != None):
            fichier.close()
            
        return self.seq, self.struc
    
    def openSaveStrucAndSeq(self, savedFile):
        fichier = open(savedFile, 'r')
        for ligne in fichier:
            ligne = ligne.strip()
            
            if(len(ligne) > 0 and ligne[0] != '>'):
                if(len(self.seq) == len(self.struc)):
                    self.seq.append(ligne)
                else:
                    self.struc.append(ligne)


    def getAllSequence(self):
        return self.seq

    def getAllStructure(self):
        return self.struc


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
        self.valueResult = []
        listeStruc = list(getStructure())

        for colonne in self.matResult:
            self.result += listeStruc[colonne.index(max(colonne))]
            self.valueResult.append(max(colonne))


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

                res[struc] = total

        return res
    
                                    
    # Permet d'avoir le score qui nous a permit de déterminer que c'était la bonne structure
    def getValuePrediction(self, index):
        return self.valueResult[index]
    
    def getListPredictValue(self):
        res = []
        for i in range(len(self.valueResult)):
            res.append((self.valueResult[i], i))
        
        res = sorted(res, key=lambda x: x[1])
        return res
    
    
    def getTPR(self, structure):
        return self.tfpn[structure]['TP'] / (self.tfpn[structure]['TP'] + self.tfpn[structure]['FN'])
    
    def getFPR(self, structure):
        return self.tfpn[structure]['TN'] / (self.tfpn[structure]['TN'] + self.tfpn[structure]['FP'])




import matplotlib.pyplot as plt

class ROC:
    
    def __init__(self, bonneSeq, gor3):
        self.seq = gor3.getResult()
        self.bonneSeq = bonneSeq
        self.gor3 = gor3
    
    
    def getCoord(self):
        P = 0
        N = 0
        for j in range(len(self.seq)):
            if self.seq[j] == self.bonneSeq[j]:
                P += 1
            else:
                N += 1
        
        LD = self.gor3.getListPredictValue()
        
        FP = 0
        TP = 0
        
        resX = []
        resY = []
        
        valuePrecedent = None
        i = 0
        
        while i < len(self.seq):
            valuePrediction = self.gor3.getValuePrediction(i)
            if valuePrediction != valuePrecedent:
                resX.append(FP/N)
                resY.append(TP/P)
                valuePrecedent = valuePrediction
            
            # si prediction[L_d[i].position] == structure[L_d[i].position]
            nextPos = LD[i][1]
            if(self.seq[nextPos] == self.bonneSeq[nextPos]):
                TP += 1
            else:
                FP += 1
            
            i+=1
            
        resX.append(FP/N)
        resY.append(TP/P)
        
        return resX, resY
    
    def draw(self):
        listX, listY = self.getCoord()
        
        listX.sort()
        listY.sort()

        plt.plot(listX, listY)

        plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])


        #plt.yscale('log')
        plt.title("Courbe ROC")
        plt.grid(True)
        plt.show()
        

class ROC2:
    
    def __init__(self, bonneSeq, seq, freq):
        self.seq = seq
        self.bonneSeq = bonneSeq
        self.freq = freq
    
    
    def getCoord(self):
        P = 0
        N = 0
        for j in range(len(self.seq)):
            if self.seq[j] == self.bonneSeq[j]:
                P += 1
            else:
                N += 1
        
        LD = []
        for i in range(len(self.freq)):
            LD.append((self.freq[i], i))
        
        LD = sorted(LD, key=lambda x: x[1])
        
        FP = 0
        TP = 0
        
        resX = []
        resY = []
        
        valuePrecedent = None
        i = 0
        
        while i < len(self.seq):
            valuePrediction = self.freq[i]
            if valuePrediction != valuePrecedent:
                resX.append(FP/N)
                resY.append(TP/P)
                valuePrecedent = valuePrediction
            
            # si prediction[L_d[i].position] == structure[L_d[i].position]
            nextPos = LD[i][1]
            if(self.seq[nextPos] == self.bonneSeq[nextPos]):
                TP += 1
            else:
                FP += 1
            
            i+=1
            
        resX.append(FP/N)
        resY.append(TP/P)
        
        return resX, resY
    
    def draw(self):
        listX, listY = self.getCoord()
        
        listX.sort()
        listY.sort()

        plt.plot(listX, listY)

        plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])


        #plt.yscale('log')
        plt.title("Courbe ROC")
        plt.grid(True)
        plt.show()
        

    
# On va récupérer les informations
# parser = Parser("./DATA/CATH_info.txt", "./DATA/dssp")
# On créé le prédicteur
# prediction = parser.createPrediction("bdd.txt")
prediction = Prediction()
prediction.loadSaveFile("bdd.txt")

# On récupère les fichiers de tests
parserTest = Parser("./DATA/CATH_info_test.txt", "./DATA/dssp_test")
allSeq, allStruc = parserTest.loadStrucAndSeq("test.txt")



testSeqUn = allSeq[0]
testStrucUn = allStruc[0]

gor3_1 = GOR3(prediction, testSeqUn)
print("Prédiction: " + str(gor3_1.getResult()))
print("Données:    " + "".join(testStrucUn))


print("Pourcent: Q3: " + str(gor3_1.calculQ3(testStrucUn)*100) + "%")

roc = ROC2("CCCTTTCCTTCCCCHHHHHHHHHHHHHHCTTTEEEEEEEECTTCCEEEEEEECCCCCCCCEEEEEECCCTTCHHHHHHHHHHHHHHHHHTTTCHHHHHHHHHCEEEEECCCCHHHHHHHHHTCTTCCCCCCCCCCCCCCCCCHHHCCCCCTTCCCCECCTTCTTECCCCTTCCHHHHHHHHHHHHHCCEEEEEEEEECCCEEEECCCCCCCCCTTHHHHHHHHHHHHHHHHHHHCCCCEEEEHHHHCCCCCCCHHHHHHHTTCCEEEEEEECCCCCCHHHCCHHHHHHHHHHHHHHHHHHHHHHHHC", 
    "CCCTTTCTTTTTCTTHHTCHHTHTTTTTCTTTTEETTTEEETTEEETTTEETCCCCCCCEETETEECTCTTCTTHTTHHTTTTHHTHTHTTTHHHTHTTTEHCETETETTHCHHHTTTTHHTCTTCTCCTCCCCCCCCCCCCCHHHCCCTTTCTTTEEETTETTCCCCCTTHCTCTHHTTHTTEHHCCTEETEETEECECEEECCCCCHHCCCTTHHTTHTTTHHTTTTTEHTCECECECEETTHHTCCCHCCHTHHETHTTTCTETTTEECCEHCCHTTTHTHTTTHHTTTHHTHTTHTTTHHTHH", 
    [19.007570045594424, 19.171175440110495, 17.939009439480014, 22.805843849246184, 18.363916240232403, 24.806423001527207, 25.36026871178199, 20.135694339946085, 28.280267714758757, 35.152124234821265, 27.80729172994874, 24.64968889269695, 23.680795021599945, 27.80729172994874, 23.647476536618257, 23.362416731556298, 18.303440665285624, 27.287352838422986, 19.249379158330072, 23.362416731556298, 22.135721299101466, 22.433612867966197, 23.01023421344494, 30.974501477448563, 30.974501477448563, 24.57285709220357, 21.615584279448324, 18.778183764386256, 23.114192564192845, 28.454208513362367, 26.238281208383107, 27.53013295273683, 24.129159592970858, 20.69301168018497, 27.653405321077912, 30.974501477448563, 26.238281208383107, 27.684802739961423, 23.12100637433541, 20.31640972621998, 20.69301168018497, 28.280267714758757, 32.82036380521271, 23.12100637433541, 20.31640972621998, 33.22917574527223, 27.838260307303564, 28.280267714758757, 27.25670385483538, 24.731086117511012, 27.85213027184713, 22.553679488271563, 20.906194854301198, 21.700396488608433, 20.489905690527998, 20.489905690527998, 20.554012336189835, 20.920675483094932, 25.150591833914813, 19.676940801372766, 29.1368012284696, 24.29014234505347, 23.574796743106887, 24.50667770247183, 31.338358275311016, 25.419756165207218, 21.780635729552166, 22.301521794617198, 23.114192564192845, 32.281991843016826, 33.38984066573628, 27.14426278595687, 21.88662886331275, 25.1722239513209, 24.287498973416604, 20.013071205313956, 21.865461752664924, 24.287498973416604, 29.28081212112437, 26.751063769381872, 20.983538876320807, 22.604832010718944, 20.96237176567298, 19.798662661322382, 19.798662661322382, 22.803556961488162, 23.986468977752622, 19.466853812082462, 16.109178004886907, 35.40856770481985, 24.197063291776487, 32.463491211452265, 16.109178004886907, 27.50642495225831, 23.300063535683385, 22.569374476798078, 24.873863976218047, 21.26340176133696, 24.068293595437115, 20.428417293632386, 20.956031615476792, 24.00442857190611, 25.626938229046754, 24.56224080336129, 22.192015488501287, 22.489110793572962, 20.65557943544674, 29.449404518458223, 24.95568859390254, 27.807611323715964, 17.76125897468347, 21.471582951975513, 27.154242434146948, 22.180930440613913, 28.025539616021064, 23.507921997710888, 22.166491748328905, 23.507921997710888, 18.365137902016343, 21.320474097544295, 22.800308589250186, 32.66221616222148, 21.47158295197551, 26.61372319378655, 37.949343900167506, 26.655632400933065, 26.61372319378655, 26.801815947328166, 24.233575190528583, 26.61372319378655, 23.013404823949067, 29.305259808613936, 23.791911469729783, 22.661222305837704, 23.013404823949067, 22.661222305837704, 29.31717793825931, 20.317771738540806, 28.930443598789036, 22.347238186959263, 28.61658976091773, 22.25964631241542, 20.317771738540806, 17.654870512556425, 20.335793791979896, 17.654870512556425, 27.497760015971416, 22.932621371585107, 20.317771738540806, 17.61967077059598, 37.89639941762839, 17.61967077059598, 26.558877177298587, 28.039519233286697, 17.61967077059598, 28.039519233286697, 20.69301168018497, 20.69301168018497, 20.69301168018497, 29.908205969234892, 28.039519233286697, 20.69301168018497, 33.90648375444735, 36.26465043927405, 19.249379158330072, 23.466375082304207, 21.995055668847904, 25.47275722806394, 19.249379158330072, 35.718726692228365, 27.854587029911734, 16.927281104292405, 20.7203278321185, 27.529215019765516, 20.7203278321185, 26.302461345396054, 20.686057659787807, 16.927281104292405, 26.797407741496, 26.501186296165272, 23.874995520196826, 17.76262275599188, 26.978307550884935, 21.428195318008765, 23.38505042326984, 22.575746602647605, 21.796330718078686, 21.823765470086872, 18.77839938420711, 21.428195318008765, 28.938076277700382, 22.604832010718944, 25.032116113174993, 20.69301168018497, 26.950865308838143, 27.289612172483572, 20.69301168018497, 19.249379158330072, 20.69301168018497, 27.822343329205918, 27.123631094296343, 26.799967406918825, 26.601242456149606, 19.249379158330072, 19.444056233846094, 19.249379158330072, 22.699420705070626, 19.249379158330072, 17.76125897468347, 17.76125897468347, 26.246278283044287, 21.70697979639838, 28.06430211944869, 27.76553846566616, 29.171640351481972, 19.293022575868875, 17.76125897468347, 19.313396244740318, 24.397108956268056, 24.430987984506153, 19.12567620684853, 26.817911280355773, 20.110434301128414, 21.21433143695485, 25.244006088482898, 19.75825178301705, 25.91482129336383, 20.309159251897633, 19.75825178301705, 22.305593975146706, 21.428195318008765, 16.927281104292405, 22.44335655396233, 15.442329601553732, 23.12100637433541, 23.858758980703684, 16.903772530057772, 15.350814620432383, 21.428195318008765, 15.294004508064166, 23.12100637433541, 20.69301168018497, 22.082281633285902, 22.082281633285906, 26.49112884893893, 26.49112884893893, 21.936153597607664, 19.249379158330072, 27.485855799621067, 29.022136774763528, 16.927281104292405, 22.29608566451188, 22.097360713742667, 16.927281104292405, 22.742514489936973, 23.788385463828583, 21.174395625858587, 17.047802786581393, 16.713093510529347, 24.981895453386734, 33.36658119844421, 24.395788242545706, 25.1722239513209, 24.217484722960634, 19.28181138605907, 20.69301168018497, 23.155739479599525, 18.365137902016343, 22.803556961488162, 29.801587036569586, 25.435451153733737, 26.15598686580152, 22.3107988348628, 17.399349060600557, 22.152512131063276, 25.803804347690157, 26.025496630279804, 22.152512131063276, 22.553679488271563, 21.088650150283456, 21.088650150283456, 20.730307480308582, 21.1610967164422, 23.50467362547291, 19.359858691538612, 27.735955262408805, 27.185047793528224, 20.730307480308582, 24.63968149152797, 21.1610967164422, 19.161133740769394, 18.56376382509052, 25.014497701352866, 20.822213107747224, 24.24953652794622, 29.26511713259785, 26.817911280355773, 24.24953652794622, 24.81577275058365, 26.387399946973517, 20.986806792865785, 17.919499595574624, 19.25541075921125, 19.989155499484404, 21.989927063020666, 14.726488003309901, 14.308147644846112])
roc.draw()



