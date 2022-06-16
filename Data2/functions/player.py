import pandas as pd
import joblib
import os

def findRank(rank):
    if rank >= 10 and rank < 20:
        coll = "herald"
    if rank >= 20 and rank < 30:
        coll = "guardian"
    if rank >= 30 and rank < 40:
        coll = "crusader"
    if rank >= 40 and rank < 50:
        coll = "archon"
    if rank >= 50 and rank < 60:
        coll = "legend"
    if rank >= 60 and rank < 70:
        coll = "ancient"
    if rank >= 70 and rank < 80:
        coll = "divine"
    if rank == 80:
        coll = "immortal"
    return coll

def findCore(scaledX, laneRole, loaded_model):
    y = loaded_model.predict(scaledX)
    if y == 1:
        if laneRole == 1:
            return 1
        elif laneRole == 2:
            return 2
        elif laneRole == 3:
            return 3
    else:
        if laneRole == 1:
            return 5
        elif laneRole == 2:
            return 4
        elif laneRole == 3:
            return 4

def findRole(player, medal):
    rank = findRank(medal)
    cwd = os.getcwd()  # Get the current working directory (cwd)
    loaded_scaler = joblib.load(f"{cwd}/model/models/{rank}/core_scaler.sav")
    loaded_model = joblib.load(f"{cwd}/model/models/{rank}/core_model.sav")
    X = [[player['last_hits'], player['obs_placed'], player['gpm']]]
    df = pd.DataFrame(X)
    scaledX = loaded_scaler.transform(df)
    role = findCore(scaledX, player['lane_role'], loaded_model)
    return role


#testing legend role model
#print(findRole({"last_hits": 500, "obs_placed":5, "gpm": 300, "lane_role": 3}, 80))