from pymongo import MongoClient
import urllib.parse
import logging
import json
from objects import User
from config import MONGO_HOST, MONGO_PASS, MONGO_PORT, MONGO_USER, MONGO_AUTHENTICATE_DB

class DatabaseEngine:
    def __init__(self):
        # if you are password has '@' then you might need to escape hence we are using "urllib.parse.quote_plus()" 
        client = MongoClient(f'mongodb://{MONGO_USER}:{urllib.parse.quote_plus(MONGO_PASS)}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_AUTHENTICATE_DB}')
        
        db = client.udbank
        
        self.collection_markets = db['markets']
        self.collection_metadata = db['metadata']
        self.collection_users = db['users']

    def get_markets(self):
        return list(self.collection_markets.find())
    
    def get_market_by_code(self, code: str):
        return list(self.collection_markets.find({"code": code}))
    
    def save_user(self, user: User):
        try:
            if (len(list(self.collection_users.find({"username": user.username})))==0):
                self.collection_users.insert_one(user.jsonify())
                return True
            return False
        except:
            return False

    def get_user(self, username: str, password: str):
        try:
            user = self.collection_users.find_one({"username": username, "password": password})
            if user is not None:
                u = User()
                u.load_json(user)
                return u
            else:
                return False
        except:
            return False

    def modify_user(self, username: str, password: str, user: User):
        self.collection_users.update_one({"username": username, "password": password}, { "$set": user.jsonify() })
