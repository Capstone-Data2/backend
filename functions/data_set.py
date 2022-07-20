import requests
from functions.sanitize import sanitize, sanitizePro
from utils import get_db_handle

db, client = get_db_handle()
lobby_types = [5, 6, 7]

def get_data_set(filter):
    response = requests.get(f'https://api.opendota.com/api/publicMatches').json()
    max_match = response[len(response)-1]
    response = requests.get(f'https://api.opendota.com/api/publicMatches?less_than_match_id={max_match["match_id"]}').json()
    sanitize(response, filter)

def get_pro_data_set():
    response = requests.get(f'https://api.opendota.com/api/proMatches').json()
    sanitizePro(response)

