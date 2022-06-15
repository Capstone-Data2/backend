from modelCreator import posModel, coreModel
import sys
sys.path.append('../functions/')
from player import findRole


def createAllWinModels():
    for x in range(1, 6):
        posModel('herald', x)
        posModel('guardian', x)
        posModel('crusader', x)
        posModel('archon', x)
        posModel('legend', x)
        posModel('ancient', x)
        posModel('divine', x)
        posModel('immortal', x)

def createAllCoreModels():
    ranks = ['herald', 'guardian', 'crusader', 'archon', 'legend', 'ancient', 'divine', 'immortal']
    loop = True
    count = 1
    while loop:
        if count < 8:
            coreModel(ranks[count-1])
            role = findRole({"last_hits": 500, "obs_placed":0, "gpm": 600, "lane_role": 1}, count*10)
            if role == 1:
                count += 1
                print(role, ranks[count-1])
        else:
            loop = False

#createAllModels()
#createAllCoreModels()
