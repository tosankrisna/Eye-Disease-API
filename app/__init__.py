import os
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = '#'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '#'

project_dir = os.path.dirname(os.path.abspath(__file__))

from app.modules.controllers import *