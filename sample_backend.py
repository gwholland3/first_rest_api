from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

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
        search_username = request.args.get('name')  # Accessing the value of parameter 'name'
        if search_username:
            subdict = {'users_list': []}
            for user in users['users_list']:
                if user['name'] == search_username:
                    subdict['users_list'].append(user)
            return subdict
        return users
    elif request.method == 'POST':
        userToAdd = request.get_json()
        users['users_list'].append(userToAdd)
        resp = jsonify(success=True, status_code=200)
        # Optionally, you can always set a response code.
        # 200 is the default code for a normal response
        return resp


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
