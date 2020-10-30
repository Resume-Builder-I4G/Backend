from app import app
import flask
from app.routes import token_required
from app.models import Hobby

@app.route('/hobbies', methods=['POST'])
@token_required
def create_hobby():
    payload = flask.request.get_json()
    if 'name' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid email or password'
        }), 400
    payload = {
        'name': payload['name'],
        'user_id': current_user._id
    }
    h=Hobby().create_hobby(**payload)
    return h, 200

@app.route('/hobbies/<id>', methods=['DELETE'])
@token_required
def delete_hobby(id):
    Hobby().delete_hobby(id)
    return '', 204

@app.route('/hobbies/<id>', methods=['PUT'])
@token_required
def edit_hobby(id):
    from bson.json_util import dumps
    if 'name' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'name not defined'
        }), 400
    h = dumps(Hobby().db.find_one({
        'user_id': current_user._id, 'name': payload['name']
        }))
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that name already exist for the user'
        }), 400
    return Hobby().edit_hobby(id, payload)
