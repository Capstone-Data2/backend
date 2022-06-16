import joblib
import os
player = [[8, 2, 11, 600, 500, 1800, 300, 10000]]

cwd = os.getcwd()  # Get the current working directory (cwd)

def predictModel(rank, pos, player):
    win_model = joblib.load(f'{cwd}/model/models/{rank}/pos{pos}_win.sav')
    y = win_model.predict_proba(player)
    return(y[0][1])


#print(predictModel('herald', 1, player))