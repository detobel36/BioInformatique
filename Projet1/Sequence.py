class Sequence:

    # Creation de l'objet
    def __init__(self, sequence = [], seqNom = "", debut = -1, fin = -1):
        self.sequence = list(sequence)
        self.debut = debut
        self.fin = fin
        self.nom = seqNom

    # Recuperer sa longueur
    def __len__(self):
        return len(self.sequence)

    # Recuperer un element a un indice specific
    def __getitem__(self, item):
        return self.sequence[item]

    # Permet de definir un element a un indice specific
    # Une sequence ne sera jamais modifiee (dans ce programme)
    # def __setitem__(self, key, item):
    #     self.sequence[key] = item

    # Transformer la sequence en string
    def __str__(self):
        res = ""
        for lettre in self.sequence:
            res += lettre;
        return res

    # Permet d'avoir l'indice de debut de la sequence
    def getDebut(self):
        return self.debut

    # Permet d'avoir l'indice de fin de la sequence
    def getFin(self):
        return self.fin

    # Permet d'avoir le nom de la sequence
    def getNom(self):
        return self.nom

    # Permet de comparer la sequence actuelle avec une autre
    def isEgal(self, sequence):
        egal = True
        i = 0

        if(len(self.sequence) != len(sequence)):
            egal = False

        while(egal and i < len(self.sequence)):
            egal = (sequence[i] == self.sequence[i])
            i+=1
            
        return egal
        

