'''Module that handles view of everything that has to do with authN and authZ'''
from werkzeug.security import (generate_password_hash, 
                    check_password_hash)
import flask, jwt
from app import app
from app.models import User
from app.routes.mail_routes import send_mail

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
    u = User().db.find_one({'email': payload['email']})
    if u:
        return flask.jsonify({
            'error': 'Invalid request',
            'message': 'email already taken.'
        }), 400
    u=User().signup(**user)
    msg = f"""From: From Person <{app.config['MAIL_USERNAME']}>
To: To {payload['name']} <{payload['email']}>
MIME-Version: 1.0
Content-type: text/html
Subject: Welcome to Resume Builder I4G

<h1>Hello {payload['name']}</h1>,
Welcome to I4G Resume Builder, we're glad to have you onboard
Click <a href='{flask.url_for('confirm_account', current_user=u, _external=True)}>here</a> to confirm your account
Admin
I4G
"""
    send_mail(payload['email'], msg, 'Welcome to I4G')
    return u, 201

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
        'token': token,
        'user': u
    }), 200

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    head = flask.request.headers.get('Authorization', None)
    if head:
        return {
            'error':'Forbidden',
            'message': 'You are signed in, you can\'t perform that operation'
        }, 403
    user = User().verify_reset_token(token)
    if not user:
        return {
            'error': 'Bad request',
            'message': 'Token is invalid'
        }, 400
    data = flask.request.get_json()
    if data['password'] != data['confirm password']:
        return {
            'error': 'Bad request',
            'message': 'Invalid data'
        }, 400
    user = User().update_profile(current_user['_id'],
                {'password_hash': generate_password_hash(data['password'])}
            )

    return '', 201

@app.route('/get_password_token', methods=['POST'])
def get_token():
    head = flask.request.headers.get('Authorization', None)
    print(head)
    if head:
        return {
            'error':'Forbidden',
            'message': 'You are signed in, you can\'t perform that operation'
        }, 403
    data = flask.request.get_json()
    if 'email' not in data:
        return {
            'error': 'Invalid request',
            'message': 'Email not given'
        }, 400
    user = User().db.find_one({'email': data['email']})
    if not user:
        return {
            'error': 'Invalid request',
            'message': 'Invalid Email'
        }, 400
    msg = f"""From: From Person <{app.config['MAIL_USERNAME']}>
To: To {user['name']} <{data['email']}>
MIME-Version: 1.0
Content-type: text/html
Subject: Welcome to Resume Builder I4G

<h1>Hello {user['name']}</h1>,
Welcome to I4G Resume Builder, we're glad to have you onboard
Click <a href='{flask.url_for('reset_password', token=User().get_reset_token(user), _external=True)}>here</a> to reset your password
Admin
I4G
"""
    mail = send_mail(data['email'], msg, 'Reset Your Password')
    return {'message': 'Mail sent successfully', 'user': user}, 200
