from flask import request
from flask_socketio import send, emit
from app import app, socket, db, roomlist

from .roomhandler import Room, RoomMate

from app.models import User, Workout



@socket.on('connect')
def connect():
    emit('my response', {'SID': f'{request.sid}'})


@socket.on('disconnect')
def disconnect():
    for room in roomlist.rooms:
        for mate in room.room_mates:
            if mate.SID == request.sid:
                room.room_mates.remove(mate)
            if mate.supervisor:
                room.room_supervisor = None
    roomlist.clearup_empty_rooms()


@socket.on('createroom')
def create_room(data):
    #create: {'room_name': 'join', 'super': True, 'new_room': False}
    if data.get('new_room') and data['new_room']:
        mate = RoomMate(name="SUPERVISOR", SID=request.sid, supervisor=data['super'])
        room = Room(room_name=data['room_name'], room_supervisor=mate, socket=socket)
        room.room_mates.append(mate)
        if roomlist.push_room(room):
            socket.emit('room_confirmed', {'status': 1, 'message': 'Room created!'})
            return
        else:
            socket.emit('room_confirmed', {'status': 0, 'message': 'Room already exists!'})
            return

    elif not data['new_room']:
        mate = RoomMate(name="SUPERVISOR", SID=request.sid, supervisor=data['super'])
        room = roomlist.get_room_by_name(data['room_name'])
        if room == None:
            socket.emit('room_confirmed', {'status': 0, 'message': 'Room doesn\'t exists!'})
            return
        if room.has_supervisor():
            socket.emit('room_confirmed', {'status': 0, 'message': 'Accept as supervisor is forbidden!'})
            return
        else:
            room.room_supervisor = mate
            room.room_mates.append(mate)
            socket.emit('room_confirmed', {'status': 1, 'message': 'Joined to room!'})
    else:
        raise Exception("Invalid operation, new room argument required!")

