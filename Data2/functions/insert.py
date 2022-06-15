from player import findRank, findRole
from utils import get_db_handle

db, client = get_db_handle()
matchPlayers =  'matches_players'
matchData =  'matches_data'

def insertData(data, query, rank):
    coll = findRank(rank)
    insertPlayerData(data[1], coll, rank)
    playercollection = db[coll + matchPlayers].find({'match_id': query}, {'_id': 1})
    playerids = []
    for player in playercollection:
        playerids.append(player)
    data[0]['players'] = playerids
    insertMatchData(data[0], coll)

def insertPlayerData(playerdata, coll, rank):
    for player in playerdata:
        player['ml_lane_role'] = findRole(player, rank)
    playercollection = db[coll + matchPlayers]
    playercollection.insert_many(playerdata)

def insertMatchData(matchdata, coll):
    matchdatacollection = db[coll + matchData]
    matchdatacollection.insert_one(matchdata)

def insertMatch(match, coll):
    matchcollection = db[coll]
    matchcollection.insert_one(match)