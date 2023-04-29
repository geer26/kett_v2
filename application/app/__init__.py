
import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager

#from app.blueprints.single.single import single_mode


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

#app.register_blueprint(single_mode, url_prefix='/single')

socketio = SocketIO(app)

from app import models
from app.routes import *

print("APP RUNNING")
os.system(f"echo 'APP RUNNING'")