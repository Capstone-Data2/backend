#from player import checkRanks
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
import time
import certifi

load_dotenv()

client = MongoClient(os.getenv('DATABASE_URL'),  tlsCAFile=certifi.where())
db = client.dota2
matchPlayers =  'matches_players'
"""
def updateMLLaneRole():
    ranks = ['herald', 'guardian', 'crusader', 'archon', 'legend', 'ancient', 'divine', 'immortal']
    loop = True
    count = 1
    while loop:
        if count < 9:
            rankCollection= db[ranks[count-1] + matchPlayers]
            collection = rankCollection.find({'ml_lane_role': 0}, {'last_hits': 1, 'obs_placed': 1, 'gpm': 1, 'lane_role': 1, '_id': 1})
            for player in collection:
                role = findRole(player, count*10)
                rankCollection.update_one({'_id':player['_id']}, {"$set": {"ml_lane_role": role}})
            count += 1
        else:
            loop = False
"""
def updateWardAndCombat():
    ranks = ['herald', 'guardian', 'crusader', 'archon', 'legend', 'ancient', 'divine', 'immortal']
    loop = True
    count = 1
    while loop:
        if count < 9:
            rankCollection = db[ranks[count-1] + matchPlayers]
            collection = list(rankCollection.find())
            last_match_id = collection[0]['match_id']
            last_match = requests.get(f'https://api.opendota.com/api/matches/{last_match_id}').json()
            max_len = len(collection)
            if "damage_inflictor" not in collection[max_len-1]:
                print(ranks[count-1])
                for player in collection:
                    if player['match_id'] != last_match_id:
                        new_match_id = player['match_id']
                        time.sleep(1.2)
                        last_match = requests.get(f'https://api.opendota.com/api/matches/{new_match_id}').json()
                    for match_player in last_match['players']:
                        if player['hero_id'] == match_player['hero_id']:
                            rankCollection.update_one({'_id':player['_id']}, {
                                "$set": {
                                    "damage_inflictor": match_player['damage_inflictor'],
                                    "damage_inflictor_received": match_player['damage_inflictor_received'],
                                    "damage_targets": match_player['damage_targets'],
                                    "obs_log": match_player['obs_log'],
                                    "obs_left_log": match_player['obs_left_log'],
                                    "sen_log": match_player['sen_log'],
                                    "sen_left_log": match_player['sen_left_log']
                                    }
                                }, 
                                upsert=True
                            )
            count += 1
        else:
            loop = False
"""
def updateMLRoles():
    ranks = ['herald', 'guardian', 'crusader', 'archon', 'legend', 'ancient', 'divine', 'immortal']
    loop = True
    count = 1
    while loop:
        if count < len(ranks)+1:
            matchCollection = db[ranks[count-1] + "matches_data"].find({}, {"_id": 0})
            rankCollection = db[ranks[count-1] + matchPlayers]
            matchcount = 1
            for match in matchCollection:
                print("---------------")
                print(matchcount)
                print(match['match_id'])
                collection = rankCollection.find({'match_id': match['match_id']})
                clean_players = []
                for player in collection:
                    clean_players.append(player)
                checked_players = checkRanks(clean_players)
                for player in checked_players:
                    rankCollection.update_one({'_id':player['_id']}, {"$set": {"ml_lane_role": player['ml_lane_role']}})
                matchcount += 1
            count += 1
        else:
            loop = False

#updateMLRoles() """

updateWardAndCombat()