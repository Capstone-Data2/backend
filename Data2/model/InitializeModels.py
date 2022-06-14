from modelCreator import posModel


def createAllModels():
    for x in range(1, 6):
        posModel('herald', x)
        posModel('guardian', x)
        posModel('crusader', x)
        posModel('archon', x)
        posModel('legend', x)
        posModel('ancient', x)
        posModel('divine', x)
        posModel('immortal', x)

#createAllModels()