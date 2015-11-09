from flask import Flask, render_template, request, redirect
from flask.ext import mongoengine
from flask.ext import login
from flask.ext import bcrypt

import os

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {'HOST': os.environ.get('MONGOLAB_URI', 'mongodb://localhost/demo')}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret-key')

db = mongoengine.MongoEngine(app)
app.session_interface = mongoengine.MongoEngineSessionInterface(db)

flask_bcrypt = bcrypt.Bcrypt(app)

login_manager = login.LoginManager()
login_manager.init_app(app)

from auth import auth
app.register_blueprint(auth)

from app import auth, models, forms
