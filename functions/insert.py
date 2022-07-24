from functions.player import findRank, findRole, checkRanks

matchPlayers =  'matches_players'
matchData =  'matches_data'

def insertData(db, data, query, rank):
    if rank == 90:
        coll = "pro"
    else:
        coll = findRank(rank)
    insertPlayerData(db, data[1], coll)
    playercollection = db[coll + matchPlayers].find({'match_id': query}, {'_id': 1})
    playerids = []
    for player in playercollection:
        playerids.append(player)
    data[0]['players'] = playerids
    insertMatchData(db, data[0], coll)

def insertPlayerData(db, playerdata, coll):
    match_ranks = []
    for player in playerdata:
        player['ml_lane_role'] = findRole(player, coll)
        match_ranks.append(player['ml_lane_role'])
    checked_players = checkRanks(playerdata)
    playercollection = db[coll + matchPlayers]
    playercollection.insert_many(checked_players)

def insertMatchData(db, matchdata, coll):
    matchdatacollection = db[coll + matchData]
    matchdatacollection.insert_one(matchdata)

def insertMatch(db, match, coll):
    matchcollection = db[coll]
    matchcollection.insert_one(match)