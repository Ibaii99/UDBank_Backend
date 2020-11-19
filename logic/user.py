import json
import uuid
from utils import HASH

class User:
    def __init__(self):
        self.id = ""
        self.username= ""
        self.email= ""
        self.password= ""
        self.first_name= ""
        self.last_name= ""
        self.address= ""
        self.city= ""
        self.country= ""
        self.postal_code= ""
        self.about = ""
        self.interested_in= []

    def initiate(self, name, mail, passwd, first_name, last_name, address, city, country, postal_code, about, interests):
        self.id = str(uuid.uuid1())
        self.username= name
        self.email= mail
        self.password= passwd
        self.first_name= first_name
        self.last_name= last_name
        self.address= address
        self.city= city
        self.country= country
        self.postal_code= postal_code
        self.about = about
        self.interested_in= interests

    def jsonify(self):
        return {
                "id": self.id,
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "address": self.address,
                "city": self.city,
                "country": self.country,
                "postal_code": self.postal_code,
                "about": self.about,
                "interested_in": self.interested_in
                }

    def json_cookie_payload(self):
        return {
                "username": self.username,
                "session_id": self.id
                }

    def __repr__(self):
        return {
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "address": self.address,
                "city": self.city,
                "country": self.country,
                "postal_code": self.postal_code,
                "about": self.about,
                }

    def load_json(self, json):
        self.id = str(uuid.uuid1())
        self.username= json["username"]
        self.email= json["email"]
        self.password= json["password"]
        self.first_name= json["first_name"]
        self.last_name= json["last_name"]
        self.address= json["address"]
        self.city= json["city"]
        self.country= json["country"]
        self.postal_code= json["postal_code"]
        self.about = json["about"]
        try:
            self.interested_in = json["interested_in"]
        except:
            self.interested_in = []
