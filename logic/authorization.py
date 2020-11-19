from flask import Response, request
import requests
import datetime
import logging

from controllers.users_controller import UsersController
from controllers.sessions_controller import SessionsController
from utils import COOKIE_MANAGER
from logic.user import User

class Authorization:

    @staticmethod
    def authorize_user_token(request):
        users = UsersController()
        sessions = SessionsController()
        session_cookie = COOKIE_MANAGER.get_authorization_token_decoded(request)
        if session_cookie:
            session = sessions.get(session_cookie)
            if session:
                diff = abs(float(session.get('timestamp')) - float(datetime.datetime.now().timestamp()))
                logging.warning(diff)
                if diff > 28800:
                    remove = sessions.remove(session)
                    return False
                return True
        return False

    @staticmethod
    def save_session(user: User):
        sessions = SessionsController()
        if user:
            sessions.save(user.json_cookie_payload())
        return False

    @staticmethod
    def remove_session(request):
        sessions = SessionsController()
        session_cookie = COOKIE_MANAGER.get_authorization_token_decoded(request)
        session = sessions.get(session_cookie)
        if session:
            remove = sessions.remove(session_cookie)
            if remove:
                return True
            return False
        return True


    @staticmethod
    def check_password(username, password):
        users = UsersController()
        return users.is_password_correct(username, password)

    @staticmethod
    def authorize_front(api_key):
        return True