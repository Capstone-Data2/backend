from functions.common import dataAccess, JSONResponseReturn
import mongomock

class TestDataAcess:

    def _dataAccess_test_setup(self, db, id, type, rank, tier = 0):
        data_obj = {"match_id": id, "avg_rank_tier": tier}
        match_obj = {"match_id": id, "players": [{"_id" : 1}, {"_id": 2}]}
        player_objs = [{"_id" : 1, "match_id": id, "hero_id": 1}, {"_id": 2, "match_id": id, "hero_id": 2}, {"_id": 3, "match_id": id, "hero_id": 3}]
        db[f"{type}matches"].insert_one(data_obj)
        db[f"{rank}matches_data"].insert_one(match_obj)
        db[f"{rank}matches_players"].insert_many(player_objs)
        return data_obj, match_obj, player_objs
    
    def _dataAccess_asserts(self, db, id, data_obj, match_obj, player_objs, rank_obj, hero_id = None):
        data, rank, match, players = dataAccess(db, id, hero_id)
        assert(hasattr(data, "_id") == False)
        assert(hasattr(match, "_id") == False)
        del data_obj["_id"]
        del match_obj["_id"]
        assert(data == data_obj)
        assert(rank == rank_obj)
        assert(match == match_obj)
        for player in player_objs:
            del player["_id"]
        if hero_id == None:
            for player in players:
                assert(hasattr(player, "_id") == False)
            assert(len(players) == len(player_objs)-1)
            
            player_objs.pop()
            assert(players == player_objs)
        else:
            assert(len([players]) == 1)
            assert(players == player_objs[2])


    def test_dataAccessPublicMatches(self):
        db = mongomock.MongoClient().db
        data_obj, match_obj, player_objs = self._dataAccess_test_setup(db, 6674091014, "all", "crusader", 31)
        self._dataAccess_asserts(db, 6674091014, data_obj, match_obj, player_objs, "crusader")
        
    
    def test_dataAccessProMatches(self):
        db = mongomock.MongoClient().db
        data_obj, match_obj, player_objs = self._dataAccess_test_setup(db, 6672384255, "pro", "pro")
        self._dataAccess_asserts(db, 6672384255, data_obj, match_obj, player_objs, "pro")
    
    def test_dataAccessHeroID(self):
        db = mongomock.MongoClient().db
        data_obj, match_obj, player_objs = self._dataAccess_test_setup(db, 6674091014, "all", "legend", 53)
        self._dataAccess_asserts(db, 6674091014, data_obj, match_obj, player_objs, "legend", 3)

        

def test_JSONResponseReturn():
    params = ["damage", "damage_taken", "gold"]
    players = [{"hero_id": 61, "damage": 5000, "damage_taken": 10000, "gold": 10000}, {"hero_id": 34, "damage": 15000, "damage_taken": 7532, "gold": 14000}]
    expected = {"damage":{61: 5000, 34: 15000}, "damage_taken": {61: 10000, 34: 7532}, "gold": {61: 10000, 34: 14000} }
    assert(JSONResponseReturn(params, players) == expected)


