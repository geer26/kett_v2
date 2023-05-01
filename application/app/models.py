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
            'is_superuser': self.is_superuser
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
