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
    msg = flask.render_template('confirm_account.txt', 
                                user=user,
                                sender=app.config['MAIL_USERNAME'])
    msg_html = flask.render_template('confirm_account.html', 
                                user=u,
                                sender=app.config['MAIL_USERNAME'])
    mail=send_mail('Welcome to Resume Builder I4G', payload['email'], msg, msg_html)
    if mail:
        return {
            'error': 'Server error',
            'message': mail
        }, 500
    return {
        'message': 'Mail has been successfully sent to your mail for confirming your account',
        'user': u
    }, 201

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
    msg = flask.render_template('reset_password.txt', 
                                token=User().get_reset_token(user),
                                sender=app.config['MAIL_USERNAME'], 
                                user=user)
    msg_html = flask.render_template('reset_password.html', 
                                token=User().get_reset_token(user),
                                sender=app.config['MAIL_USERNAME'], 
                                user=user)
    mail = send_mail('Reset Your password', data['email'], msg, msg_html)
    if mail:
        return {
            'error': 'Server error',
            'message': mail
        }, 500
    return {'message': 'Mail sent successfully', 'user': user}, 200
