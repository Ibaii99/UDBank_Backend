from flask import Blueprint, Response, request, jsonify
import requests
import logging
import json

from controllers.markets_controller import MarketsController
from utils import MongoJSONEncoder

import config

markets_blueprint = Blueprint("market", __name__)
    
headers = {"X-Finnhub-Token": config.FINNHUB_API_KEY}
url = "https://finnhub.io/api/v1/stock"

markets_db = MarketsController()

@markets_blueprint.route("/info/<brand>", methods=["GET"])
def get_brand_info(brand):
    return requests.get(url + "/profile2", headers=headers, params={'symbol': brand}).json()

@markets_blueprint.route("/<exchange>/stocks", methods=["GET"])
def get_all_stocks_from_market(exchange):
    r = requests.get(url + "/symbol", headers=headers, params={'exchange': exchange})
    return jsonify(json.dumps(r.json()))

@markets_blueprint.route("/exchanges", methods=["GET"])
def get_all_markets():
    return MongoJSONEncoder.encode(markets_db.get_all())
    
@markets_blueprint.route("/", methods=["GET"])
def echo():
    return ("Market module")

