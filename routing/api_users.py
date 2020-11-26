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

from utils import COOKIE_MANAGER
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
    username = request.json.get('username')
    password = request.json.get('password')
    is_correct = Authorization.check_password(username, HASH.hash(password))
    if is_correct:
        u = users_db.get(username)
        if u:
            Authorization.save_session(u)
            return jsonify({ 'Authorization' : encode(u.json_cookie_payload()), "Message": "Logged in"}), 200
    abort(401)


@users_blueprint.route("/logout", methods=["DELETE"])
@cross_origin()
def logout():
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
        Authorization.save_session(u)
        return jsonify({ 'Authorization' : encode(u.json_cookie_payload()), "Message": "Registered"}), 200
    abort(401)

@users_blueprint.route("/info", methods=["GET"])
@cross_origin()
def get_user():
    session_cookie = COOKIE_MANAGER.get_authorization_token_decoded(request)
    if session_cookie:
        session = sessions_db.get(session_cookie)
        if session:
            user = users_db.get(session_cookie.get("username"))
            if user:
                return jsonify(json.dumps(user.safe_jsonify())), 200
    abort(401)

@users_blueprint.route("/info", methods=["POST"])
@cross_origin()
def modify_user():
    logging.warning("llega")
    session_cookie = COOKIE_MANAGER.get_authorization_token_decoded(request)
    if session_cookie:
        session = sessions_db.get(session_cookie)
        if session:
            user = users_db.get(session_cookie.get("username"))
            if user:    
                user2 = User()
                request.get_json()["password"] = user.password
                user2.load_json(request.get_json())
                modify = users_db.modify(user.username, user.password, user2)
                if modify:
                    removed = Authorization.remove_session(request)
                    if removed:       
                        Authorization.save_session(user2)
                    return jsonify({ 'Authorization' : encode(user2.json_cookie_payload()), "Message": "Modified"}), 200

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



    
