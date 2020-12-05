'''Module that handles view of everything that has to do with CRUD of the user'''
from app import app
from ..models import *
import flask
from werkzeug.security import generate_password_hash
from xhtml2pdf import pisa
from io import StringIO
from . import token_required
from .image_saver import save_pic
from .mail_routes import send_mail
from .htmltopdf import render_pdf

@app.route('/user')
@token_required
def get_user(current_user):
    user = User().get_user(current_user['_id'])
    user['skills'] = Skill().get_user_skills(current_user['_id'])
    user['education'] = Education().get_user_educations(current_user['_id'])
    user['languages'] = Language().get_user_languages(current_user['_id'])
    user['experiences'] = WorkExperience().get_user_experiences(current_user['_id'])
    user['achievements'] = Achievement().get_user_achievements(current_user['_id'])
    user['certificates'] = Certificate().get_user_certificates(current_user['_id'])
    return flask.jsonify(user)

@app.route('/user', methods=['PUT'])
@token_required
def update_user(current_user):
    data = dict(flask.request.form)
    avatar_name = save_pic(flask.request.files['avatar']) \
            if flask.request.files['avatar'] else None
    if type(avatar_name) == dict and 'error' in avatar_name or not avatar:
        return {
            'error': 'Bad request',
            'message': avatar_name['message']
        }, 400
    if avatar_name is not None:
        data['image_path'] = flask.request.host_url+'static/'+avatar_name
    User().update_profile(current_user['_id'], **data)
    return flask.redirect(
        flask.url_for('get_user', current_user=current_user)
        ), 201

@app.route('/')
def home():
    return flask.redirect('https://www.postman.com/collections/11d9c8bcd44db2b4040c')

@app.route('/confirm', methods=['POST'])
@token_required
def confirm_account(current_user):
    user = User().update_profile(current_user['_id'], **{'is_confirmed': True})
    return user, 201

@app.route('/templates', methods=['POST'])
@token_required
def template(current_user):
    template = flask.request.get_json()['template']
    if not template:
        return {
            'error': 'Invalid request',
            'message': 'Template not given'
        }, 400
    User().update_profile(current_user['_id'], {'template': template})

@app.route('/plans')
def plans():
    return 'In Progress'


@app.route('/pdf-mail', methods=['POST'])
@token_required
def pdf_mail(current_user):
    name=f"{current_user['name'].replace(' ', '-')}.pdf"
    pdf_template=flask.request.files['pdf']
    pdf = render_pdf(str(pdf_template.read(), encoding='utf-8'), name)
    print(pdf)
    response = flask.send_file(pdf, 
                attachment_filename=name, 
                mimetype='application/pdf'
            )    
    try: 
        msg = flask.render_template('pdf_mail.txt')
        msg_html = flask.render_template('pdf_mail.html')
        mail = send_mail('Here\'s The Resume You Requested For  -- I4G', 
                        current_user.email, 
                        msg, 
                        msg_html, 
                        pdf_attachment=response, 
                        pdf_name=name)
        return {
            'message': 'Email sent successfully'
        }
    except Exception as e: 
        return {'error': e}, 500    

@app.route('/pdf', methods=['POST'])
@token_required
def pdf_(current_user):
    name=f"{current_user['name'].replace(' ', '-')}.pdf"
    pdf_template=flask.request.files['pdf']
    pdf = render_pdf(str(pdf_template.read(), encoding='utf-8'), name)
    print(pdf)
    response = flask.send_file(pdf, 
                attachment_filename=name, 
                mimetype='application/pdf'
            )
    return response