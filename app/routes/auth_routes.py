'''Module that handles view of everything that has to do with authN and authZ'''
from werkzeug.security import (generate_password_hash, 
                    check_password_hash)
import flask, jwt
from app import app
from app.models import User

@app.route('/auth/signup', methods=['POST'])
def signup():
    payload = flask.request.get_json()
    print(payload)
    if not payload['name'] or not payload['email'] or  not payload['password']:
        return flask.jsonify({
            'error': 'Invalid request',
            'message': 'Name, or email or password wasn\'t given.'
        }), 400
    user = {
        'name': payload['name'],
        'email': payload['email'],
        'password_hash': generate_password_hash(payload['password'])
    }
    u=User().signup(**user)
    return u, 200

@app.route('/auth/signin', methods=['POST'])
def signin():
    payload = flask.request.get_json()
    if not payload['email'] or not payload['password']:
        return flask.jsonify({
            'error': 'Invalid request',
            'message': 'Email or password wasn\'t given.'
        }), 400
    details = {
        'email': payload['email'],
        'password': payload['password']
    }
    u=User().signin(**details)
    if 'error' in u:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid email or password'
        }), 400

    token = jwt.encode({'user': u}, app.config['SECRET_KEY'])
    return flask.jsonify({
        'token': token.decode('utf-8'),
        'user': u
    }), 200