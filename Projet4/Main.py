from Prediction import Prediction
from Parser import Parser
from GOR3 import GOR3


parser = Parser("DATA/CATH_info.txt", "DATA/dssp")
# parser.loadStrucAndSeq("bdd.txt")
prediction = parser.createPrediction()

# prediction = Prediction()
# prediction.loadSaveFile("prediction.txt")
# prediction.getDimension()

# parserTest = Parser("DATA/CATH_info_test.txt", "DATA/dssp_test")
# allSeq, allStruc = parserTest.loadStrucAndSeq("test.txt")


# for index in range(len(allSeq)):
#     seq = allSeq[index]
#     struc = allStruc[index]

#     gor3 = GOR3(prediction, seq)
#     print("Prédiction: " + str(gor3.getResult()))
#     print("Donnée:     " + "".join(struc))
#     print("Pourcent: Q3: " + str(gor3.calculQ3(struc)*100) + "%")
#     print("Pourcent: MCC: " + str(gor3.calculMCC(struc)*100) + "%")
#     print("")
#     print("")


