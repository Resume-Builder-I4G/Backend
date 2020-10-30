from flask import jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.http import HTTP_STATUS_CODES
from app import app, mongo



@app.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

def revoke_token():
    token_auth.current_user().revoke_auth()
    db.session.commit()
    return '', 204