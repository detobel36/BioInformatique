# -*- coding:Utf8 -*-
CONVERT_L_STRUCTURE = {'H':'H', 'G':'H', 'I':'H', # H,G,I -> H
                'E':'E', 'B':'E',                 # E,B -> E
                'T':'T',                          # T -> T
                'C':'C', 'S':'C', ' ':'C'}        # C,S,' ' -> C

def getStructure():
    return set(CONVERT_L_STRUCTURE.values())

def getAllStructure():
    return list(CONVERT_L_STRUCTURE.keys())


def increment(dictionnaire, niveau1, niveau2):
    if(niveau1 in dictionnaire):
        if(niveau2 in dictionnaire[niveau1]):
            dictionnaire[niveau1][niveau2] += 1
        else:
            dictionnaire[niveau1][niveau2] = 1
    else:
        dictionnaire[niveau1] = {niveau2: 1}
    return dictionnaire



# def calculTFandPN(result, correctStruc):
#     tfpn = {}
#     for index in range(len(result)):
#         corrStruc = correctStruc[index]
#         prediStruc = result[index]
#         if(corrStruc == prediStruc):
#             tfpn = increment(tfpn, corrStruc, 'TP')
#             for struc in getStructure():
#                 if(struc != corrStruc):
#                     tfpn = increment(tfpn, struc, 'TN')
#         else:
#             for struc in getStructure():
#                 if(struc == prediStruc):
#                     tfpn = increment(tfpn, prediStruc, 'FP')
#                 else:
#                     tfpn = increment(tfpn, prediStruc, 'FN')
#                     print("INdex: " + str(index) + " corrStruc: " + str(corrStruc) + " prediStruc:" + str(prediStruc))
#     return tfpn


def calculTFandPN(seqPredi, correctStruc):
    tfpn = {}
    for index in range(len(seqPredi)):
        corrStruc = correctStruc[index]
        prediStruc = seqPredi[index]

        value = "T" if corrStruc == prediStruc else "F"

        for struc in getStructure():
            # res = value + ("P" if struc == prediStruc else "N")

            if(struc == prediStruc):
                res = value + "P"
            elif(struc == corrStruc):
                res = value + "N"
            elif(value == "T"):
                res = value + "N"
            else:
                continue

            tfpn = increment(tfpn, struc, res)

    return tfpn



print(calculTFandPN('CHHHCCCCEEEECCCEEECCCHHHHC', 'HHHHHCCCCEEEECCCEEECCCHHHH'))