
import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager
from .roomhandler import RoomList
from engineio.payload import Payload

Payload.max_decode_packets = 50

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

socket = SocketIO(app, cors_allowed_origins="*")
#socket = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

roomlist = RoomList([])

from app import models
from app.routes import *
from app.sockets import *


os.system(f"echo 'APP RUNNING'")