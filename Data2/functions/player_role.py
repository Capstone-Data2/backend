import pandas as pd
import joblib

loaded_model = joblib.load("models/core_model.sav")
loaded_scaler = joblib.load("models/core_scaler.sav")


def findCore(scaledX, laneRole):
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

def findRole(player):
    X = [[player['last_hits'], player['obs_placed'], player['gpm']]]
    df = pd.DataFrame(X)
    scaledX = loaded_scaler.transform(df)
    role = findCore(scaledX, player['lane_role'])
    player['ml_lane_role'] = role


