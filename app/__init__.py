from flask import Flask, render_template, request, redirect
import flask_mongoengine
import flask_login
import flask_bcrypt

import os

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {'host': os.environ.get('MONGOLAB_URI', 'mongodb://localhost/demo')}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret-key')

db = flask_mongoengine.MongoEngine(app)
app.session_interface = flask_mongoengine.MongoEngineSessionInterface(db)

flask_bcrypt = flask_bcrypt.Bcrypt(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from auth import auth
app.register_blueprint(auth)

from app import auth, models, forms
