import joblib

player = [[8, 2, 11, 600, 500, 1800, 300, 10000]]


def predictModel(rank, pos, player):
    win_model = joblib.load(f'backend/data2/model/models/{rank}/pos{pos}_win.sav')
    y = win_model.predict_proba(player)
    return(y[0][1])


print(predictModel('herald', 1, player))