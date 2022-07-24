import mongomock
import requests_mock
from unittest.mock import patch
from functions.data_set import get_data_set, get_pro_data_set
from functions.common import dataAccess
import json

with open('functions/tests/testing_constants/allmatch.json', 'r') as j:
    allmatch = json.loads(j.read())
with open('functions/tests/testing_constants/promatch.json', 'r') as j:
    promatch = json.loads(j.read())
with open('functions/tests/testing_constants/proplayers.json', 'r') as j:
    proplayers = json.loads(j.read())
with open('functions/tests/testing_constants/sanitized_match.json', 'r') as p:
    sanitized_match = json.loads(p.read())
    del sanitized_match["players"],
with open('functions/tests/testing_constants/match.json', 'r') as j:
    match = json.loads(j.read())
with open('functions/tests/testing_constants/players.json', 'r') as j:
    sanitized_players = json.loads(j.read())

class TestDataInsertAndRead:
    
    @patch('time.sleep', return_value=None)
    def testPublicMatch(self, patch_time_sleep):
        db = mongomock.MongoClient().db
        match_id = 6676192106
        with requests_mock.Mocker() as m:
            m.get(f'https://api.opendota.com/api/publicMatches', json=allmatch )
            m.get(f'https://api.opendota.com/api/publicMatches?less_than_match_id=6676192106', json=allmatch )
            m.get(f'https://api.opendota.com/api/matches/{match_id}', json=match )
            m.post(f'https://api.opendota.com/api/request/{match_id}', json={'job': {"jobId": 12}}, status_code=201)
            m.get(f'https://api.opendota.com/api/request/12', json={})
            m.get(f'https://api.opendota.com/api/matches/{match_id}', json=match)
            
            get_data_set(db, [])
            data, rank, read_match, players = dataAccess(db, 6676192106)
            assert data == allmatch[0]
            assert rank == "archon"
            del read_match["players"]
            assert read_match == sanitized_match
            assert players == sanitized_players
    
    @patch('time.sleep', return_value=None)
    def testProMatch(self, patch_time_sleep):
        db = mongomock.MongoClient().db
        match_id = 6676192106
        with requests_mock.Mocker() as m:
            m.get(f'https://api.opendota.com/api/proMatches', json=promatch )
            m.get(f'https://api.opendota.com/api/matches/{match_id}', json=match )
            
            get_pro_data_set(db)
            data, rank, read_match, players = dataAccess(db, 6676192106)
            del promatch[0]["leagueid"]
            assert data == promatch[0]
            assert rank == "pro"
            del read_match["players"], sanitized_match["avg_rank_tier"], read_match["avg_rank_tier"]
            assert read_match == sanitized_match
            assert players == proplayers
