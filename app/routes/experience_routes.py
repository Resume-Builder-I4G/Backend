from app import app
from app.models import WorkExperience
import flask
from app.routes import token_required

@app.route('/experience', methods=['POST'])
@token_required
def create_experience():
    payload = flask.request.get_json()
    if 'course' not in payload or 'school' not in payload or\
             'start_date' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid data'
        }), 400
    data = {
        'course': payload['course'], 'school': payload['school'],
        'start_date': payload['start_date'],
        'user_id': current_user._id
    }
    if 'end_date' in payload:
        data['end_date'] = payload['end_date']
    if 'description' in payload:
        data['desc'] = payload['description']
    data['user_id'] = current_user._id
    w=WorkExperience().create_work(**data)
    return w, 200

@app.route('/experience/<id>', methods=['DELETE'])
@token_required
def delete_experience(id):
    WorkExperience().delete_work(id)
    return '', 204

@app.route('/experience/<id>', methods=['PUT'])
@token_required
def edit_experience(id):
    from bson.json_util import dumps
    if 'title' not in payload or 'company' not in payload:
        return flask.jsonify({
            'error': 'Bad request'
        }), 400
    h = dumps(WorkExperience().db.find_one({
        'user_id': current_user._id, 'title': payload['title']
        })) if 'title' in payload an else None
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that name already exist for the user'
        }), 400
    return WorkExperience().edit_work(id, payload)