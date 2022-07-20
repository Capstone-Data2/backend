import joblib
import os

#player = [[3, 1, 10, 565, 683, 1992, 334, 7898, 0, 0]] # kills, deaths, assists, gpm, xpm, duration, last hits, hero damage
#player = [[6, 1, 9, 801, 917, 1992, 460, 20911]] # kills, deaths, assists, gpm, xpm, duration, last hits, hero damage
player = [[3, 2, 6, 345, 465, 1724, 132, 11543, 4]] # kills, deaths, assists, gpm, xpm, duration, last hits, hero damage
cwd = os.getcwd()  # Get the current working directory (cwd)

def predictModel(rank, pos, player):
    win_model = joblib.load(f'{cwd}/models/{rank}/pos{pos}_win.sav')
    y = win_model.predict_proba(player)
    return(y[0][1])


print(predictModel('herald', 2, player))
