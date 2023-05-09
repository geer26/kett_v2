from flask import request
from flask_socketio import send, emit
from app import app, socket, db, roomlist

from .roomhandler import Room, RoomMate

from app.models import User, Workout



@socket.on('connect')
def connect():
    SID = request.sid
    socket.emit('my response', {'SID': f'{request.sid}'}, to=SID)


@socket.on('disconnect')
def disconnect():
    for room in roomlist.rooms:
        for mate in room.room_mates:
            if mate.SID == request.sid:
                room.room_mates.remove(mate)
            if mate.supervisor:
                room.room_supervisor = None
    roomlist.clearup_empty_rooms()


@socket.on('joinroom')
def join_room(data):
    SID = request.sid
    mate = RoomMate(name=str(data['station_name']), SID=request.sid, supervisor=data['super'])
    room = roomlist.get_room_by_roomname(data['room_name'])
    if not data.get("room_name") or room == None:
        socket.emit('room_confirmed', {'status': 0, 'message': 'Event doesn\'t exists!'}, to=SID)
        return
    if room.has_supervisor() and data['super'] == True:
        socket.emit('room_confirmed', {'status': 0, 'message': 'Connect as supervisor is forbidden!'}, to=SID)
        return
    for m in room.room_mates:
        if mate.name == m.name:
            socket.emit('room_confirmed', {'status': 0, 'message': 'This station already joined!'}, to=SID)
            return
    if not room.has_supervisor() and data['super'] == True:
        room.room_supervisor = mate
        room.room_mates.append(mate)
        socket.emit('room_confirmed', {'status': 1,
                                       'message': 'Joined to event as supervisor!',
                                       'namespace': f'{room.namespace}'}, to=SID)
        return
    if data.get('super') == None or data['super'] != True:
        room.room_mates.append(mate)
        socket.emit('room_confirmed', {'status': 1,
                                       'message': 'Joined to event as supervised!',
                                       'namespace': f'{room.namespace}'}, to=SID)
        if room.room_supervisor:
            supervisor_sid = room.room_supervisor.SID
            room_mate_data = {'name' : f'{mate.name}'}
        return


@socket.on('createroom')
def create_room(data):
    SID = request.sid
    if data.get('new_room') and data['new_room']:
        mate = RoomMate(name=data['station_name'], SID=request.sid, supervisor=data['super'])
        room = Room(room_name=data['room_name'], room_supervisor=mate, socket=socket)
        room.room_mates.append(mate)
        if roomlist.push_room(room):
            socket.emit('room_confirmed', {'status': 1, 'message': 'Event created!', 'namespace': f'{room.namespace}'}, to=SID)
            return
        else:
            socket.emit('room_confirmed', {'status': 0, 'message': 'Event already exists!'}, to=SID)
            return
    else:
        raise Exception("Invalid operation, new room argument required!")

