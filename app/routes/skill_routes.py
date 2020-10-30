from app import app
import flask
from app.routes import token_required
from app.models import Skill, User

@app.route('/skills', methods=['POST'])
@token_required
def create_skill():
    payload = flask.request.get_json()
    if 'name' not in payload or 'level' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid email or password'
        }), 400
    payload = {
        'name': payload['name'], 'level': payload['level'],
        'user_id': current_user._id
    }
    s=Skill().create_skill(**payload)
    return s, 200

@app.route('/skills/<id>', methods=['DELETE'])
@token_required
def delete_skill(id):
    Skill().delete_skill(id)
    return '', 204

@app.route('/languages/<id>', methods=['PUT'])
@token_required
def edit_hobby(id):
    from bson.json_util import dumps
    if 'name' not in payload or 'level' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'name or level not defined'
        }), 400
    h = dumps(Skill().db.find_one({
        'user_id': current_user._id, 'name': payload['name']
        })) if 'name' in payload else None
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that name already exist for the user'
        }), 400
    return Skill().edit_skill(id, payload)