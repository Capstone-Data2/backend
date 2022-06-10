from pymongo import MongoClient
import os
from dotenv import load_dotenv
#from player_role import findRole

load_dotenv()
client = MongoClient(os.getenv('DATABASE_URL'))
db = client.dota2

def findRank(rank):
    if rank > 10 and rank < 20:
        coll = "heraldmatches"
    if rank > 20 and rank < 30:
        coll = "guardianmatches"
    if rank > 30 and rank < 40:
        coll = "crusadermatches"
    if rank > 40 and rank < 50:
        coll = "archonmatches"
    if rank > 50 and rank < 60:
        coll = "legendmatches"
    if rank > 60 and rank < 70:
        coll = "ancientmatches"
    if rank > 70 and rank < 80:
        coll = "divinematches"
    if rank == 80:
        coll = "immortalmatches"
    return coll

def insertData(data, query, rank):
    coll = findRank(rank)
    insertPlayerData(data[1], coll)
    playercollection = db[coll + "_players"].find({'match_id': query}, {'_id': 1})
    playerids = []
    for player in playercollection:
        playerids.append(player)
    data[0]['players'] = playerids
    insertMatchData(data[0], coll)

def insertPlayerData(playerdata, coll):
    #for player in playerdata:
        #findRole(player)
    playercollection = db[coll + "_players"]
    playercollection.insert_many(playerdata)

def insertMatchData(matchdata, query):
    matchdatacollection = db[query + "_data"]
    matchdatacollection.insert_one(matchdata)

def insertMatch(match, query):
    matchcollection = db[query]
    matchcollection.insert_one(match)