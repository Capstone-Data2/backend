from functions.sanitize import sanitizeMatches, parse, sanitize, sanitizePro
import mongomock
import requests
import requests_mock
from unittest.mock import patch
import json

data_obj = {"match_id": 6676192106, "avg_rank_tier": 31}
amateur_data = [{
                "match_id": 6676192106,
                "match_seq_num": 5583309030,
                "radiant_win": True,
                "start_time": 1658678267,
                "duration": 1903,
                "avg_mmr": 2549,
                "num_mmr": 2,
                "lobby_type": 5,
                "game_mode": 4,
                "avg_rank_tier": 44,
                "num_rank_tier": 2,
                "cluster": 183,
                "radiant_team": "135,26,41,88,49",
                "dire_team": "123,74,15,11,72"
            },
            {
                "match_id": 6676192018,
                "match_seq_num": 5583313368,
                "radiant_win": True,
                "start_time": 1658678273,
                "duration": 2040,
                "avg_mmr": 2549,
                "num_mmr": 2,
                "lobby_type": 7,
                "game_mode": 22,
                "avg_rank_tier": 53,
                "num_rank_tier": 4,
                "cluster": 193,
                "radiant_team": "135,14,101,44,50",
                "dire_team": "40,69,10,64,13"
            },
            {
                "match_id": 6676192016,
                "match_seq_num": 5583310578,
                "radiant_win": True,
                "start_time": 1658678273,
                "duration": 1925,
                "avg_mmr": 2549,
                "num_mmr": 2,
                "lobby_type": 7,
                "game_mode": 22,
                "avg_rank_tier": 14,
                "num_rank_tier": 2,
                "cluster": 188,
                "radiant_team": "50,93,113,86,73",
                "dire_team": "75,105,2,37,36"
            }]
pro_data = [{
                    "match_id": 6676192106,
                    "radiant_win": True,
                    "start_time": 1658678273,
                    "duration": 2040,
                    "radiant_name": 'sdf',
                    "dire_name": 'sdf',
                    "leagueid" : 123454
                },{
                    "match_id": 123456,
                    "radiant_win": True,
                    "start_time": 1658678273,
                    "duration": 2040,
                    "radiant_name": 'sdf',
                    "dire_name": 'sdf',
                    "leagueid" : 123454
                },{
                    "match_id": 123456,
                    "radiant_win": True,
                    "start_time": 1658678273,
                    "duration": 2040,
                    "radiant_name": 'sdf',
                    "dire_name": 'sdf',
                    "leagueid" : 123454
                }]

with open('functions/tests/testing_constants/sanitized_match.json', 'r') as p:
    sanitized_match = json.loads(p.read())
    del sanitized_match["players"],
with open('functions/tests/testing_constants/match.json', 'r') as j:
    match = json.loads(j.read())

class TestSanitizeMatches:

    def test_sanitze_matches_amateur(self):
        
        expected_response = [{'match_id': 6676192106, 'radiant_win': True, 'start_time': 1658678267, 'duration': 1903, 'lobby_type': 5, 'game_mode': 4, 'avg_rank_tier': 44, 'radiant_team': '135,26,41,88,49', 'dire_team': '123,74,15,11,72'}, 
        {'match_id': 6676192018, 'radiant_win': True, 'start_time': 1658678273, 'duration': 2040, 'lobby_type': 7, 'game_mode': 22, 'avg_rank_tier': 53, 'radiant_team': '135,14,101,44,50', 'dire_team': '40,69,10,64,13'}, 
        {'match_id': 6676192016, 'radiant_win': True, 'start_time': 1658678273, 'duration': 1925, 'lobby_type': 7, 'game_mode': 22, 'avg_rank_tier': 14, 'radiant_team': '50,93,113,86,73', 'dire_team': '75,105,2,37,36'}]
        db = mongomock.MongoClient().db
       
        res = sanitizeMatches(amateur_data, db)
        assert res == expected_response
    

    def test_santize_matches_matching_id(self):
        expected_response = [{'match_id': 6676192018, 'radiant_win': True, 'start_time': 1658678273, 'duration': 2040, 'lobby_type': 7, 'game_mode': 22, 'avg_rank_tier': 53, 'radiant_team': '135,14,101,44,50', 'dire_team': '40,69,10,64,13'}, 
        {'match_id': 6676192016, 'radiant_win': True, 'start_time': 1658678273, 'duration': 1925, 'lobby_type': 7, 'game_mode': 22, 'avg_rank_tier': 14, 'radiant_team': '50,93,113,86,73', 'dire_team': '75,105,2,37,36'}]
        db = mongomock.MongoClient().db
        db['allmatches'].insert_one(data_obj)
        
        res = sanitizeMatches(amateur_data, db)
        print(res)

        assert res == expected_response

    def test_sanitize_matches_pro(self):
        
        db = mongomock.MongoClient().db
        res = sanitizeMatches(pro_data, db)
        expected_res =[{
                    "match_id": 6676192106,
                    "radiant_win": True,
                    "start_time": 1658678273,
                    "duration": 2040,
                    "radiant_name": 'sdf',
                    "dire_name": 'sdf'
                },{
                    "match_id": 123456,
                    "radiant_win": True,
                    "start_time": 1658678273,
                    "duration": 2040,
                    "radiant_name": 'sdf',
                    "dire_name": 'sdf'
                },{
                    "match_id": 123456,
                    "radiant_win": True,
                    "start_time": 1658678273,
                    "duration": 2040,
                    "radiant_name": 'sdf',
                    "dire_name": 'sdf'
                }]
        assert res == expected_res

class TestParse:
    @patch('time.sleep', return_value=None)
    def test_parse(self, patch_time_sleep):
        with requests_mock.Mocker() as m:
            match_id = 123456
            
            m.post(f'https://api.opendota.com/api/request/{match_id}', json={'job': {"jobId": 12}}, status_code=201)
            m.get(f'https://api.opendota.com/api/request/12', json={})
            m.get(f'https://api.opendota.com/api/matches/{match_id}', json={
                "radiant_gold_adv" : 1234,
                'replay_url': 'asdfasdf'
            })

            match = {
                "radiant_gold_adv": None, 
            }

            assert parse(match, match_id) == [True, {"radiant_gold_adv" : 1234, 'replay_url': 'asdfasdf'}]

class TestSanitize:
    @patch('time.sleep', return_value=None)
    def test_sanitize(self, patch_time_sleep):
        match_id = 6676192106
        db = mongomock.MongoClient().db
        with requests_mock.Mocker() as m:
            m.get(f'https://api.opendota.com/api/matches/{match_id}', json=match )

            m.post(f'https://api.opendota.com/api/request/{match_id}', json={'job': {"jobId": 12}}, status_code=201)
            m.get(f'https://api.opendota.com/api/request/12', json={})
            m.get(f'https://api.opendota.com/api/matches/{match_id}', json=match)
            
            
            sanitize(db, amateur_data, [4])
            test_match = list(db["archonmatches_data"].find({}, {"_id": 0}))[0]
            del test_match["players"]
            assert  test_match == sanitized_match 

class TestSanitizePro:
    @patch('time.sleep', return_value=None)
    def test_sanitize_pro_players(self, patch_time_sleep):
        match_id = 6676192106
        db = mongomock.MongoClient().db
        with requests_mock.Mocker() as m:
            
            m.get(f'https://api.opendota.com/api/matches/{match_id}', json=match )
            
            sanitizePro(db, [pro_data[0]])
            test_match = list(db["promatches_data"].find({}, {"_id": 0}))[0]
            print(sanitized_match)
            del test_match["players"], sanitized_match["avg_rank_tier"], test_match["avg_rank_tier"]
            assert  test_match == sanitized_match 
