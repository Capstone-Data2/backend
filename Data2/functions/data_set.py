from pymongo import MongoClient
import requests
import os
import time
from dotenv import load_dotenv
from sanitize import sanitize

load_dotenv()
client = MongoClient(os.getenv('DATABASE_URL'))
lobby_types = [5, 6, 7]
db = client.dota2

def get_data_set(filter):
    response = requests.get(f'https://api.opendota.com/api/publicMatches').json()
    max_match = response[len(response)-1]
    response = requests.get(f'https://api.opendota.com/api/publicMatches?less_than_match_id={max_match["match_id"]}').json()
    sanitize(response, filter)

get_data_set([])
