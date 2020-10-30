from app import app
from app.models import Certificate
import flask
from app.routes import token_required

@app.route('/certificate', methods=['POST'])
@token_required
def create_certificate():
    payload = flask.request.get_json()
    if 'title' not in payload or 'company' not in payload or\
             'start_date' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid data'
        }), 400
    data = {
        'title': payload['title'], 'company': payload['company'],
        'start_date': payload['start_date'],
        'user_id': current_user._id
    }
    if 'end_date' in payload:
        data['end_date'] = payload['end_date']
    if 'description' in payload:
        data['desc'] = payload['description']
    data['user_id'] = current_user._id
    c=Certificate().create_certificate(**data)
    return e, 200

@app.route('/Certificate/<id>', methods=['DELETE'])
@token_required
def delete_certificate(id):
    Certificate().delete_certificate(id)
    return '', 204

@app.route('/Certificate/<id>', methods=['PUT'])
@token_required
def edit_certificate(id):
    from bson.json_util import dumps
    if 'course' not in payload or 'school' not in payload:
        return flask.jsonify({
            'error': 'Bad request'
        }), 400
    h = dumps(Certificate().db.find_one({
        'user_id': current_user._id, 'course': payload['course']
        })) if 'course' in payload else None
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that name already exist for the user'
        }), 400
    return Certificate().edit_certificate(id, payload)