from app import app, mongo
from app.models import (User, Skill, Language, 
                Hobby, WorkExperience, Education)
import flask, jwt
from werkzeug.security import (generate_password_hash, 
                    check_password_hash)

@app.route('/users/<id>')
@token_required
def user(id):
    return User().get_user(id)






