import json, uuid
from app import db, login
import bcrypt
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)

    # -------- Connections
    # -------- FK
    # -------- BACKREF
    # events = db.relationship('Event', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    # workouts = db.relationship('Workout', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    # exercises = db.relationship('Exercise', backref='owner', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'Username: {self.username}, ID: {self.id}'

    def set_password(self, password):
        salt = bcrypt.gensalt(14)
        p_bytes = password.encode()
        pw_hash = bcrypt.hashpw(p_bytes, salt)
        self.password_hash = pw_hash.decode()
        self.salt = salt.decode()
        return True

    def check_password(self, password):
        c_password = bcrypt.hashpw(password.encode(), self.salt.encode()).decode()
        if c_password == self.password_hash:
            return True
        else:
            return False

    def get_self_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'is_superuser': self.is_superuser
        }


class Event(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    description = db.Column(db.String(256), default='No description')
    short_name = db.Column(db.String(32), default='No name')
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    workouts = db.Column(db.String(), default='')
    sequence = db.Column(db.String(), default='')
    ident = db.Column(db.String(6), nullable=False)
    closed = db.Column(db.Boolean, default=False)
    named = db.Column(db.Integer, default=0)

    # -------- Connections
    # -------- FK
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    # -------- BACKREF
    # competitors = db.relationship('Competitor', backref='event', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self):
        self.ident = self.gen_ident()

    def __repr__(self):
        return f'id: {self.id}, ident: {self.ident}, user: {self.user}'

    def gen_ident(self):
        uid = str(uuid.uuid1()).split('-')[3]
        ts = str(datetime.now().timestamp()).encode()
        ts_hash = bcrypt.hashpw(ts, bcrypt.gensalt()).decode()[51:53]
        self.ident = uid + ts_hash
        return str(uid + ts_hash)

    def get_ident(self):
        return str(self.ident)

    def get_self_json(self):
        return {
            'id': self.id,
            'name': self.short_name,
            'description': self.description,
            'workouts': self.workouts,
            'sequence': self.sequence,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'closed': self.closed,
            'ident': self.ident,
            'named': self.named
        }


class Workout(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    short_name = db.Column(db.String(32), unique=True, nullable=False, default='No name')
    description = db.Column(db.String(256), default=None)
    exercises = db.Column(db.String(), default='')
    '''

    eg.
    [4,56,23,76,2,42, ... ] -> ID of Exercise

    eg.
    [{'time': 600(time in secs), 'type': 'warmup'(warmup/time/rest), 'max': 120(maximum reps) , 'add': 'KÉSZÜLJ!(plain text)'},{...}]
    eg. pentathlon:
    [
    { 'time': 5, 'type': 'warmup', 'max': 0, 'add': 'Felkészülés'},
    { 'time': 360, 'type': 'time', 'max': 120, 'add': 'Clean'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'time', 'max': 60, 'add': 'Clean&Press'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'rest', 'max': 120, 'add': 'Jerk'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'rest', 'max': 108, 'add': 'Half Snatch'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'rest', 'max': 120, 'add': 'Push Press'}
    ]
    '''
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)

    # -------- Connections
    # -------- FK
    #user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'id: {self.id}, name: {self.short_name}, exercises: {self.exercises}'

    def get_self_json(self):
        return {
            'id': self.id,
            'name': self.short_name,
            'description': self.description,
            'exercises': json.loads(self.exercises),
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        }
