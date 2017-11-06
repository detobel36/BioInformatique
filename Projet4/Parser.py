from Utils import *
from Prediction import Prediction

class Parser:
    
    # On indique au parser le fichier cath qu'il va utiliser ainsi que le dossier 
    # où se touvent les fichiers DSSP
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
            ligneNoStrip = ligne
            ligne = ligne.strip()
            
            # Si la ligne est vide ou que c'est un commentaire
            if(len(ligne) > 0 and ligne[0] != '#' and ligne[len(ligne)-1] != '.'):
                ligneData = ligne.split()
                
                # Index de la colonne que l'on va lire
                index = 1
                
                # On regarde si la valeur dans la colonne 1 est un nombre.  Si ce n'est pas le cas c'est qu'il
                # manque un espace.  On décalle donc toutes les colonnes
                if(not ligneData[index].lstrip('-').isdigit()):
                    tmp = ligneData[index]
                    residu = tmp[len(tmp)-1]
                    index -= 1
                else:
                    residu = ligneData[index+1]
                
                residu = residu.upper()
                

                # Si le résidu ne fait pas partie du résidu que l'on doit lire dans ce fichier 
                if(not (residu in extractType)):
                    # on passe au suivant
                    continue

                aa = ligneData[index+2]
                aa = aa.upper()
                
                if(aa != (ligneNoStrip[13]).upper()):
                    print(ligneNoStrip)
                    print(ligneNoStrip[13])
                    print(aa)
                    return

                # Vérification que la variable est bien un acide aminé
                if(aa not in getAllAA()):
                    continue
                
                structure = ligneData[index+3]
                structure = structure.upper()
                
                # On vérifie que la structure existe et si ce n'est pas le cas
                # On la définit comme étant vide (la conversion se fait ensuite comme définie précédemment)
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
            
        
        # On sauvegarde si cela a été précisé précédemment
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