import asyncio
from typing import List
from dataclasses import dataclass
from flask_socketio import SocketIO
from uuid import uuid4


class RoomMate:
    def __init__(self, name, SID, supervisor=False):
        self.name = name
        self.SID = SID
        self.supervisor = supervisor


class Room:

    def __init__(self, room_name: str, room_supervisor: RoomMate, socket: SocketIO):
        self.room_name: str = room_name
        self.room_supervisor: RoomMate = room_supervisor
        self.room_mates: List[RoomMate] = []
        self.socket = socket
        self.namespace = f'{room_name}:{uuid4()}'


    def mate_connect(self, mate: RoomMate, d=None) -> None:
        if not mate.supervisor and self.room_supervisor != None:
            supervisor_sid = self.room_supervisor.SID
            data = {'mate_name': str(mate.name), 'mate_sid': mate.SID}
            if d:
                data['ready_to_go'] = d['ready_to_go']
                #data[] = d[]
                #data[] = d[]
            self.socket_send(namespace="mate_connect", data=data, sid=supervisor_sid)
        if mate.supervisor:
            self.room_supervisor = mate


    def mate_disconnect(self, mate) -> None:
        if mate in self.room_mates:
            self.room_mates.remove(mate)
        if self.room_supervisor != None:
            supervisor_sid = self.room_supervisor.SID
            data = {'mate_name': str(mate.name), 'mate_sid': mate.SID}
            self.socket_send(namespace="mate_disconnect", data=data, sid=supervisor_sid)


    def broadcast(self, namespace, data) -> None:
        for mate in self.room_mates:
            self.socket_send(namespace=namespace, data=data, sid=mate.SID)
        return

    def socket_send(self, namespace, data, sid) -> None:
        self.socket.emit(namespace, data, to=sid)
        return


    def has_supervisor(self) -> bool:
        if self.room_supervisor != None:
            return True
        return False

    def get_mate_by_name(self, name):
        for mate in self.room_mates:
            if mate.name == name:
                return mate
        return None

    def get_mate_by_sid(self, sid):
        for mate in self.room_mates:
            if mate.SID ==sid:
                return mate
        return None

    def has_mate_by_name(self, name) -> bool:
        for mate in self.room_mates:
            if mate.name == name:
                return True
        return False

    def has_mate_by_sid(self, sid) -> bool:
        for mate in self.room_mates:
            if mate.SID == sid:
                return True
        return False


@dataclass
class RoomList:

    rooms: List[Room]

    def get_mate_by_sid(self, sid):
        mate = None
        for room in self.rooms:
            mate = room.get_mate_by_sid(sid)
            if mate:
                break
        return mate

    def get_mate_by_name(self,name):
        mate = None
        for room in self.rooms:
            mate = room.get_mate_by_name(name)
            if mate:
                break
        return mate

    def get_room_by_sid(self, sid):
        for room in self.rooms:
            if room.has_mate_by_sid(sid):
                return room
        return None

    def get_room_by_name(self, name):
        for room in self.rooms:
            if room.has_mate_by_name(name):
                return room
        return None

    def get_room_by_roomname(self, roomname):
        for room in self.rooms:
            if room.room_name == roomname : return room
        return None

    def push_room(self, room: Room) -> bool:
        for r in self.rooms:
            if room.room_name == r.room_name:
                return False
        self.rooms.append(room)
        return True

    def clearup_empty_rooms(self) -> None:
        for room in self.rooms:
            if len(room.room_mates) == 0:
                self.rooms.remove(room)
