import pandas as pd
import joblib
import os
from model.predictModel import predictModel
from model.positionFeatures import positionFiller
from collections import Counter
from utils import get_db_handle

db, client = get_db_handle()

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
    if rank >= 80:
        coll = "immortal"
    if rank >= 80:
        coll = "immortal"
    return coll

def findCore(scaledX, laneRole, loaded_model):
    y = loaded_model.predict(scaledX)
    if laneRole != None:
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
    else:
      return 4

def findRole(player, rank):
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
  return(round(num / (duration/60), 2))

def percentageGoldGained(gold_gained):
  total_avaiable = (((3 * 34 + 43) * 10 * 2) - 1) + 59 #Gold from creepwaves -1 for the last round that the wave spawns on +59 siege creep
  total_avaiable = total_avaiable + (100*5) + (106*5) #Passive gold calculation
  total_avaiable = total_avaiable + 80 + (36 * 2) + 45 #Runes that are avaible for one team before 10 min
  return gold_gained/total_avaiable


def rivalResponse(player, rank):
  player_resp = common(player, rank)
  if player['ml_lane_role'] >= 1 and player['ml_lane_role'] <= 3:
    player_resp.update(commonCore(player))
    if player['ml_lane_role'] == 1:
      player_resp.update(pos1Rival(player))
    elif player['ml_lane_role'] == 2:
      player_resp.update(pos2Rival(player))
    elif player['ml_lane_role'] == 3:
      player_resp.update(pos3Rival(player))
  elif player['ml_lane_role'] >= 4 and player['ml_lane_role'] <= 5:
    player_resp.update(commonSup(player))
    if player['ml_lane_role'] == 4:
      player_resp.update(pos4Rival(player))
    elif player['ml_lane_role'] == 5:
      player_resp.update(pos5Rival(player))
  
  return player_resp
        

def common(player, rank):
  all_items = [
    player['item_0'],
    player['item_1'],
    player['item_2'],
    player['item_3'],
    player['item_4'],
    player['item_5'],
    player['item_neutral'],
    player['backpack_0'], player['backpack_1'],
    player['backpack_2']
  ]
  player_resp = {
    "hero_id": player['hero_id'],
    "ml_lane_role": player['ml_lane_role'],
    "items": all_items,
    "level": player['level'],
    "net_worth": player['net_worth'],
    "kills": player['kills'],
    "assists": player['assists'],
    "deaths": player['deaths'],
    "hero_damage": player['hero_damage'],
    "HDM": perMin(player['hero_damage'], player['duration']),
    "permanent_buffs": player['permanent_buffs'],
    "rank_tier": player['rank_tier'],
    "life_state_dead": player['life_state_dead'],
    "predicted_win": predictModel(rank, player['ml_lane_role'], [positionFiller(player, player['ml_lane_role'])]),
    "buybacks": player['buyback_log'],
    "deaths_per_min": perMin(player['deaths'], player['duration']),
  }
  return player_resp

def commonCore(player):
  resp = {
    "last_hits": player['last_hits'],
    "lane_kills": (killsPerMinTen(player['kills_log']))*10,
    "multi_kills": player['multi_kills'],
    "xpm": player['xpm'],
    "gpm": player['gpm'],
    "kill_streaks": player['kill_streaks'],
    "lane_performance": percentageGoldGained(player['gold_t'][10]),
  }
  return resp

def pos1Rival(player):
  resp = {
    "kpm": perMin(player['kills'], player['duration']),
    "max_hero_hit": player['max_hero_hit'],
    "lowest_gpm": lowestGPMFiveMin(player['gold_t']),
    "lhm": perMin(player['last_hits'], player['duration']),
  }
  return resp

def pos2Rival(player):
  resp = {
    "runes_picked_up": player['runes_log'],
    "kpm": perMin(player['kills'], player['duration']),
    "max_hero_hit": player['max_hero_hit'],
    "lowest_gpm": lowestGPMFiveMin(player['gold_t']),
    "lhm": perMin(player['last_hits'], player['duration']),
  }
  return resp

def pos3Rival(player):
  resp = {
    "tower_damage": player['tower_damage'],
    "tdm": perMin(player['tower_damage'], player['duration']),
    "damage_taken": player['damage_taken'],
    "stuns": player['stuns'],
  }
  return resp

def pos4Rival(player):
  resp = {
    "runes_picked_up": player['runes_log'],
    "is_roaming": player['is_roaming'],
  }
  return resp

def pos5Rival(player):
  resp = {
    "obs_placed": player['obs_placed'],
    "sen_placed": player['sen_placed'],
    "hero_healing": player['hero_healing'],
    "hhm": perMin(player['hero_healing'], player['duration']),
  }
  return resp

def commonSup(player):
  resp = {
    "camps_stacked": player['camps_stacked'],
    "stuns": player['stuns']
  }
  return resp

def checkRanks(players):
  even = False
  while not even:
    radiant_roles = []
    dire_roles = []
    radiant_players = []
    dire_players = []

    for player in players:
      if player['ml_lane_role'] == None:
        player['ml_lane_role'] = 4
      if player['is_radiant']:
        radiant_roles.append(player['ml_lane_role'])
        radiant_players.append(player)
      else:
        dire_roles.append(player['ml_lane_role'])
        dire_players.append(player)

    print("radiant roles:", radiant_roles)
    print("dire roles:", dire_roles)
    print("---------------")
    radiant_counts = Counter(radiant_roles)
    dire_counts = Counter(dire_roles)
    radiant_excess_roles = []
    radiant_missing_roles = []
    dire_excess_roles = []
    dire_missing_roles = []

    for role in range(1,6):
      if role not in radiant_counts.keys():

        radiant_missing_roles.append(role)
      elif role not in dire_counts.keys():
        
        dire_missing_roles.append(role)

    for count in radiant_counts:
      if radiant_counts[count] > 1:
        radiant_excess_roles.append(count)
      elif radiant_counts[count] < 1:
        radiant_missing_roles.append(count)
    
    for count in dire_counts:
      if dire_counts[count] > 1:
        dire_excess_roles.append(count)
      elif dire_counts[count] < 1:
        dire_missing_roles.append(count)
    
    if len(radiant_excess_roles) == 0 and len(dire_excess_roles) == 0:
      even = True
    else:
      print("---------------")
      print(radiant_counts)
      print(dire_counts)
      if len(radiant_excess_roles) > 0:
        print("rad excess", radiant_excess_roles)
        findExcess(radiant_excess_roles, radiant_missing_roles, radiant_players)
      if len(dire_excess_roles) > 0:
        print("dire excess", dire_excess_roles)
        findExcess(dire_excess_roles, dire_missing_roles, dire_players)
  return players


def findExcess(excess, missing, players):
  for rank in excess:
    excess_players = []
    for player in players:
      if player['ml_lane_role'] == rank:
        excess_players.append(player)

    max_net_player, lowest_net_player = findHighestAndLowest(excess_players)
    print("---------------")
    print("role:", excess)
    print("missing:", missing)
    for player in players:
      if player['hero_id'] == max_net_player['hero_id']:
        if player['lane_role'] == 4:
          player['ml_lane_role'] = 3
        else:
          player['ml_lane_role'] = player['lane_role']
        print("highest:", player['ml_lane_role'])
      
      if player['hero_id'] == lowest_net_player['hero_id']:
        print("lowest:", player['ml_lane_role'])
        if len(missing) == 1:
          player['ml_lane_role'] = missing[0]
          print("fixed with:", player['ml_lane_role'])
        elif player['ml_lane_role'] == 1:
          player['ml_lane_role'] = 5
        elif player['ml_lane_role'] == 2:
          if 4 in missing:
            player['ml_lane_role'] = 4
          elif 3 in missing:
            player['ml_lane_role'] = 3
          elif 5 in missing:
            player['ml_lane_role'] = 5
          elif 1 in missing:
            player['ml_lane_role'] = 1
        elif player['ml_lane_role'] == 3:
          player['ml_lane_role'] = 4
        elif player['ml_lane_role'] == 4:
          if 2 in missing:
            player['ml_lane_role'] = 2
          if 5 in missing:
            player['ml_lane_role'] = 5

def findHighestAndLowest(excess):
  max_net_worth = excess[0]['net_worth']
  lowest_net_worth = excess[0]['net_worth']
  max_net_player = excess[0]
  lowest_net_player = excess[0]
  for excess_player in excess:
    if excess_player['net_worth'] > max_net_worth:
      max_net_worth = excess_player['net_worth']
      max_net_player = excess_player
    elif excess_player['net_worth'] < lowest_net_worth:
      lowest_net_worth = excess_player['net_worth']
      lowest_net_player = excess_player
  
  return max_net_player, lowest_net_player