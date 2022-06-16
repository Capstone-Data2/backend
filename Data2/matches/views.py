from turtle import position
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
#from backend.Data2.model.predictModel import predictModel
from utils import get_db_handle
from functions import player as pl
import pandas as pd

from model.predictModel import predictModel
from functions.player import findRank, perMin, lowestGPMFiveMin, killParticipation, killsPerMinTen, percentageGoldGained
from model.positionFeatures import positionFiller

db, client = get_db_handle()
# Create your views here.

class RecentMatches(View):
  
  def get(self, request, *args, **kwargs):
    print("hi")
  
  def post(self, request, *args, **kwargs):
    print("hi")

class Match(View):
  
  def get(self, match_id, request, *args, **kwargs):
    print("hi")
  
  def post(self, match_id, request, *args, **kwargs):
    print("hi")

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
    
    return JsonResponse(resp)
    
class Rivals(View):

  def get(self, match_id, hero_id, request, *args, **kwargs):
    print("hi")
  
  def post(self, match_id, hero_id, request, *args, **kwargs):
    print("hi")