from utils import get_db_handle
from functions.player import perMin, lowestGPMFiveMin, killParticipation, killsPerMinTen, percentageGoldGained, rivalResponse, findRank
from functions.time import getTimeDiff 
from functions.data_set import get_data_set, get_pro_data_set
from functions.sanitize import parse, sanitizeMatch
from functions.insert import insertMatch, insertData
from model.predictModel import predictModel
from model.positionFeatures import positionFiller
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from functions.common import JSONResponseReturn, dataAccess

# Create your views here.
db, client = get_db_handle()
match_players =  'matches_players'
match_data = 'matches_data'
class RecentMatches(APIView):
  
  def get(self, request, *args, **kwargs):
    rank = request.GET.get('rank')
    if rank == "9":
      collection = db.promatches
      data = collection.find({}, {"_id": 0}).sort("_id", -1).limit(20)
    else:
      collection = db.allmatches
      if rank == "0":
        data = collection.find({}, {"_id": 0}).sort("start_time", -1).limit(20)
      else:
        data = collection.find({"avg_rank_tier": {"$gt": (int(rank)*10)-1, "$lt": (int(rank)*10)+6}}, {"_id": 0}).sort("start_time", -1).limit(20)
    match_list = []
    for match in data:
      match_list.append(getTimeDiff(match))

    res_object = {"matches": match_list}
    return Response(res_object, status=status.HTTP_200_OK)

  def post(self, request, *args, **kwargs):
    if request.data == {}:
      filter = []
    if request.data == {"filter": "pro"}:
      get_pro_data_set()
      return Response(status=status.HTTP_201_CREATED)
    else:
      filter = request.data['filter']
    get_data_set(filter)
    return Response(status=status.HTTP_201_CREATED)

class Match(APIView):
  
  def get(self, request, match_id, *args, **kwargs):
    data, rank, match, players = dataAccess(db, match_id)
    match = getTimeDiff(match)

    radiant_win = 0
    dire_win = 0
    for player in players:
      radiant_name = "Radiant"
      dire_name = "Dire"

      if "radiant_name" in data:
        radiant_name = data["radiant_name"]
        dire_name = data["dire_name"]
      else: 
        if player['rank_tier'] == None:
          player['rank_tier'] = data['avg_rank_tier']

      if player['is_radiant']:
        radiant_win += predictModel(rank, player['ml_lane_role'], [positionFiller(player, player['ml_lane_role'])])
      else:
        dire_win += predictModel(rank, player['ml_lane_role'], [positionFiller(player, player['ml_lane_role'])])


    
    match['radiant_win_proba'] = round(radiant_win, 2)
    match['dire_win_proba'] = round(dire_win, 2)
    match['players'] = players
    match['radiant_name'] = radiant_name
    match['dire_name'] = dire_name
    return Response(match, status=status.HTTP_200_OK)
  
  def post(self, request, match_id, *args, **kwargs):
    if db.allmatches.count_documents({'match_id': match_id}) == 0:
      response = requests.get(f'https://api.opendota.com/api/matches/{match_id}').json()
      if response['duration'] != None:
        lobby_types = [5, 6, 7]
        if response['lobby_type'] in lobby_types:
          total_rank = 0
          count = 0
          radiant_heroes = []
          dire_heroes = []
          for player in response['players']:
            if player['rank_tier'] != None:
              total_rank += player['rank_tier']
              count += 1
            if player['isRadiant']:
              radiant_heroes.append(str(player['hero_id']))
            else:
              dire_heroes.append(str(player['hero_id']))
          avg_rank = total_rank / count
          match = {
            "match_id": response['match_id'],
            "radiant_win": response['radiant_win'],
            "start_time": response['start_time'],
            "duration": response['duration'],
            "lobby_type": response['lobby_type'],
            "game_mode": response['game_mode'],
            "avg_rank_tier": avg_rank,
            "radiant_team": ",".join(radiant_heroes),
            "dire_team": ",".join(dire_heroes)
          }
          parsed_res = parse(response, match_id)
          if parsed_res[0]:
            insertMatch(match, "allmatches")
            data = sanitizeMatch(parsed_res[1], avg_rank)
            if data != False:
              insertData(data, match_id, avg_rank)
              return Response(status=status.HTTP_201_CREATED)
          else:
            return Response({"error": "Match can't be parsed right now, please try again later"},status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
          return Response({"error": "Ranked only pls"},status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response({"error": "Match does not exist"},status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response({"error": "Match already in DB"},status=status.HTTP_400_BAD_REQUEST)

class Performance(APIView):
  
  def get(self, request, match_id):
    data, rank, match, players = dataAccess(db, match_id)
    
    if rank == None:
      return Response({"error": "Match does not exist"},status=status.HTTP_400_BAD_REQUEST)
    else:
      response = {}
      for selected_player in players:
        resp = {
          'GPM': selected_player['gpm'],
          'XPM': selected_player['xpm'],
          'LHM': perMin(selected_player['last_hits'], match['duration']),
          'DNM': perMin(selected_player['denies'], match['duration']),
          'DPM': perMin(selected_player['deaths'], match['duration']),
          'HDM': perMin(selected_player['hero_damage'], match['duration']),
          'KPM': perMin(selected_player['kills'], match['duration']),
          'KP': round(killParticipation(selected_player['is_radiant'], match['radiant_score'], match['dire_score'], selected_player['kills'], selected_player['assists']), 3),
          'HHM' : perMin(selected_player['hero_healing'], match['duration']),
          'TDM' : perMin(selected_player['tower_damage'], match['duration']),
          'Lowest GPM' : lowestGPMFiveMin(selected_player['gold_t']),
          'KPM @ 10' : killsPerMinTen(selected_player['kills_log']),
          'XPM @ 10' : selected_player['xp_t'][10]/10,
          'LHM @ 10' : selected_player['lh_t'][10]/10,
          '% of Gold @ 10' : round(percentageGoldGained(selected_player['gold_t'][10]), 2),
          'ML Score': round(predictModel(rank, selected_player['ml_lane_role'], [positionFiller(selected_player, selected_player['ml_lane_role'])])*100, 2)
        }
        response.update({str(selected_player['hero_id']): resp})
      
      return Response(response)
    
class Rivals(APIView):

  def get(self, request, match_id, hero_id, *args, **kwargs):
    data, rank, match, selected_player = dataAccess(db, match_id, hero_id)
    rival = None
    for player in match['players']:
      player_details = db[rank + match_players].find_one({'_id': player['_id']}, {"_id": 0})
      if selected_player['hero_id'] is not player_details['hero_id']:
        if player_details['ml_lane_role'] is selected_player['ml_lane_role']:
          rival = player_details

    players = [selected_player, rival]

    if rival == None:
      print("None")
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
      formatted_players = []
      for player in players:
        player_resp = rivalResponse(player, rank)
        formatted_players.append(player_resp)
      resp = {"rivals": formatted_players}
      return Response(resp, status=status.HTTP_200_OK)

class Items(APIView):

  def get(self, request, match_id, *args, **kwargs):
    data, rank, match, players = dataAccess(db,match_id)
    player_items = {}
    for player in players:
      items = player['purchase_log']
      player_items.update({player['hero_id']: items})

    return Response(player_items, status=status.HTTP_200_OK)

class GraphData(APIView):

  def get(self, request, match_id, *args, **kwargs):
    data, rank, match, players = dataAccess(db, match_id)

    resp = {"radiant_advantage": {"team_gold": match['radiant_gold_adv'], "team_xp": match['radiant_xp_adv']}}
    resp.update(JSONResponseReturn(["xp_t", "gold_t", "lh_t"], players))
    
    return Response(resp, status=status.HTTP_200_OK)

class WardData(APIView):

  def get(self, request, match_id, *args, **kwargs):
    data, rank, match, players = dataAccess(db, match_id)

    resp = JSONResponseReturn(["obs_log", "sen_log", "obs_left_log", "sen_left_log"], players)

    return Response(resp, status=status.HTTP_200_OK)

class CombatData(APIView):

  def get(self, request, match_id, *args, **kwargs):
    data, rank, match, players = dataAccess(db, match_id)

    resp = JSONResponseReturn(["damage_inflictor", "damage_inflictor_received", "damage_targets"], players)
    return Response(resp, status=status.HTTP_200_OK)

class Log(APIView):
  def get(self, request, match_id):
    data, rank, match, players = dataAccess(db, match_id)
    
    objectives = match['objectives']
    
    player_kills = []
    player_runes = []
    count = 0
    for player in players:  
      player_kill_log = {
        str(player['hero_id']): player['kills_log']
      }
      player_rune_log = {
        str(player['hero_id']): player['runes_log']
      }
      player_kills.append(player_kill_log)
      player_runes.append(player_rune_log)
    
    towers = []
    roshans_kills = []

    for objective in objectives:
      if objective['type'] == 'building_kill':
        towerData = {
          'time' : objective['time'],
          'tower' : objective['key'],
          'unit' : objective['unit'],
        }
        towers.append(towerData)
      
      elif objective['type'] == 'CHAT_MESSAGE_ROSHAN_KILL':
        roshans_kills.append({
          'time': objective['time'],
          'team' : objective['team'] 
        })

    roshan = []
    count = 0
    for kills in roshans_kills:
      roshan.append({
        'rosh_kill_time': kills['time'],
        'rosh_kill_team': kills['team'],
      })
      count = count + 1 
      
    resp = {
      'Kills': player_kills,
      'Buildings': towers,
      'Roshan': roshan,
      'Runes' : player_runes,
    }
    return Response(resp, status=status.HTTP_200_OK)