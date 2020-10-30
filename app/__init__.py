'''API Application'''
import flask, os
from pymongo import MongoClient
from werkzeug.http import HTTP_STATUS_CODES
from flask_cors import CORS

MONGODB_URI = os.environ.get('MONGODB_URI')

app = flask.Flask(__name__)
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
mongo = MongoClient(MONGODB_URI)
db = mongo.resume

CORS(app)

from app.routes import (
        achievement_routes, auth_routes, certificate_routes,
        education_routes, experience_routes, hobby_routes,
        htmltopdf, language_routes, mail_routes, skill_routes, user_routes
)