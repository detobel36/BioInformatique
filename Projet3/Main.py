from Profil import Profil
from Align import Align


def importSeq(nom_fichier):

    # Ouverture du fichier
    fichier = open(nom_fichier, 'r')

    listeSeq = []
    currentSeq = ""

    for ligne in fichier:
        ligne = ligne.strip()

        if(len(ligne) > 0):
            if(ligne[0] == '>'):
                if(currentSeq != ""):
                    listeSeq.append(currentSeq)

                currentSeq = ""
            else:
                currentSeq += ligne

    if(currentSeq != ""):
        listeSeq.append(currentSeq)

    return listeSeq


def print_solution(solution):
    col = 1
    for colonne in solution:
        print("Colonne : " + str(col))
        for lettre in colonne:
            print(lettre + " : " + str(colonne[lettre]))
        col += 1

# Permet d'afficher une matrice
def printMatrice(matrice):
    for i in range(len(matrice)):
        # Ligne avec les indices
        if(i == 0):
            print("     ", end="")
            for j in range(len(matrice[i])):
                print('{:4}|'.format(j), end="")
            print()
        
        # Affichage des lignes
        for j in range(len(matrice[i])):
            if(j == 0):
                # Affiche l'indice
                print('{:4}|'.format(i), end="")

            if(isinstance(matrice[i][j], list)):
                print('{:4}|'.format("".join(matrice[i][j])), end="")
            else:
                print('{:4}|'.format(str(matrice[i][j])), end="")
        print() # Retour à la ligne



print("MUSCLE")
profil = Profil(importSeq("msaresults-MUSCLE.fasta"), -0.2)

sequence = importSeq("test.fasta")
# print(sequence[0])

# print("---------- PSSM ----------")
# print_solution(profil.getPSSM())


align = Align(sequence[0], profil.getPSSM())
align.printResult()


print("")
print("")
print("")

align = Align(sequence[1], profil.getPSSM())
align.printResult()



# print("ClustalOmega")
# profil2 = Profil(importSeq("msaresults-omega.fasta"))
# print_solution(profil2.getPSSM())
