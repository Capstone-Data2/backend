from pymongo import MongoClient
import requests
import time
import os
from dotenv import load_dotenv
from insert import insertData, insertMatch

load_dotenv()
client = MongoClient(os.getenv('DATABASE_URL'))
lobby_types = [5, 6, 7]
db = client.dota2

def sanitizeMatches(response):
    all_matches = []
    for data in response:
        if data['lobby_type'] in lobby_types:
            if data['duration'] > 900:
                matchdata = {
                    "match_id": data['match_id'],
                    "radiant_win": data['radiant_win'],
                    "start_time": data["start_time"],
                    "duration": data['duration'],
                    "lobby_type": data['lobby_type'],
                    "game_mode": data['game_mode'],
                    "avg_rank_tier": data['avg_rank_tier'],
                    "radiant_team": data['radiant_team'],
                    "dire_team": data['dire_team'],
                }
                all_matches.append(matchdata)
        continue
    return all_matches

def sanitizeMatch(response, avg_rank):
    if response['dire_score'] != 0 or response['radiant_score'] != 0:
        if "comeback" not in response.keys():
            response['comeback'] = None
            response['stomp'] = None
        if "throw" not in response.keys():
            response['throw'] = None
            response['loss'] = None
        matchdata = {
            'match_id': response['match_id'],
            'barracks_status_dire': response['barracks_status_dire'],
            'barracks_status_radiant': response['barracks_status_radiant'],
            'dire_score': response['dire_score'], 
            'duration': response['duration'], 
            'first_blood_time': response['first_blood_time'],
            'picks_bans': response['picks_bans'],
            'objectives': response['objectives'],
            'radiant_gold_adv': response['radiant_gold_adv'],
            'radiant_score': response['radiant_score'], 
            'radiant_win': response['radiant_win'], 
            'radiant_xp_adv': response['radiant_xp_adv'],
            'start_time': response['start_time'],
            'teamfights': response['teamfights'],
            'players': [],
            'replay_url': response['replay_url'],
            'avg_rank_tier': avg_rank,
            'comeback': response['comeback'],
            'stomp': response['stomp'],
            'throw': response['throw'],
            'loss': response['loss'],
        }
        
        playerdata = []
        for player in response['players']:
            playerdata.append(sanitizePlayer(player))
    
        return matchdata, playerdata
    return False

def sanitizePlayer(player):
    if "personaname" not in player.keys():
        player['personaname'] = "Unknown"
    if "kills_per_min" not in player.keys():
        player["kills_per_min"] = 0
    playerdata = {
        'match_id': player['match_id'],
        'ability_upgrades_arr': player['ability_upgrades_arr'],
        'account_id': player['account_id'], 
        'additional_units': player['additional_units'], 
        'assists': player['assists'], 
        'backpack_0': player['backpack_0'], 
        'backpack_1': player['backpack_1'],
        'backpack_2': player['backpack_2'],
        'buyback_log': player['buyback_log'],
        'camps_stacked': player['camps_stacked'],
        'damage': player['damage'],
        'damage_taken': player['damage_taken'],
        'deaths': player['deaths'], 
        'denies': player['denies'],
        'dn_t': player['dn_t'],
        'gpm': player['gold_per_min'],
        'gold_t': player['gold_t'],
        'hero_damage': player['hero_damage'],
        'hero_healing': player['hero_healing'], 
        'hero_id': player['hero_id'], 
        "item_0": player['item_0'],
        "item_1": player['item_1'],
        "item_2": player['item_2'],
        "item_3": player['item_3'],
        "item_4": player['item_4'],
        "item_5": player['item_5'],
        "item_neutral": player["item_neutral"],
        "kill_streaks": player["kill_streaks"],
        "killed": player["killed"],
        'kills': player['kills'],
        "kills_log": player["kills_log"],
        'last_hits': player['last_hits'],  
        'level': player['level'],
        'lh_t': player['lh_t'],
        'max_hero_hit': player['max_hero_hit'],
        'multi_kills': player['multi_kills'],
        'net_worth': player['net_worth'],
        'obs_placed': player['obs_placed'],
        'party_id': player['party_id'],
        'permanent_buffs': player['permanent_buffs'],
        'purchase_log': player['purchase_log'],
        'rune_pickups': player['rune_pickups'],
        'runes_log': player['runes_log'],
        'sen_placed': player['sen_placed'],
        'stuns': player['stuns'],
        'tower_damage': player['tower_damage'],
        'xpm': player['xp_per_min'],
        'xp_t': player['xp_t'],
        'personaname': player['personaname'],
        'duration': player['duration'],
        'is_radiant': player['isRadiant'],
        'win': player['win'],
        'total_gold': player['total_gold'],
        'total_xp': player['total_xp'],
        'kills_per_min': player['kills_per_min'],
        'kda': player['kda'],
        'lane': player['lane'], 
        'lane_role': player["lane_role"],
        'is_roaming': player['is_roaming'],
        'life_state_dead': player['life_state_dead'], 
        'rank_tier': player['rank_tier'],
        'ml_lane_role': 0,
    }
    return playerdata

def sanitize(res):
    alldata = sanitizeMatches(res)
    for match in alldata:
        if db.allmatches.count_documents({'match_id': match['match_id']}) == 0:
            insertMatch(match, "allmatches")
            query = match['match_id']
            print(query)
            response = requests.get(f'https://api.opendota.com/api/matches/{query}').json()
            if "replay_url" not in response.keys() or "radiant_gold_adv" not in response.keys():
                time.sleep(1.5)
                requests.post(f'https://api.opendota.com/api/request/{query}')
                time.sleep(3)
                response = requests.get(f'https://api.opendota.com/api/matches/{query}').json()
            data = sanitizeMatch(response, match['avg_rank_tier'])
            if data != False:
                insertData(data, query, match['avg_rank_tier'])
            time.sleep(1.5)
        