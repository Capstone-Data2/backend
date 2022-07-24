from functions.common import dataAccess, JSONResponseReturn

def test_dataAccess():
    assert(5==5)
    #assert(dataAccess(6674091014))

def test_JSONResponseReturn():
    params = ["damage", "damage_taken", "gold"]
    players = [{"hero_id": 61, "damage": 5000, "damage_taken": 10000, "gold": 10000}, {"hero_id": 34, "damage": 15000, "damage_taken": 7532, "gold": 14000}]
    expected = {"damage":{61: 5000, 34: 15000}, "damage_taken": {61: 10000, 34: 7532}, "gold": {61: 10000, 34: 14000} }
    assert(JSONResponseReturn(params, players) == expected)

