from flask import Blueprint, Response, request, abort, jsonify
from flask_cors import cross_origin

import requests
import logging
import json
import jwt

from controllers.users_controller import UsersController

from controllers.sessions_controller import SessionsController

from utils import HASH
from config import JWT_SIGN_KEY
from logic.user import User

from logic.authorization import Authorization

users_blueprint = Blueprint("user", __name__)

users_db = UsersController()
sessions_db = SessionsController()

@users_blueprint.route("/", methods=["GET"])
def echo():
    return ("User module")

@users_blueprint.route("/login", methods=["POST"])
@cross_origin()
def login():
    logging.warning('Log in:')
    username = request.json.get('username')
    password = request.json.get('password')
    is_correct = Authorization.check_password(username, password)
    if is_correct:
        u = users_db.get(username)
        if u:
            Authorization.save_session(u)
            return jsonify({ 'Authorization' : encode(u.json_cookie_payload()), "Message": "Logged in"}), 200
    abort(401)


@users_blueprint.route("/logout", methods=["DELETE"])
@cross_origin()
def logout():
    logging.warning("Logout:")
    removed = Authorization.remove_session(request)
    if removed:
        return jsonify({"Message": "Logged out"}), 200
    abort(401)



@users_blueprint.route("/register", methods=["POST"])
@cross_origin()
def register():
    u = User()
    u.load_json(request.json)
    u.password = HASH.hash(u.password)
    cookie = users_db.save(u)
    if cookie:
        sessions_db.save(u.json_cookie_payload())
        return jsonify({ 'Authorization' : encode(u.json_cookie_payload()), "Message": "Registered"}), 200
    abort(401)

@users_blueprint.route("/info", methods=["POST"])
def modify_user():
    u = check_token(request)
    if u:
        new_u_json = get_new_token_decoded(request)
        if new_u_json:
            u2 = User()
            u2.load_json(new_u_json)
            user_new = users_db.modify(u.username,u.password, u2)
            return u2.jsonify()
    abort(401)


# @users_blueprint.route("/info", methods=["GET"])
# def get_user():
#     u = check_token(request)
#     if u:
#         return u.jsonify()
#     abort(401)

def encode(token):
    return jwt.encode(token, JWT_SIGN_KEY , algorithm='HS256').decode('utf-8')


def get_authorization_token_decoded(request):
    encoded_token = get_encoded_token(request)
    logging.warning(encoded_token)
    if encoded_token:
        decoded_token = decode_token(encoded_token)
        if decoded_token:
            return decoded_token
        else:
            return False

def get_encoded_token(request):
    auth_header = request.headers.get('Authorization')
    logging.warning(request.headers)
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

# def check_token(request):
#     token = get_authorization_token_decoded(request)
#     return db.get_user(token["username"], token["password"])

# def get_new_token_decoded(request):
#     encoded_token = get_new_encoded_data(request)
#     if encoded_token:
#         decoded_token = decode_token(encoded_token)
#         if decoded_token:
#             return decoded_token
#         else:
#             return False

# def get_new_encoded_data(request):
#     auth_header = request.headers.get('New-Authorization')
#     if auth_header:
#         try:
#             auth_token = auth_header.split(" ")[1]
#         except IndexError:
#             responseObject = {
#                 'status': 'fail',
#                 'message': 'Bearer token malformed.'
#             }
#             return abort(403)
#     else:
#         auth_token = ''

#     if auth_token:
#         return auth_token
#     else:
#         return abort(403)



    
