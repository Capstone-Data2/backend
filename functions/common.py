from functions.player import findRank
from utils import get_db_handle
db, client = get_db_handle()
match_players =  'matches_players'
match_data =  'matches_data'

def dataAccess(match_id, filter=0, hero_id=None ):
    data = db.allmatches.find_one({"match_id": match_id, }, {"_id": 0})
    if data is not None:
        rank = findRank(data['avg_rank_tier'])
    elif filter == "1" or data is None:
        data = db.promatches.find_one({"match_id": match_id, }, {"_id": 0})
        rank = "pro"
    match = db[rank + match_data].find_one({"match_id": match_id, }, {"_id": 0})
    if hero_id == None:
        players = list(db[rank + match_players].find({"match_id": match_id}, {"_id": 0}))
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