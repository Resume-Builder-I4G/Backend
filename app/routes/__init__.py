import flask, jwt

from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in flask.request.headers:
            token = flask.request.headers['Authorization'].split(' ')[1]
        if not token: 
            return flask.jsonify({
                'error': 'Unauthorized',
                'message': 'You are not signed in'
                }), 403
        try:
            data=jwt.decode(token, app.config['SECRET_KEY'])
            current_user=User().get_user(data['_id'])
        except Exception as e:
            return flask.jsonify({
                'error': 'Unauthorized',
                'message': str(e)
                }), 403

        return f(current_user, *args, **kwargs)

    return decorated


from app.routes import *