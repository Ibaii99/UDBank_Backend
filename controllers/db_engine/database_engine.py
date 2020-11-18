from pymongo import MongoClient
import urllib.parse
import datetime
import logging
import json
from logic.user import User
from config import MONGO_HOST, MONGO_PASS, MONGO_PORT, MONGO_USER, MONGO_AUTHENTICATE_DB
from utils import HASH

class DatabaseEngine:
    def __init__(self):
        # if you are password has '@' then you might need to escape hence we are using "urllib.parse.quote_plus()" 
        client = MongoClient(f'mongodb://{MONGO_USER}:{urllib.parse.quote_plus(MONGO_PASS)}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_AUTHENTICATE_DB}')
        
        db = client.udbank
        
        self.collection_markets = db['markets']
        self.collection_metadata = db['metadata']
        self.collection_users = db['users']
        self.collection_sessions = db['sessions']


    def get_markets(self):
        return list(self.collection_markets.find())
    
    def get_market_by_code(self, code: str):
        return list(self.collection_markets.find({"code": code}))   

    
    
    def is_password_correct(self, username: str, password:str):
        try:
            user = self.collection_users.find_one({"username": username, 'password':password})
            if user is not None:
                return True 
            else:
                return False
        except:
            return False

    def save_user(self, user: User):
        try:
            if (len(list(self.collection_users.find({"username": user.username})))==0):
                self.collection_users.insert_one(user.jsonify())
                return True
            return False
        except:
            return False

    def get_user(self, username: str):
        try:
            user = self.collection_users.find_one({"username": username})
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


    
    def save_session(self, session_data):
        _session_hash = session_data["session_id"]
        _username = session_data["username"]
        timestamp = datetime.datetime.now().timestamp()
        session= {
            'username': HASH.hash(_username),
            'session_id': HASH.hash(_session_hash),
            'timestamp': timestamp
        }
        self.collection_sessions.insert_one(session)

        return session
    
    def remove_session(self, session_data):
        removed = self.collection_sessions.delete_one({"session_id": session_data["session_id"], "username": session_data["username"]})
        if removed:
            return True
        return False

    def get_session(self, session):
        s = self.collection_sessions.find_one({"username": session["username"], "session_id": session["session_id"]})
        if s is not None:
            return s
        else:
            return False