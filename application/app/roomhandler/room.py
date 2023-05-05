from typing import List


class RoomMate:
    def __init__(self, name, SID, supervisor=False):
        self.name = name
        self.SID = SID
        self.supervisor = supervisor

class Room:

    def __init__(self, room_name: str, room_supervisor: RoomMate):
        self.room_name: str = room_name
        self.room_supervisor: RoomMate = room_supervisor
        self.room_mates: List = [self.room_supervisor]

    def mate_connect(self):
        pass