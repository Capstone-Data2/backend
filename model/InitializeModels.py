from modelCreator import posModel, coreModel
import sys
sys.path.append('../functions/')
from player import findRole

ranks = ['herald', 'guardian', 'crusader', 'archon', 'legend', 'ancient', 'divine', 'immortal', 'pro']
positions = [1, 2, 3, 4, 5]

def createAllModels():
    for rank in ranks:
        for position in positions:
            posModel(rank, position)
            
def createAllCoreModels():
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