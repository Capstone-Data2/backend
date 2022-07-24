from rest_framework.test import APITestCase
import json

match_id = '6672384255'

class TestLog(APITestCase):
    def testLogGetResponse(self):
        
        response = self.client.get(f'/matches/{match_id}/log')
        content = response.data
        file_path = 'matches/tests/responses/log.json'
        
        with open(file_path, 'r') as j:
            expected_response = json.loads(j.read())
        assert content == expected_response

class TestPerformance(APITestCase):
    def testPerformanceGetResponse(self):
        response = self.client.get(f'/matches/{match_id}/performance')
        content = response.data
        print(content)
        file_path = 'matches/tests/responses/performance.json'
        
        with open(file_path, 'r') as j:
            expected_response = json.loads(j.read())
            
        assert content == expected_response

class TestRivals(APITestCase):
    def testRivalsGetResponse(self):
        response = self.client.get(f'/matches/6616044912/rivals/69')
        content = response.data
        print(content)
        file_path = 'matches/tests/responses/rivals.json'
        
        with open(file_path, 'r') as j:
            expected_response = json.loads(j.read())
            
        assert content == expected_response

class TestMatch(APITestCase):
    def testMatchGetResponse(self):
        response = self.client.get(f'/matches/6616044912')
        content = response.data
        print(content)
        file_path = 'matches/tests/responses/match.json'
        
        with open(file_path, 'r') as j:
            expected_response = json.loads(j.read())
        del content["time_difference"], expected_response["time_difference"]
        assert content == expected_response

class TestItems(APITestCase):
    def testItemsGetResponse(self):
        response = self.client.get(f'/matches/6616044912/items')
        content = response.data
        file_path = 'matches/tests/responses/items.json'
        
        with open(file_path, 'r') as j:
            expected_response = json.loads(j.read())
        assert content == expected_response

class GraphData(APITestCase):
    def testGraphDataGetResponse(self):
        response = self.client.get(f'/matches/6616044912/graphdata')
        content = response.data
        file_path = 'matches/tests/responses/graphdata.json'
        
        with open(file_path, 'r') as j:
            expected_response = json.loads(j.read())
        assert content == expected_response

class WardData(APITestCase):
    def testWardDataGetResponse(self):
        response = self.client.get(f'/matches/6616044912/warddata')
        content = response.data
        file_path = 'matches/tests/responses/warddata.json'
        
        with open(file_path, 'r') as j:
            expected_response = json.loads(j.read())
        assert content == expected_response

class CombatData(APITestCase):
    def testWardDataGetResponse(self):
        response = self.client.get(f'/matches/6616044912/combatdata')
        content = response.data
        file_path = 'matches/tests/responses/combatdata.json'
        
        with open(file_path, 'r') as j:
            expected_response = json.loads(j.read())
        assert content == expected_response