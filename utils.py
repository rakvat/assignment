from constants import OTHER_HOUSE, SAME_FLOOR, SAME_HOUSE
from data import ROOM_CLOSENESS, ROOMS, N
from enums import House, RoomKey, RoomUseKey


# room gets assigned to a use
def room_to_use(use: RoomUseKey) -> list[int]:
    return [1 if i == use.value else 0 for i in range(N)]


# use is given a room
def use_to_room(room: RoomKey) -> list[int]:
    return [1 if i == room.value else 0 for i in range(N)]


def distance(room1_key: RoomKey, room2_key: RoomKey) -> int:
    if room1_key == room2_key:
        return -1
    if (room1_key, room2_key) in ROOM_CLOSENESS:
        return ROOM_CLOSENESS[(room1_key, room2_key)]
    if (room2_key, room1_key) in ROOM_CLOSENESS:
        return ROOM_CLOSENESS[(room2_key, room1_key)]

    room1 = ROOMS[room1_key]
    room2 = ROOMS[room2_key]
    if room1.house is room2.house and room1.floor == room2.floor:
        return SAME_FLOOR
    if room1.house is room2.house or (
        room1.house in (House.KH, House.MH) and room2.house in (House.KH, House.MH)
    ):
        return SAME_HOUSE
    return OTHER_HOUSE
