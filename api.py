from flask import Flask, Blueprint, abort, request, Response, jsonify
from flask_cors import CORS, cross_origin

import json
from routing import markets, users
import config
import logging

from objects import Authorization

app = Flask(__name__)
app.register_blueprint(markets.markets_blueprint, url_prefix=config.API_URL_PREFIX+"/market")
app.register_blueprint(users.users_blueprint, url_prefix=config.API_URL_PREFIX + "/user")

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'






auth = Authorization()

@app.route('/', methods=["GET"])
@cross_origin()
def hello():
    return "Hello World!"

@app.before_request
def check_api_key():
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers
        
        return resp
    else:
        logging.warning("BEFORE")
        logging.warning(request.headers)
        api_key = request.headers.get("X-Api-Key")
        userId = request.headers.get("user-id")
        if (api_key is not None and userId is not None):
            if not auth.authorize_user(api_key, userId):  
                abort(403)
        elif (api_key is not None and userId is None):
            if not auth.authorize_front(api_key):
                abort(403)
        elif (api_key is None and userId is None):
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
    return jsonify(json.dumps("Forbbiden acces, invalid api-key")), 403

@app.errorhandler(401)
def page_not_found(e):
    return jsonify(json.dumps("Incorrect username or password")), 401

if __name__ == '__main__':
    app.run(debug=True, host=config.HOST, port=config.PORT)

