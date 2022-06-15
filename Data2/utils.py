from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_handle():
 client = MongoClient(os.getenv('DATABASE_URL'))
 db = client.dota2
 return db, client