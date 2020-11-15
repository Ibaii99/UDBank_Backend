import json

class User:
    def __init__(self):
        pass

    def initiate(self, name, mail, passwd, first_name, last_name, address, city, country, postal_code, about):
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

    def jsonify(self):
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
                "about": self.about
                }

    def json_cookie_payload(self):
        return {
                "username": self.username,
                "password": self.password
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



from flask import Response, request
import requests

class Authorization:
    def authorize_user(self, api_key, userId):
        return True
    
    def authorize_front(self, api_key):
        return True