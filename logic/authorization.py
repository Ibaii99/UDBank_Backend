from flask import Response, request
import requests

class Authorization:
    # db = DatabaseEngine()

    @staticmethod
    def authorize_user(cookie):
        # 28800 = 8h
        
        return True

    @staticmethod
    def check_password(username, password):
        # return self.db.is_password_correct(username, HASH.hash(password))
        return True

    @staticmethod
    def authorize_front(api_key):
        return True