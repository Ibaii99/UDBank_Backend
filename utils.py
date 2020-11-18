from bson import ObjectId
import datetime
import json
import hashlib
from config import SALT


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