'''Module that handles view of everything that has to do with achievement of the  user'''
from app import app
from app.models import Achievement
import flask
from app.routes import token_required

@app.route('/achievement')
@token_required
def get_achievements(current_user):
    return flask.jsonify(
        Achievement().get_user_achievements(current_user['_id'])
        )

@app.route('/achievement/<id>')
@token_required
def get_achievement(current_user, id):
    return flask.jsonify(
        Achievement().get_achievement(id)
        )

@app.route('/achievement', methods=['POST'])
@token_required
def create_achievement(current_user):
    payload = flask.request.get_json()
    payload['user_id'] = current_user['_id']
    a=Achievement().create_achievement(**payload)
    return a, 201

@app.route('/achievement/<id>', methods=['DELETE'])
@token_required
def delete_achievement(current_user, id):
    Achievement().delete_achievement(id)
    return '', 204


@app.route('/achievement/<id>', methods=['PUT'])
@token_required
def edit_achievement(current_user, id):
    payload = flask.request.get_json()
    if 'course' not in payload or 'school' not in payload:
        return flask.jsonify({
            'error': 'Bad request'
        }), 400
    h = Achievement().db.find_one({
        'user_id': current_user['_id'], 'course': payload['course']
        }) if 'course' in payload else None
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that name already exist for the user'
        }), 400
    a=Achievement().edit_achievement(id, payload)
    return a, 201