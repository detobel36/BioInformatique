import sys
# Add folder path to the path list (sys.path)
sys.path.append('../')

from Score import Score


# =-=-=-=-=-=-=-=-= TEST =-=-=-=-=-=-=-=-= #
def testScore():
    score1 = Score("../Mat_Substitution/blosum30.iij")

    print("AA: " + score1.get("A", "A"))
    print("AN: " + score1.get("A", "N"))
    
    
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
