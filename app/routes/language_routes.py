'''Module that handles view of everything that has to do with language of the  user'''
from app import app
import flask
from app.routes import token_required
from app.models import Language

@app.route('/languages')
@token_required
def get_languages(current_user):
    return flask.jsonify(
        Language().get_user_languages(current_user['_id'])
    )

@app.route('/languages/<id>')
@token_required
def get_language(current_user):
    return flask.jsonify(
        Language().get_language(id)
    )

@app.route('/languages', methods=['POST'])
@token_required
def create_language(current_user):
    payload = flask.request.get_json()
    if 'name' not in payload or 'proficiency' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid email or password'
        }), 400
    payload = {
        'name': payload['name'], 'proficiency': payload['proficiency'],
        'user_id': current_user['_id']
    }
    l=Language().create_language(**payload)
    return flask.jsonify(payload), 201

@app.route('/languages/<id>', methods=['DELETE'])
@token_required
def delete_language(current_user, id):
    Language().delete_language(id)
    return '', 204

@app.route('/languages/<id>', methods=['PUT'])
@token_required
def edit_language(current_user, id):
    if 'name' not in payload or 'proficiency' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'name or proficiency not defined'
        }), 400
    h = Language().db.find_one({
        'user_id': current_user['_id'], 'name': payload['name']
        }) if 'name' in payload else None
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that language already exist for the user'
        }), 400
    Language().edit_language(id, payload)
    return '', 204