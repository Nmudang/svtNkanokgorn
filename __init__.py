from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'svt.sqlite')
app.config['SECRET_KEY'] = 'f79259f32ac3ff68beeaefe4'
app.config['IMAGE_UPLOADS'] = os.path.join(basedir, 'static/images/')
if not os.path.isdir(app.config['IMAGE_UPLOADS']):
	os.mkdir(app.config['IMAGE_UPLOADS'])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from svt import routes