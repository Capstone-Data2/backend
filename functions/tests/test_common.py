from functions.common import dataAccess, JSONResponseReturn
import mongomock

class TestDataAcess:

    def test_dataAccess(self):
        db = mongomock.MongoClient().db
        data_obj = {"match_id": 6674091014, "avg_rank_tier": 31}
        match_obj = {"match_id": 6674091014, "players": [{"_id" : 1}, {"_id": 2}]}
        player_arr = [{"_id" : 1, "hero": 1}, {"_id": 2, "hero": 2}, {"_id": 3, "hero": 3}]
        db["allmatches"].insert_one(data_obj)
        db["crusadermatches_data"].insert_one(match_obj)
        db["crusadermatches_players"].insert_many(player_arr)
        data, rank, match, players = dataAccess(db, 6674091014)
        assert(hasattr(data, "_id") == False)
        assert(hasattr(match, "_id") == False)
        for player in players:
            assert(hasattr(player, "_id") == False)
        del data_obj["_id"]
        del match_obj["_id"]
        for player in player_arr:
            del player["_id"]
        assert(data == data_obj)
        assert(rank == "crusader")
        assert(match == match_obj)
        assert(len(players) == len(player_arr)-1)
        player_arr.pop()
        assert(players == player_arr)
        

def test_JSONResponseReturn():
    params = ["damage", "damage_taken", "gold"]
    players = [{"hero_id": 61, "damage": 5000, "damage_taken": 10000, "gold": 10000}, {"hero_id": 34, "damage": 15000, "damage_taken": 7532, "gold": 14000}]
    expected = {"damage":{61: 5000, 34: 15000}, "damage_taken": {61: 10000, 34: 7532}, "gold": {61: 10000, 34: 14000} }
    assert(JSONResponseReturn(params, players) == expected)


