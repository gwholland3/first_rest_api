from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = {
    'users_list':
        [
            {
                'id': 'xyz789',
                'name': 'Charlie',
                'job': 'Janitor',
            },
            {
                'id': 'abc123',
                'name': 'Mac',
                'job': 'Bouncer',
            },
            {
                'id': 'ppp222',
                'name': 'Mac',
                'job': 'Professor',
            },
            {
                'id': 'yat999',
                'name': 'Dee',
                'job': 'Aspiring actress',
            },
            {
                'id': 'zap555',
                'name': 'Dennis',
                'job': 'Bartender',
            }
        ]
}


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        if len(request.args) > 0:
            subdict = {'users_list': []}
            for user in users['users_list']:
                if is_match(user):
                    subdict['users_list'].append(user)
            return subdict
        return users
    elif request.method == 'POST':
        user_to_add = request.get_json()
        users['users_list'].append(user_to_add)
        resp = jsonify(success=True, status_code=201)
        # 201 = content created
        return resp


def is_match(user):
    supported_filters = ['name', 'job']

    for filter in request.args.keys():
        if filter in supported_filters and user[filter] != request.args.get(filter):
            return False
    return True


@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        if id:
            for user in users['users_list']:
                if user['id'] == id:
                    return user
            return {}
        return users
    elif request.method == 'DELETE':
        if id:
            for user in users['users_list']:
                if user['id'] == id:
                    users['users_list'].remove(user)
                    resp = jsonify(success=True, status_code=200)
                    return resp
            resp = jsonify(success=False, status_code=404)
            return resp
        resp = jsonify(success=False, status_code=400)
        return resp
