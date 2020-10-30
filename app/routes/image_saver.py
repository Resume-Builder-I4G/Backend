'''Helper module that saves the avatar of the  user to disc and returns the filename'''
from PIL import Image
import os, secrets
from app import app

def save_pic(picture):
    file_name = secrets.token_hex(8) +os.path.splitext(picture.filename)[1]
    file_path = os.path.join(app.root_path, 'static', file_name)
    picture = Image.open(picture)
    picture.thumbnail((150, 150))
    picture.save(file_path)
    return file_name