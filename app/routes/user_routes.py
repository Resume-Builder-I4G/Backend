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
    avatar_name = save_pic(flask.request.files['avatar']) \
            if flask.request.files['avatar'] else None
    if type(avatar_name) == dict and 'error' in avatar_name or not avatar:
        return {
            'error': 'Bad request',
            'message': avatar_name['message']
        }, 400
    data['image_path'] = flask.request.host_url+'static/'+avatar_name
    User().update_profile(current_user['_id'], **data)
    return flask.redirect(
        flask.url_for('get_user', current_user=current_user)
        ), 201

@app.route('/')
def home():
    return flask.redirect('https://www.postman.com/collections/11d9c8bcd44db2b4040c')

@app.route('/confirm', methods=['POST'])
@token_required
def confirm_account(current_user):
    user = User().update_profile(current_user['_id'], {'is_confirmed': True})
    return user, 201

@app.route('/templates', methods=['POST'])
@token_required
def template(current_user):
    template = flask.request.get_json()['template']
    if not template:
        return {
            'error': 'Invalid request',
            'message': 'Template not given'
        }, 400
    User().update_profile(current_user['_id'], {'template': template})
    