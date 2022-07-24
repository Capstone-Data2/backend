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
