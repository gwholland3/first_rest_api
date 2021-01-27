from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

import random
import string

from model_mongodb import User

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
        # search_username = request.args.get('name')
        # search_job = request.args.get('job')
        # if search_username and search_job:
        #     return find_users_by_name_job(search_username, search_job)  # not converted to DB access yet
        # elif search_username:
        #     # return find_users_by_name(search_username) #old code left here for comparuson
        #     users = User().find_by_name(search_username)
        # else:
        #     users = User().find_all()
        users = User().find_by_queries(request.args)
        return {"users_list": users}
    elif request.method == 'POST':
        user_to_add = request.get_json()
        # user_to_add['id'] = generate_random_id()
        # users['users_list'].append(user_to_add)
        # status = {'success': True, 'status_code': 201}
        # resp = jsonify(status, user_to_add)
        new_user = User(user_to_add)
        new_user.save()
        resp = jsonify(new_user), 201
        # 201 = content created
        return resp


@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        if id:
            user = User({"_id": id})
            if user.reload():
                return user
            else:
                resp = jsonify(error="User not found"), 404
                return resp
        resp = jsonify(success=False), 400
        return resp
    elif request.method == 'DELETE':
        if id:
            user = User({"_id": id})
            if user.remove() > 0:
                resp = jsonify(), 204
                return resp
            resp = jsonify(error="User not found"), 404
            return resp
        resp = jsonify(success=False), 400
        return resp
