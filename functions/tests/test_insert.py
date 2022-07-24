from functions.insert import insertMatch, insertData, insertPlayerData, insertMatchData
import mongomock

db = mongomock.MongoClient().db
match = {"match_id": 6674091014}
playerdata = [
        {
            "hero_id": 1,
            "lane_role": 1,
            "ml_lane_role": 1,
            "net_worth": 10000,
            "is_radiant": True,
            "last_hits": 300,
            "obs_placed": 2,
            "gpm": 500
        },
        {
            "hero_id": 2,
            "lane_role": 1,
            "ml_lane_role": 5,
            "net_worth": 5000,
            "is_radiant": True,
            "last_hits": 50,
            "obs_placed": 2,
            "gpm": 500
        },
        {
            "hero_id": 3,
            "lane_role": 2,
            "ml_lane_role": 2,
            "net_worth": 15000,
            "is_radiant": True,
            "last_hits": 200,
            "obs_placed": 2,
            "gpm": 500
        },
        {
            "hero_id": 4,
            "lane_role": 3,
            "ml_lane_role": 4,
            "net_worth": 7800,
            "is_radiant": True,
            "last_hits": 15,
            "obs_placed": 2,
            "gpm": 500
        },
        {
            "hero_id": 5,
            "lane_role": 3,
            "ml_lane_role": 3,
            "net_worth": 12000,
            "is_radiant": True,
            "last_hits": 120,
            "obs_placed": 2,
            "gpm": 500
        },
        {
            "hero_id": 6,
            "lane_role": 1,
            "ml_lane_role": 1,
            "net_worth": 11200,
            "is_radiant": False,
            "last_hits": 350,
            "obs_placed": 2,
            "gpm": 500
        },
        {
            "hero_id": 7,
            "lane_role": 1,
            "ml_lane_role": 5,
            "net_worth": 6150,
            "is_radiant": False,
            "last_hits": 30,
            "obs_placed": 2,
            "gpm": 500
        },
        {
            "hero_id": 8,
            "lane_role": 2,
            "ml_lane_role": 2,
            "net_worth": 17500,
            "is_radiant": False,
            "last_hits": 250,
            "obs_placed": 2,
            "gpm": 500
        },
        {
            "hero_id": 9,
            "lane_role": 3,
            "ml_lane_role": 4,
            "net_worth": 6300,
            "is_radiant": False,
            "last_hits": 20,
            "obs_placed": 2,
            "gpm": 500
        },
        {
            "hero_id": 10,
            "lane_role": 3,
            "ml_lane_role": 3,
            "net_worth": 14200,
            "is_radiant": False,
            "last_hits": 130,
            "obs_placed": 2,
            "gpm": 500
        },
    ]

def test_insertData():
    data = [match, playerdata]
    insertData(db, data, 6674091014, 80)
    assert list(db["immortalmatches_data"].find())[0] == match
    assert list(db["immortalmatches_players"].find()) == playerdata


def test_insertPlayerData():

    insertPlayerData(db, playerdata, "crusader")
    assert list(db["crusadermatches_players"].find()) == playerdata


def test_insertMatchData():
    coll = "crusader"
    insertMatchData(db, match, coll)
    assert list(db[coll + "matches_data"].find())[0] == match


def test_insertMatch():
    coll = "allmatches"
    insertMatch(db, match, coll)
    assert list(db[coll].find())[0] == match
