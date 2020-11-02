'''Module that handles view of everything that has to do with certificate of the  user'''
from app import app
from app.models import Certificate
import flask
from app.routes import token_required

@app.route('/certificate')
@token_required
def get_certificates(current_user):
    return flask.jsonify(
        Certificate().get_user_certificates(current_user['_id'])
    )

@app.route('/certificate/<id>')
@token_required
def get_certificate(current_user, id):
    return flask.jsonify(
        Certificate().get_certificate(id)
    )

@app.route('/certificate', methods=['POST'])
@token_required
def create_certificate(current_user):
    payload = flask.request.get_json()
    payload['user_id'] = current_user['_id']
    c=Certificate().create_certificate(**payload)
    return c, 201

@app.route('/Certificate/<id>', methods=['DELETE'])
@token_required
def delete_certificate(current_user, id):
    Certificate().delete_certificate(id)
    return '', 204

@app.route('/Certificate/<id>', methods=['PUT'])
@token_required
def edit_certificate(current_user, id):
    payload = flask.request.get_json()
    if 'course' not in payload or 'school' not in payload:
        return flask.jsonify({
            'error': 'Bad request'
        }), 400
    h = Certificate().db.find_one({
        'user_id': current_user['_id'], 'course': payload['course']
        }) if 'course' in payload else None
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that name already exist for the user'
        }), 400
    c=Certificate().edit_certificate(id, payload)
    return c, 201