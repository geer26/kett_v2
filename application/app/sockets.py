from flask import request
from flask_socketio import send, emit
from flask_login import login_required
from app import app, socket, db, roomlist

from .roomhandler import Room, RoomMate

from app.models import User, Workout



@socket.on('connect')
def connect():
    SID = request.sid
    socket.emit('my response', {'SID': f'{request.sid}'}, to=SID)


@socket.on('disconnect')
def disconnect():
    room = roomlist.get_room_by_sid(request.sid)
    if not room:
        roomlist.clearup_empty_rooms()
        return
    for mate in room.room_mates:
        if mate.SID == request.sid:
            room.mate_disconnect(mate)
        if mate.SID == request.sid and mate.supervisor == True:
            room.room_supervisor = None
            room.mate_disconnect(mate)
    roomlist.clearup_empty_rooms()
    return


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
        room.mate_connect(mate)
        socket.emit('room_confirmed', {'status': 1,
                                       'message': 'Joined to event as supervisor!',
                                       'namespace': f'{room.namespace}'}, to=SID)
        return

    if data.get('super') == None or data['super'] == False:
        room.room_mates.append(mate)
        room.mate_connect(mate, data)
        socket.emit('room_confirmed', {'status': 1,
                                       'message': 'Joined to event as supervised!',
                                       'namespace': f'{room.namespace}'}, to=SID)
        return


@socket.on('createroom')
#@login_required
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


@socket.on('fetch_roomstatus')
#@login_required
def fetch_roomstatus(data):
    room = roomlist.get_room_by_sid(request.sid)
    if not room:
        print('NO ROOM!')
        return

    room.broadcast(namespace='fetch_roomstatus', data={})
    return


@socket.on('provide_roomstatus')
def provide_roomstatus(data):
    data['mate_sid'] = request.sid
    room = roomlist.get_room_by_sid(request.sid)
    if not room:
        print('NO ROOM!')
        return
    mate = room.get_mate_by_sid(request.sid)
    if not mate:
        print('NO ROOM!')
        return
    socket.emit('provide_roomstatus', (data), to=room.room_supervisor.SID)



@socket.on('nameenter')
#@login_required
def name_entered(data):
    name = data['data']['name']
    sid = data['data']['sid']
    socket.emit('nameenter', {'name': f'{name}'}, to=sid)


@socket.on('suspend_mate')
#@login_required
def suspend_mate(data):
    sid = data['sid']
    socket.emit('toggle_suspend', {}, to=sid)


@socket.on('send_workout')
#login_required
def send_workout(data):
    room = roomlist.get_room_by_sid(request.sid)
    if not room:
        print('NO ROOM')
        return
    room.broadcast(namespace='send_workout', data=data)


@socket.on('ready_to_go')
def ready_to_go(data):
    sid = request.sid
    data['sid'] = sid
    room = roomlist.get_room_by_sid(sid)
    if not room:
        print('NO ROOM!')
        return
    if room.room_supervisor:
        super_sid = room.room_supervisor.SID
        socket.emit('platform_ready', data, to=super_sid)
    else:
        print('NO ROOM SUPERVISOR')


