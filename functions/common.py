from functions.player import findRank
from utils import get_db_handle
db, client = get_db_handle()
match_players =  'matches_players'
match_data =  'matches_data'

def dataAccess(match_id, hero_id=None):
    data = db.allmatches.find_one({"match_id": match_id, }, {"_id": 0})
    if data is not None:
        rank = findRank(data['avg_rank_tier'])
    elif data is None:
        data = db.promatches.find_one({"match_id": match_id, }, {"_id": 0})
        rank = "pro"
    match = db[rank + match_data].find_one({"match_id": match_id, }, {"_id": 0})
    if hero_id == None:
        players = []
        for player in match["players"]:
            players.append(db[rank + match_players].find_one({"_id": player["_id"]}, {"_id": 0}))

        return data, rank, match, players
    else:
        selected_player = db[rank + match_players].find_one({"match_id": match_id, "hero_id": hero_id,}, {"_id": 0})
        return data, rank, match, selected_player

def JSONResponseReturn(params, players):
    resp = {}
    for param in params:
        values = {}
        for player in players:
            values.update({player["hero_id"]: player[param]})
        resp.update({param: values})
    return resp