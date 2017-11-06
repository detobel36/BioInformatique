# -*- coding:Utf8 -*-
CONVERT_L_STRUCTURE = {'H':'H', 'G':'H', 'I':'H', # H,G,I -> H
                'E':'E', 'B':'E',                 # E,B -> E
                'T':'T',                          # T -> T
                'C':'C', 'S':'C', ' ':'C'}        # C,S,' ' -> C

def getStructure():
    return set(CONVERT_L_STRUCTURE.values())

def getAllStructure():
    return list(CONVERT_L_STRUCTURE.keys())


def getAllAA():
    return ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']


def convertStructure(lettreStructure):
    return CONVERT_L_STRUCTURE[lettreStructure]
