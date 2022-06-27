from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

def get_db_handle():
 client = MongoClient(os.getenv('DATABASE_URL'), tlsCAFile=certifi.where())
 db = client.dota2
 return db, client