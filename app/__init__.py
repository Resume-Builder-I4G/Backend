'''API Application'''
import flask, os
from flask_mail import Mail
from pymongo import MongoClient
from werkzeug.http import HTTP_STATUS_CODES
from flask_cors import CORS

MONGODB_URI = os.environ.get('MONGODB_URI')

app = flask.Flask(__name__)
mail = Mail(app)
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SERVER']=os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT']=os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS']=1
mongo =MongoClient(MONGODB_URI)
db = mongo.resume

CORS(app)

from app.routes import (
        achievement_routes, auth_routes, certificate_routes,
        education_routes, experience_routes, hobby_routes,
        htmltopdf, language_routes, mail_routes, skill_routes, user_routes
)