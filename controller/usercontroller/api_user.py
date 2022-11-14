import json

from flask import Blueprint, request

api_url_user = Blueprint('/', __name__)


@api_url_user.route("/login", methods=['POST', 'GET'])
def login():
    username = request.args['username']
    password = request.args['password']
    res = {
        'code': 0,
        "msg": "success"
    }
    return json.dumps(res)
