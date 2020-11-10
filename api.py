from flask import Flask, Blueprint, abort, request, Response
from routing import markets, users
import config
import logging

from objects import Authorization

app = Flask(__name__)
app.register_blueprint(markets.markets_blueprint, url_prefix=config.API_URL_PREFIX+"/market")
app.register_blueprint(users.users_blueprint, url_prefix=config.API_URL_PREFIX + "/user")

auth = Authorization()

@app.route('/')
def hello():
    return "Hello World!"

@app.before_request
def check_api_key():
    logging.warning("BEFORE")
    api_key = request.headers.get("X-Api-Key")
    userId = request.headers.get("user-id")
    if (api_key is not None and userId is not None):
        if not auth.authorize(api_key, userId):  
            abort(403)
    else:
        abort(403)

@app.after_request
def save_history(response):
    logging.warning("After")
    # logging.warning(response)
    # logging.warning(request)
    # logging.warning(request.headers)
    # logging.warning(request.cookies)
    # logging.warning(request.args)
    # logging.warning(request.url_rule)   
    return response





@app.errorhandler(403)
def page_not_found(e):
    return "Forbbiden acces, invalid api-key", 403

@app.errorhandler(401)
def page_not_found(e):
    return "Incorrect username or password", 401

if __name__ == '__main__':
    app.run(debug= True, host= config.HOST, port=config.PORT)

