from app import app
import flask
from app.routes import token_required
from app.models import Language, User

@app.route('/languages', methods=['POST'])
@token_required
def create_language():
    payload = flask.request.get_json()
    if 'name' not in payload or 'proficiency' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid email or password'
        }), 400
    payload = {
        'name': payload['name'], 'proficiency': payload['proficiency'],
        'user_id': current_user._id
    }
    l=Language().create_language(**payload)
    return l, 200

@app.route('/languages/<id>', methods=['DELETE'])
@token_required
def delete_language(id):
    Language().delete_language(id)
    return '', 204

@app.route('/languages/<id>', methods=['PUT'])
@token_required
def edit_hobby(id):
    from bson.json_util import dumps
    if 'name' not in payload or 'proficiency' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'name or proficiency not defined'
        }), 400
    h = dumps(Language().db.find_one({
        'user_id': current_user._id, 'name': payload['name']
        })) if 'name' in payload else None
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that name already exist for the user'
        }), 400
    return Language().edit_language(id, payload)