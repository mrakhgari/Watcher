from flask import Flask
from directory import configs

import requests


app = Flask(__name__)


@app.route('/accounts/', methods=['GET'])
def get_users():
    response = requests.get(f'{configs.DB_API_URL}/users/')
    return response.json(), response.status_code
                        

@app.route('/tweets/<string:username>/', methods=["GET"])
def get_conversations(username):
    response = requests.get(f'{configs.DB_API_URL}/tweets/conversations/{username}/')
    return response.json(), response.status_code


@app.route('/tweets/<string:username>/<string:conversation_id>/', methods=['GET'])
def get_conversation(username, conversation_id):
    response = requests.get(f'{configs.DB_API_URL}/tweets/conversations/{username}/{conversation_id}')
    return response.json(), response.status_code


