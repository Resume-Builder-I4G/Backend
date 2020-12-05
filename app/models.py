'''Module that defines all the db attributes and helper methods'''
import os, datetime, uuid
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, app

class User:
    def __init__(self):
        self.db = db.users
    
    def signup(self, name, email, password_hash):
        user = {
            '_id': uuid.uuid4().hex,
            'name': name,
            'email': email, 
            'is_confirmed': False,
            'password_hash': password_hash
        }
        user =  self.db.insert_one(user)
        # create the user model.
        return self.db.find_one({'email': email})
    
    def signin(self, email, password):
        # get user with email if any
        # check if password is same
        user = self.db.find_one({'email': email})
        if user and check_password_hash(user['password_hash'], password):
            return user
        else:
            return {'error': 'Invalid email or password'}
    
    def get_users(self):
        return [user for user in self.db.find()]
    
    def get_user(self, id):
        return self.db.find_one({'_id':id})
    
    def update_profile(self, id, **kwargs):
        # find user with email, and update the account
        # city, phone, about, current_template, avatar, state, country
        user = self.db.find_one_and_update({'_id': id}, {'$set':kwargs})
        return user

    def get_reset_token(self, current_user, expires_sec=1800):
        '''Generates a timed token to reset password'''
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': current_user['_id']}).decode('utf-8')

    @staticmethod 
    def verify_reset_token(token):
        '''Verifies the timed token generated in the function above'''
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User().db.find_one({'_id': user_id})

    
class Skill:
    def __init__(self):
        self.db = db.skills

    def create_skill(self, name, level, user_id):
        skill = {
            '_id': uuid.uuid4().hex,
            'name': name, 'level': level
        }
        skill = self.db.insert_one({
            **skill, 'user_id': user_id
        })
        return self.db.find_one({'name': name, 'user_id': user_id})
    
    def get_skill(self, id):
        return self.db.find_one({'_id':id})

    def get_user_skills(self, user_id):
        return [skill for skill in self.db.find({'user_id': user_id})]
    
    def edit_skill(self, _id, payload):
        # get skill with the _id and update
        skill = self.db.find_one_and_update({'_id': _id}, {'$set': payload})
        return self.db.find_one(payload)
    
    def delete_skill(self, _id):
        # get skill with the _id and delete
        skill = self.db.delete_one({'_id': _id})
        return skill


class Hobby:
    def __init__(self):
        self.db = db.hobbies

    def create_hobby(self, name, user_id):
        hobby = {
            '_id': uuid.uuid4().hex,
            'name': name
        }
        hobby = self.db.insert_one({
            **hobby, 'user_id': user_id
        })
        return self.d.find_one({'name': name, 'user_id': user_id})
    
    def get_hobby(self, id):
        return self.db.find_one({'_id':id})

    def get_user_hobbies(self, user_id):
        return [hobby for hobby in self.db.find({'user_id': user_id})]

    def edit_hobby(self, _id, payload):
        # get hobby with the _id and update
        hobby = self.db.find_one_and_update({'_id': _id}, {'$set': payload})
        return self.db.find_one(payload)
    
    def delete_hobby(self, _id):
        # get hobby with the _id and delete
        hobby = self.db.delete_one({'_id': _id})
        return hobby

class Language:
    def __init__(self):
        self.db = db.languages

    def create_language(self, name, proficiency, user_id):
        language = {
            '_id': uuid.uuid4().hex, 'name': name, 
            'proficiency': proficiency
        }
        # create the hobby model and add the hobby model to the auth user
        language = self.db.insert_one({
            **language, 'user_id': user_id
        })
        return self.db.find_one({'name': name, 'user_id': user_id})
    
    def get_language(self, id):
        return self.db.find_one({'_id':id})

    def get_user_languages(self, user_id):
        return [language for language in self.db.find({'user_id': user_id})]
    
    def edit_language(self, _id, payload):
        # get language with the _id and update
        language = self.db.find_one_and_update({'_id': _id}, {'$set':payload})
        return self.db.find_one(payload)
    
    def delete_language(self, _id):
        # get language with the _id and delete
        language = self.db.delete_one({'_id': _id})
        return language

class Certificate:
    def __init__(self):
        self.db = db.certificates

    def create_certificate(self, payload, user_id):
        certificate = {
            '_id': uuid.uuid4().hex, **payload
        }
        # create the hobby model.
        # add the hobby model to the auth user
        certificate = self.db.insert_one({
            **certificate, 'user_id': user_id
        })
        return self.db.find_one({**payload, 'user_id': user_id})
    
    def get_certificate(self, id):
        return self.db.find_one({'_id':id})

    def get_user_certificates(self, user_id):
        return list(self.db.find({'user_id': user_id}))
    
    def edit_certificate(self, _id, payload):
        # get language with the _id and update
        certificate = self.db.find_one_and_update({'_id': _id}, {'$set':payload})
        return (self.db.find_one(payload))
    
    def delete_certificate(self, _id):
        # get language with the _id and delete
        certificate = self.db.delete_one({'_id': _id})
        return certificate

class Achievement:
    def __init__(self):
        self.db = db.achievements

    def create_achievement(self, payload, user_id):
        achievement = {
            '_id': uuid.uuid4().hex, **payload
        }
        # create the hobby model.
        # add the hobby model to the auth user
        achievement = self.db.insert_one({
            **achievement, 'user_id': user_id
        })
        return self.db.find_one({**payload, 'user_id': user_id})
    
    def get_achievement(self, id):
        return self.db.find_one({'_id':id})

    def get_user_achievements(self, user_id):
        return list(self.db.find({'user_id': user_id}))
    
    def edit_achievement(self, _id, payload):
        # get language with the _id and update
        achievement = self.db.find_one_and_update({'_id': _id}, {'$set': payload})
        return self.db.find_one(payload)
    
    def delete_language(self, _id):
        # get language with the _id and delete
        achievement = self.db.delete_one({'_id': _id})
        return achievement

class WorkExperience:
    def __init__(self):
        self.db = db.work_experience

    def create_work(self, title, company, start_date, end_date=None, desc=None):
        end_date = 'Present' if not end_date else end_date
        work = {
            '_id': uuid.uuid4().hex,
            'title': title, 'company': company, 
            'start_date': start_date, 'end_date': end_date
        }
        if desc:
            work['description'] = desc
        work = self.db.insert_one({
            **work, 'user_id': user_id
        })
        return self.db.find_one({'user_id': user_id, 'title': title, 'company': company})
    
    def get_work(self, id):
        return self.db.find_one({'_id':id})

    def get_user_experiences(self, user_id):
        return list(self.db.find({'user_id': user_id}))
    
    def edit_work(self, _id, payload):
        # get work with the _id and update
        work = self.db.find_one_and_update({'_id': _id}, {'$set': payload})
        return self.db.find_one({**payload, 'user_id': user_id})
    
    def delete_work(self, _id):
        # get work with the _id and delete
        work = self.db.delete_one({'_id': _id})
        return work

class Education:
    def __init__(self):
        self.db = db.education

    def create_education(self, course, school, start_date, user_id, end_date=None, desc=None):
        end_date = 'Present' if not end_date else end_date
        education = {
            '_id': uuid.uuid4().hex,
            'course': course, 'school': school, 
            'start_date': start_date, 'end_date': end_date
        }
        if desc:
            education['description'] = desc
        # create the education and add it to the auth user.
        education = self.db.insert_one({
            **education, 'user_id': user_id
        })
        return self.db.find_one({'school': school, 'course': course, 'user_id': user_id})

    def get_education(self, id):
        return self.db.find_one({'_id':id})

    def get_user_educations(self, user_id):
        return list(self.db.find({'user_id': user_id}))
    
    def edit_education(self, _id, payload):
        # get education with the _id and update
        education = self.db.find_one_and_update({'_id': _id}, {'$set': payload})
        return self.db.find_one({**payload, 'user_id': user_id})
    
    def delete_education(self, _id):
        # get education with the _id and delete
        education = self.db.delete_one({'_id': _id})
        return education