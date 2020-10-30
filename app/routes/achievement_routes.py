from app import app
from app.models import Achievement
import flask
from app.routes import token_required

@app.route('/achievement', methods=['POST'])
@token_required
def create_achievement():
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
    a=Achievement().create_achievement(**data)
    return a, 200

@app.route('/achievement/<id>', methods=['DELETE'])
@token_required
def delete_achievement(id):
    Achievement().delete_achievement(id)
    return '', 204


@app.route('/achievement/<id>', methods=['PUT'])
@token_required
def edit_achievement(id):
    from bson.json_util import dumps
    if 'course' not in payload or 'school' not in payload:
        return flask.jsonify({
            'error': 'Bad request'
        }), 400
    h = dumps(Achievement().db.find_one({
        'user_id': current_user._id, 'course': payload['course']
        })) if 'course' in payload else None
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that name already exist for the user'
        }), 400
    return Achievement().edit_achievement(id, payload)