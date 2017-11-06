from Score import Score
from Sequence import Sequence
from Align import Align


def chargerFichierSequence(nom_fichier):
    res = [] # Liste où seront stocké les séquences

    # Ouverture du fichier
    fichier = open(nom_fichier, 'r')

    nomSequence = "" # Nom de la séquence
    debut = -1       # Index de début de séquence
    fin = -1         # Index de fin de séquence
    sequence = ""    # La séquence en elle-même

    # On lit chaque ligne du fichier
    for ligne in fichier:
        ligne = ligne.strip() # Supprime les espaces inutiles
        if(ligne[0] == '>'): # début d'une séquence

            if(sequence != ""): # Si la séquence n'est pas vide
                # On enregistre
                res.append(Sequence(sequence, nomSequence, debut, fin))
                # On remet tout à zero
                nomSequence = ""
                debut = -1
                fin = -1
                sequence = ""

            # On extrait les informations
            infos = ligne.split('|')
            if(len(infos) == 3):
                nomSequence = infos[1]
                debutFin = infos[2].split("-")

                if(len(debutFin) == 2):
                    debut = debutFin[0]
                    fin = debutFin[1]
                    
            else: # Si on a pas toutes les informations on informe qu'il y a une erreur
                raise SyntaxError("Fichier invalide (debug ligne: %s )" % ligne)

        else: # Suite d'une séquence
            sequence += ligne.strip()

    # On oublies pas la dernière séquence (qui n'a aucune autre séquence après elle)
    if(sequence != ""): 
        res.append(Sequence(sequence, nomSequence, debut, fin))

    return res


##### TEST 1 #####
# print("----------- ORIGINAL -----------")
# listSeq = chargerFichierSequence("seqTest.fasta")

# seq0_0 = listSeq[0]
# seq0_1 = listSeq[1]
# print(seq0_0.getNom() + ": " + str(seq0_0) + " (taille: " + str(len(seq0_0)) + ")")
# print(seq0_1.getNom() + ": " + str(seq0_1) + " (taille: " + str(len(seq0_1)) + ")")
# print("")

# blosum60 = Score("./Mat_Substitution/blosum62.iij")
# align = Align(seq0_0, seq0_1, blosum60, -12, -2)
# align.printResult()
# print("")


##### TEST 1 #####
# print("----------- SH3 40% -----------")
# listSeq2 = chargerFichierSequence("seqTest.fasta")

# seq0_0 = listSeq[0]
# seq0_1 = listSeq[1]
# print(seq0_0.getNom() + ": " + str(seq0_0) + " (taille: " + str(len(seq0_0)) + ")")
# print(seq0_1.getNom() + ": " + str(seq0_1) + " (taille: " + str(len(seq0_1)) + ")")
# print("")


# sh3_40 = Score("./Mat_Substitution/sh40.iij")
# align2 = Align(seq0_0, seq0_1, sh3_40, -12, -2)
# align2.printResult()
# print("")


##### TEST 2 #####
print("----------- SH3 70% -----------")
listSeq1 = chargerFichierSequence("SH3-sequence.fasta")

seq1_0 = listSeq1[0]
seq1_1 = listSeq1[1]
print(seq1_0.getNom() + ": " + str(seq1_0) + " (taille: " + str(len(seq1_0)) + ")")
print(seq1_1.getNom() + ": " + str(seq1_1) + " (taille: " + str(len(seq1_1)) + ")")
print("")

sh3_40 = Score("./Mat_Substitution/sh40.iij")
sh3_70 = Score("./Mat_Substitution/SH3_70.iij")
blosum62 = Score("./Mat_Substitution/blosum62.iij")
align1 = Align(seq1_0, seq1_1, blosum62, -12, -2, True)
align1.printResult()
print("")


# ##### TEST 3 #####
# listSeq2 = chargerFichierSequence("SH3-sequence.fasta")

# seq2_0 = listSeq2[0]
# seq2_1 = listSeq2[1]
# print(seq2_0.getNom() + ": " + str(seq2_0) + " (taille: " + str(len(seq2_0)) + ")")
# print(seq2_1.getNom() + ": " + str(seq2_1) + " (taille: " + str(len(seq2_1)) + ")")
# print("")

# blosum50 = Score("./Mat_Substitution/blosum62.iij")
# align2 = Align(seq2_0, seq2_1, blosum50, -8, -2, True)
# align2.printResult()
# print("")

