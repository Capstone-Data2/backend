from pymongo import MongoClient
import requests
import os
from dotenv import load_dotenv
from sanitize import sanitize

load_dotenv()
client = MongoClient(os.getenv('DATABASE_URL'))
lobby_types = [5, 6, 7]
db = client.dota2

def get_data_set():
    response = requests.get(f'https://api.opendota.com/api/publicMatches').json()
    sanitize(response)

get_data_set()
