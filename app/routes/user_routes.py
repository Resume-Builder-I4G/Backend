from app import app
from app.models import *
import flask
from app.routes import token_required
from app.routes.image_saver import save_pic

@app.route('/user')
@token_required
def get_user():
    user = User().get_user(current_user._id)
    user['skills'] = Skill().get_user_skills(current_user._id)
    user['education'] = Education().get_user_educations(current_user._id)
    user['languages'] = Languages().get_user_skills(current_user._id)
    user['experiences'] = WorkExperience().get_user_experiences(current_user._id)
    user['achievements'] = Achievement().get_user_achievements(current_user._id)
    user['certificates'] = Certificate().get_user_certificates(current_user._id)
    return flask.jsonify(user), 200

@app.route('/user', methods=['PUT'])
@token_required
def update_user():
    data = flask.request.get_json()

    print(flask.request.files['avatar'])
    return {
        'msg': 'Done', 
        'file': save_pic(flask.request.files['avatar'])
        }