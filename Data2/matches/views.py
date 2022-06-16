from django.views import View
from utils import get_db_handle
from functions.player import findRank, perMin, lowestGPMFiveMin, killParticipation, killsPerMinTen, percentageGoldGained
from functions.time import getTimeDiff 
from functions.data_set import get_data_set
from functions.sanitize import parse, sanitizeMatch
from functions.insert import insertMatch, insertData
from model.predictModel import predictModel
from model.positionFeatures import positionFiller
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

db, client = get_db_handle()
# Create your views here.
db, client = get_db_handle()
matchPlayers =  'matches_players'
matchData =  'matches_data'

class RecentMatches(APIView):
  
  def get(self, request, *args, **kwargs):
    collection = db.allmatches
    data = collection.find({}, {"_id": 0}).sort("_id", -1).limit(20)
    match_list = []
    for match in data:
      match_list.append(getTimeDiff(match))

    res_object = {"matches": (sorted(match_list, key=lambda x: x["time_difference"]))}
    return Response(res_object)

  def post(self, request, *args, **kwargs):
    filter = request.data['filter']
    get_data_set(filter)
    return Response(status=status.HTTP_201_CREATED)

class Match(APIView):
  
  def get(self, request, match_id, *args, **kwargs):
    data = db.allmatches.find_one({"match_id": match_id}, {"_id": 0})
    rank = findRank(data['avg_rank_tier'])
    match = db[rank + matchData].find_one({"match_id": match_id}, {"_id": 0})
    match = getTimeDiff(match)

    players = []
    radiant_win = 0
    dire_win = 0
    for player in match['players']:
      player_details = db[rank + matchPlayers].find_one({"_id": player['_id']}, {"_id": 0})
      player = player_details
      players.append(player_details)

      if player['rank_tier'] == None:
        player['rank_tier'] = data['avg_rank_tier']

      if player['is_radiant']:
        radiant_win += predictModel(rank, player['ml_lane_role'], [positionFiller(player, player['ml_lane_role'])])
      else:
        dire_win += predictModel(rank, player['ml_lane_role'], [positionFiller(player, player['ml_lane_role'])])
    
    match['radiant_win_proba'] = radiant_win
    match['dire_win_proba'] = dire_win
    match['players'] = players
    return Response(match)
  
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
              radiant_heroes.append(player['hero_id'])
            else:
              dire_heroes.append(player['hero_id'])
          avg_rank = total_rank / count
          match = {
            "match_id": response['match_id'],
            "radiant_win": response['radiant_win'],
            "start_time": response['start_time'],
            "duration": response['duration'],
            "lobby_type": response['lobby_type'],
            "game_mode": response['game_mode'],
            "avg_rank_tier": avg_rank,
            "radiant_team": radiant_heroes,
            "dire_team": dire_heroes
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

class Player(View):
  
  def get(self, request, match_id, hero_id):
    rankData = db.allmatches.find_one({"match_id": match_id, }, {"_id": 0})
    rank = findRank(rankData['avg_rank_tier'])
    match = db[f"{rank}"+'matches_players'].find_one({"match_id": match_id, "hero_id": hero_id,}, {"_id": 0})
    matchData = db[f"{rank}" + 'matches_data'].find_one({"match_id": match_id, }, {"_id": 0})
    
    resp = {
      'LHM': perMin(match['last_hits'], match['duration']),
      'Denies per min': perMin(match['denies'], match['duration']),
      'Deaths per min': perMin(match['deaths'], match['duration']),
      'HDM': perMin(match['hero_damage'], match['duration']),
      'Kill Participation': killParticipation(match['is_radiant'], matchData['radiant_score'], matchData['dire_score'], match['kills'], match['assists']),
      'Hero Healing per min' : perMin(match['hero_healing'], match['duration']),
      'TDM' : perMin(match['tower_damage'], match['duration']),
      'Lowest GPM in 5 min interval' : lowestGPMFiveMin(match['gold_t']),
      'KPM10' : killsPerMinTen(match['kills_log']),
      'XPM10' : match['xp_t'][10]/10,
      'LHM10' : match['lh_t'][10]/10,
      'Percentage of gained gold vs total available10' : percentageGoldGained(match['gold_t'][10]),
      'Model Prediction': predictModel(findRank(rankData['avg_rank_tier']), match['ml_lane_role'], [positionFiller(match, match['ml_lane_role'])])
    }
    
    return Response(resp)
    
class Rivals(View):

  def get(self, request, match_id, hero_id, *args, **kwargs):
    print("hi")
  
  def post(self, request, match_id, hero_id, *args, **kwargs):
    print("hi")