'''Module that handles view of everything that has to do with hobbies of the  user'''
from app import app
import flask
from app.routes import token_required
from app.models import Hobby


@app.route('/hobbies')
@token_required
def get_hobbies(current_user):
    return flask.jsonify(
        Hobby().get_user_hobbies(current_user['_id'])
    )

@app.route('/hobbies/<id>')
@token_required
def get_hobby(current_user, id):
    return flask.jsonify(
        Hobby().get_hobby(id)
    )

@app.route('/hobbies', methods=['POST'])
@token_required
def create_hobby(current_user):
    payload = flask.request.get_json()
    if 'name' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid email or password'
        }), 400
    payload = {
        'name': payload['name'],
        'user_id': current_user['_id']
    }
    h=Hobby().create_hobby(**payload)
    return h, 201

@app.route('/hobbies/<id>', methods=['DELETE'])
@token_required
def delete_hobby(current_user, id):
    Hobby().delete_hobby(id)
    return '', 204

@app.route('/hobbies/<id>', methods=['PUT'])
@token_required
def edit_hobby(current_user, id):
    payload = flask.request.get_json()
    if 'name' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'name not defined'
        }), 400
    h = Hobby().db.find_one({
        'user_id': current_user['_id'], 'name': payload['name']
        })
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that hobby already exist for the user'
        }), 400
    h=Hobby().edit_hobby(id, payload)
    return h, 201
