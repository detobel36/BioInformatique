import sys
# Add folder path to the path list (sys.path)
sys.path.append('../')

from Sequence import Sequence


# =-=-=-=-=-=-=-=-= TEST =-=-=-=-=-=-=-=-= #
seq1 = Sequence("ABC")
seq2 = Sequence("BAC")
seq3 = Sequence("ABC")
# 
print(str(seq1) + " != " + str(seq2) + ":")
if(seq1.isEquals(seq2)):
    print("Equals")
else:
    print("NotEquals")

print("")

print(str(seq1) + " = " + str(seq3) + ":")
if(seq1.isEquals(seq3)):
    print("Equals")
else:
    print("NotEquals")


print("2eme element " + seq1[2])
seq1[2] = "D"
print("2eme element " + seq1[2])

print("Seq1 " + str(seq1))


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
