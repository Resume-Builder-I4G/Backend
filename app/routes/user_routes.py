'''Module that handles view of everything that has to do with CRUD of the user'''
from app import app
from app.models import *
import flask
from werkzeug.security import generate_password_hash
from app.routes import token_required
from app.routes.image_saver import save_pic

@app.route('/user')
@token_required
def get_user(current_user):
    user = User().get_user(current_user['_id'])
    user['skills'] = Skill().get_user_skills(current_user['_id'])
    user['education'] = Education().get_user_educations(current_user['_id'])
    user['languages'] = Language().get_user_languages(current_user['_id'])
    user['experiences'] = WorkExperience().get_user_experiences(current_user['_id'])
    user['achievements'] = Achievement().get_user_achievements(current_user['_id'])
    user['certificates'] = Certificate().get_user_certificates(current_user['_id'])
    return flask.jsonify(user)

@app.route('/user', methods=['PUT'])
@token_required
def update_user(current_user):
    data = dict(flask.request.form)
    avatar_name = save_pic(flask.request.files['avatar'])
    if type(avatar_name) == dict and 'error' in avatar_name:
        return {
            'error': 'Bad request',
            'message': avatar_name['message']
        }, 400
    data['image_path'] = flask.request.host_url+'static/'+avatar_name
    return {
        **data
        }, 201

@app.route('/users')
def users():
    return flask.jsonify(User().get_users())

@app.route('/confirm', methods=['POST'])
@token_required
def confirm_account(current_user):
    user = User().db.find_one_and_update(current_user, {'$set': {'is_confirmed': True}})
    print(user)
    return user, 201

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
    user = User().db.find_one_and_update(
            user, 
            {'$set': 
                {'password_hash': generate_password_hash(data['password'])}
            })
    print(user)
    return user, 201

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
    return {'token': User().get_reset_token(user), 'user': user}, 200

    