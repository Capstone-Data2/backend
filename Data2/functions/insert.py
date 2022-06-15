from pymongo import MongoClient
import os
from dotenv import load_dotenv
from player import findRank, findRole

load_dotenv()
client = MongoClient(os.getenv('DATABASE_URL'))
db = client.dota2
matchPlayers =  'matches_players'
matchData =  'matches_data'

def insertData(data, query, rank):
    coll = findRank(rank)
    insertPlayerData(data[1], coll)
    playercollection = db[coll + matchPlayers].find({'match_id': query}, {'_id': 1})
    playerids = []
    for player in playercollection:
        playerids.append(player)
    data[0]['players'] = playerids
    insertMatchData(data[0], coll)

def insertPlayerData(playerdata, coll):
    #for player in playerdata:
        #findRole(player)
    playercollection = db[coll + matchPlayers]
    playercollection.insert_many(playerdata)

def insertMatchData(matchdata, coll):
    matchdatacollection = db[coll + matchData]
    matchdatacollection.insert_one(matchdata)

def insertMatch(match, coll):
    matchcollection = db[coll]
    matchcollection.insert_one(match)