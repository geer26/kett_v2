from flask import request
from flask_socketio import send, emit
from app import app, socket, db

from .roomhandler import Room, RoomMate

from app.models import User, Workout



@socket.on('connect')
def connect():
    print(f'User with SID: {request.sid} connected!')
    emit('my response', {'SID': f'{request.sid}'})


@socket.on('disconnect')
def disconnect():
    print(f'User with SID: {request.sid} disconnected!')


@socket.on('createroom')
def create_room(data):
    pass


@socket.on('connect_to_room')
def connect_to_room(data):
    pass
