from flask import Blueprint, Response, request, abort
import requests
import logging
import json
import jwt

from database_engine import DatabaseEngine
from utils import MongoJSONEncoder

from config import JWT_SIGN_KEY

from objects import User

users_blueprint = Blueprint("user", __name__)
db = DatabaseEngine()
json_encoder = MongoJSONEncoder()

@users_blueprint.route("/", methods=["GET"])
def echo():
    return ("User module")

@users_blueprint.route("/login", methods=["GET"])
def login():
    u = check_token(request)
    if u:
        return u.json_cookie_payload()
    abort(401)

@users_blueprint.route("/register", methods=["POST"])
def register():
    token = get_authorization_token_decoded(request)
    u = User()
    u.load_json(token)
    cookie = db.save_user(u)
    if cookie:
        return u.json_cookie_payload()
    abort(401)

@users_blueprint.route("/info", methods=["GET"])
def get_user():
    u = check_token(request)
    if u:
        return u.jsonify()
    abort(401)

@users_blueprint.route("/info", methods=["POST"])
def modify_user():
    u = check_token(request)
    if u:
        new_u_json = get_new_token_decoded(request)
        if new_u_json:
            u2 = User()
            u2.load_json(new_u_json)
            user_new = db.modify_user(u.username,u.password, u2)
            return u2.jsonify()
    abort(401)

def check_token(request):
    token = get_authorization_token_decoded(request)
    return db.get_user(token["username"], token["password"])

def get_authorization_token_decoded(request):
    encoded_token = get_encoded_token(request)
    if encoded_token:
        decoded_token = decode_token(encoded_token)
        if decoded_token:
            return decoded_token
        else:
            return False

def get_encoded_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return abort(403)
    else:
        auth_token = ''

    if auth_token:
        return auth_token
    else:
        return abort(403)


def get_new_token_decoded(request):
    encoded_token = get_new_encoded_data(request)
    if encoded_token:
        decoded_token = decode_token(encoded_token)
        if decoded_token:
            return decoded_token
        else:
            return False

def get_new_encoded_data(request):
    auth_header = request.headers.get('New-Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return abort(403)
    else:
        auth_token = ''

    if auth_token:
        return auth_token
    else:
        return abort(403)

def decode_token(token):
    token = jwt.decode(token, JWT_SIGN_KEY, algorithms=['HS256'])
    if not isinstance(token, str):    
        return token
    return False
