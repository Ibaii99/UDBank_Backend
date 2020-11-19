from bson import ObjectId
import datetime
import json
import hashlib
from config import SALT
import logging
import jwt
from config import JWT_SIGN_KEY
from flask import request


class MongoJSONEncoder(json.JSONEncoder):
    @staticmethod
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

class HASH():
    @staticmethod
    def hash(data):
        key = hashlib.pbkdf2_hmac(
                                    'sha256', # The hash digest algorithm for HMAC
                                    data.encode('utf-8'), # Convert the password to bytes
                                    SALT, # Provide the salt
                                    100000, # It is recommended to use at least 100,000 iterations of SHA-256 
                                    dklen=128 # Get a 128 byte key
                                )
        return key

class COOKIE_MANAGER():
    
    @staticmethod
    def get_authorization_token_decoded(request: request):
        encoded_token = COOKIE_MANAGER.get_encoded_token(request)
        if encoded_token:
            decoded_token = COOKIE_MANAGER.decode_token(encoded_token)
            if decoded_token:
                return decoded_token
            else:
                return False
    
    @staticmethod
    def get_encoded_token(request: request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return False
        else:
            auth_token = ''

        if auth_token:
            return auth_token
        else:
            return False
    
    @staticmethod
    def decode_token(token):
        token = jwt.decode(token, JWT_SIGN_KEY, algorithms=['HS256'])
        if not isinstance(token, str):    
            return token
        return False
