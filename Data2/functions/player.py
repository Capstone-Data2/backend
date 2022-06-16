import pandas as pd
import joblib

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
    loaded_scaler = joblib.load(f"../model/models/{rank}/core_scaler.sav")
    loaded_model = joblib.load(f"../model/models/{rank}/core_model.sav")
    X = [[player['last_hits'], player['obs_placed'], player['gpm']]]
    df = pd.DataFrame(X)
    scaledX = loaded_scaler.transform(df)
    role = findCore(scaledX, player['lane_role'], loaded_model)
    return role

#testing legend role model
#print(findRole({"last_hits": 500, "obs_placed":5, "gpm": 300, "lane_role": 3}, 80))

def lowestGPMFiveMin(gold_array):
  goldIntervals = []
  if len(gold_array) < 15:
    return 0
  for x in range(10, len(gold_array)):
    if((x+5)<len(gold_array)):
      goldForFiveMin = gold_array[x+5] - gold_array[x]
      goldIntervals.append(goldForFiveMin)
  
  min = 10000
  min_count = 0
  count = 10
  for interval in goldIntervals:
    if interval < min:
      min = interval
      min_count = count
    count = count+ 1
  return (min/5, min_count)

def killParticipation(radiant, dire_score, radiant_score, kills, assists):
  if radiant:
    return (kills+assists)/radiant_score
  else:
    return (kills+assists)/dire_score

def killsPerMinTen(kills_log):
  kill_count = 0
  for kill in kills_log:
    if kill['time'] < 600:
      kill_count = kill_count + 1
  
  if kill_count == 0:
    return 0
  else:
    return kill_count/10

def perMin(num, duration):
  return(num / (duration/60))

def percentageGoldGained(gold_gained):
  total_avaiable = (((3 * 34 + 43) * 10 * 2) - 1) + 59 #Gold from creepwaves -1 for the last round that the wave spawns on +59 siege creep
  total_avaiable = total_avaiable + (100*5) + (106*5) #Passive gold calculation
  total_avaiable = total_avaiable + 80 + (36 * 2) + 45 #Runes that are avaible for one team before 10 min
  return gold_gained/total_avaiable

