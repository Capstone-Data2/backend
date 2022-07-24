import requests
from functions.sanitize import sanitize, sanitizePro

def get_data_set(db, filter):
    response = requests.get(f'https://api.opendota.com/api/publicMatches').json()
    max_match = response[len(response)-1]
    response = requests.get(f'https://api.opendota.com/api/publicMatches?less_than_match_id={max_match["match_id"]}').json()
    sanitize(db, response, filter)

def get_pro_data_set(db):
    response = requests.get(f'https://api.opendota.com/api/proMatches').json()
    sanitizePro(db, response)

