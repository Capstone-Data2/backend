from modelCreator import posModel

ranks = ['herald', 'guardian', 'crusader', 'archon', 'legend', 'ancient', 'divine', 'immortal']
positions = [1, 2, 3, 4, 5]


def createAllModels():
    for rank in ranks:
        for position in positions:
            posModel(rank, position)

createAllModels()