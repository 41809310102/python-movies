from flask import Blueprint, request

api_url_user = Blueprint('/', __name__)


@api_url_user.route("/login", methods=['POST', 'GET'])
def login():
    username = request.args['username']
    print(username)
    return username
