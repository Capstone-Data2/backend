from pymongo import MongoClient
import os
from player import findRole
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('DATABASE_URL'))
db = client.dota2
matchPlayers =  'matches_players'

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

updateMLLaneRole()