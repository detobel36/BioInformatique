
from Bloc import Bloc
from Score import Score


def importBloc(nom_fichier, proportion = 0.5):

    # Ouverture du fichier
    fichier = open(nom_fichier, 'r')

    listBloc = []


    i = 0
    seq = 0

    for ligne in fichier:
        ligne = ligne.strip()

        if(ligne[0] == '>'):
            i = 0
            seq += 1

        else:
            if(seq == 1):
                listBloc.append([ligne])
            else:
                if(len(listBloc) > i):
                    listBloc[i].append(ligne)
                else:
                    raise SyntaxError("Erreur de taille dans la" \
                        " liste: %d | i: %d" % (len(listBloc), i))
            i += 1

    return Score([Bloc(seq, proportion) for seq in listBloc])
    


# testBloc = importBloc("TEST.fasta")
# testBloc.printResMatrice()

print("\n\nSH3 avec 70% \d'identité")
sh3Bloc70 = importBloc("SH3.fasta", 0.7)
sh3Bloc70.printResMatrice()

# sh3Bloc62 = importBloc("SH3.fasta", 0.62)
# sh3Bloc62.printResMatrice()


print("\n\nSH3 avec 40% \d'identité")
sh3Bloc30 = importBloc("SH3.fasta", 0.4)
sh3Bloc30.printResMatrice()


# print("-----------")

print("PDZ avec 40% \d'identité")
pdzBloc = importBloc("PDZ.fasta", 0.4)
pdzBloc.printResMatrice()

print("PDZ avec 70% \d'identité")
pdzBloc70 = importBloc("PDZ.fasta", 0.7)
pdzBloc70.printResMatrice()