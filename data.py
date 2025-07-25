from constants import NEIGHBOR, PASSTHROUGH
from entities import Function, Person, Room
from enums import House, RoomKey, RoomUseKey

ROOM_USES: dict[RoomUseKey, Person | Function] = {
    RoomUseKey.G: Function(key=RoomUseKey.G),
    RoomUseKey.B: Function(key=RoomUseKey.B),
    RoomUseKey.P: Function(key=RoomUseKey.P),
    RoomUseKey.LW: Person(
        key=RoomUseKey.LW,
        current_room_key=RoomKey.MH0,
        current_activity=0.0,
        past_activity=0.0,
        was_lucky_with_room_before=0.9,
        child=True,
        reluctance_to_move=0.9,
    ),
    RoomUseKey.SH: Person(
        key=RoomUseKey.SH,
        current_room_key=RoomKey.MH1,
        current_activity=0.1,
        past_activity=0.5,
        was_lucky_with_room_before=0.9,
        reluctance_to_move=1.0,
    ),
    RoomUseKey.SW: Person(
        key=RoomUseKey.SW,
        current_room_key=RoomKey.MH2,
        current_activity=0.9,
        past_activity=0.9,
        was_lucky_with_room_before=0.5,
        reluctance_to_move=0.5,
    ),
    RoomUseKey.LR: Person(
        key=RoomUseKey.LR,
        current_room_key=RoomKey.MH3,
        current_activity=0.1,
        past_activity=0.2,
        was_lucky_with_room_before=1.0,
        reluctance_to_move=0.2,
    ),
    RoomUseKey.CH: Person(
        key=RoomUseKey.CH,
        current_room_key=RoomKey.MH4,
        current_activity=0.2,
        past_activity=0.4,
        was_lucky_with_room_before=0.3,
        reluctance_to_move=0.6,
    ),
    RoomUseKey.FW: Person(
        key=RoomUseKey.FW,
        current_room_key=RoomKey.MH5,
        current_activity=0.0,
        past_activity=0.0,
        was_lucky_with_room_before=0.7,
        child=True,
        reluctance_to_move=0.6,
    ),
    RoomUseKey.MB: Person(
        key=RoomUseKey.MB,
        current_room_key=RoomKey.MH6,
        current_activity=0.7,
        past_activity=0.5,
        was_lucky_with_room_before=1.0,
        reluctance_to_move=0.9,
        min_room_size_wish=16,
    ),
    RoomUseKey.WF: Person(
        key=RoomUseKey.WF,
        current_room_key=RoomKey.MH7,
        current_activity=0.0,
        past_activity=0.0,
        was_lucky_with_room_before=0.0,
        child=True,
        reluctance_to_move=0.9,
    ),
    RoomUseKey.CL: Person(
        key=RoomUseKey.CL,
        current_room_key=RoomKey.MH8,
        current_activity=0.5,
        past_activity=0.4,
        was_lucky_with_room_before=0.3,
        child=True,
        reluctance_to_move=0.2,
    ),
    RoomUseKey.KE: Person(
        key=RoomUseKey.KE,
        current_room_key=RoomKey.MH10,
        current_activity=0.7,
        past_activity=0.9,
        was_lucky_with_room_before=0.3,
        reluctance_to_move=0.6,
    ),
    RoomUseKey.JL: Person(
        key=RoomUseKey.JL,
        current_room_key=RoomKey.GH0,
        current_activity=0.9,
        past_activity=0.9,
        was_lucky_with_room_before=0.6,
        reluctance_to_move=0.4,
        min_room_size_wish=15,
    ),
    RoomUseKey.MH: Person(
        key=RoomUseKey.MH,
        current_room_key=RoomKey.GH1,
        current_activity=0.2,
        past_activity=0.8,
        was_lucky_with_room_before=0.5,
        reluctance_to_move=0.6,
        min_room_size_wish=18,
    ),
    RoomUseKey.AZ: Person(
        key=RoomUseKey.AZ,
        current_room_key=RoomKey.GH2,
        current_activity=0.2,
        past_activity=0.2,
        was_lucky_with_room_before=0.3,
        reluctance_to_move=0.4,
    ),
    RoomUseKey.CJ: Person(
        key=RoomUseKey.CJ,
        current_room_key=RoomKey.GH3,
        current_activity=0.1,
        past_activity=0.2,
        was_lucky_with_room_before=0.9,
        reluctance_to_move=0.2,
        min_room_size_wish=20,
    ),
    RoomUseKey.VH: Person(
        key=RoomUseKey.VH,
        current_room_key=RoomKey.GH4,
        current_activity=0.1,
        past_activity=0.2,
        was_lucky_with_room_before=1.0,
        reluctance_to_move=0.7,
        min_room_size_wish=16,
    ),
    RoomUseKey.JH: Person(
        key=RoomUseKey.JH,
        current_room_key=RoomKey.GH5,
        current_activity=0.0,
        past_activity=0.0,
        was_lucky_with_room_before=0.1,
        child=True,
        reluctance_to_move=0.7,
    ),
}

FUNCTIONAL_USES = {
    use_key for use_key in RoomUseKey if isinstance(ROOM_USES[use_key], Function)
}

ROOMS: dict[RoomKey, Room] = {
    RoomKey.KH0: Room(
        key=RoomKey.KH0,
        house=House.KH,
        floor=1,
        size=15,
    ),
    RoomKey.KH1: Room(
        key=RoomKey.KH1,
        house=House.KH,
        floor=1,
        size=25,
    ),
    RoomKey.MH0: Room(
        key=RoomKey.MH0,
        house=House.MH,
        floor=3,
        size=12,
    ),
    RoomKey.MH1: Room(
        key=RoomKey.MH1,
        house=House.MH,
        floor=3,
        size=16.6,
    ),
    RoomKey.MH2: Room(
        key=RoomKey.MH2,
        house=House.MH,
        floor=3,
        size=13,
    ),
    RoomKey.MH3: Room(
        key=RoomKey.MH3,
        house=House.MH,
        floor=2,
        size=20.5,
        window_to_street=True,
    ),
    RoomKey.MH4: Room(
        key=RoomKey.MH4,
        house=House.MH,
        floor=2,
        size=10,
        window_to_street=True,
    ),
    RoomKey.MH5: Room(
        key=RoomKey.MH5,
        house=House.MH,
        floor=2,
        size=15.5,
    ),
    RoomKey.MH6: Room(
        key=RoomKey.MH6,
        house=House.MH,
        floor=1,
        size=20.5,
        window_to_street=True,
    ),
    RoomKey.MH7: Room(
        key=RoomKey.MH7,
        house=House.MH,
        floor=1,
        size=10,
        window_to_street=True,
    ),
    RoomKey.MH8: Room(
        key=RoomKey.MH8,
        house=House.MH,
        floor=1,
        size=10,
    ),
    RoomKey.MH9: Room(
        key=RoomKey.MH9,
        house=House.MH,
        floor=0,
        size=20,
    ),
    RoomKey.MH10: Room(
        key=RoomKey.MH10,
        house=House.MH,
        floor=0,
        size=8,
    ),
    RoomKey.GH0: Room(
        key=RoomKey.GH0,
        house=House.GH,
        floor=1,
        size=15.5,
    ),
    RoomKey.GH1: Room(
        key=RoomKey.GH1,
        house=House.GH,
        floor=1,
        size=15,
    ),
    RoomKey.GH2: Room(
        key=RoomKey.GH2,
        house=House.GH,
        floor=1,
        size=12,
    ),
    RoomKey.GH3: Room(
        key=RoomKey.GH3,
        house=House.GH,
        floor=1,
        size=20.5,
    ),
    RoomKey.GH4: Room(
        key=RoomKey.GH4,
        house=House.GH,
        floor=0,
        size=23.5,
    ),
    RoomKey.GH5: Room(
        key=RoomKey.GH5,
        house=House.GH,
        floor=0,
        size=9.5,
    ),
}
MIN_ROOM_SIZE = min(room.size for _, room in ROOMS.items())

ROOM_CLOSENESS: dict[tuple[RoomKey, RoomKey], int] = {
    (RoomKey.MH6, RoomKey.MH7): PASSTHROUGH,
    (RoomKey.MH9, RoomKey.MH10): PASSTHROUGH,
    (RoomKey.KH1, RoomKey.KH0): PASSTHROUGH,
    (RoomKey.MH0, RoomKey.MH1): NEIGHBOR,
    (RoomKey.MH1, RoomKey.MH2): NEIGHBOR,
    (RoomKey.MH3, RoomKey.MH4): NEIGHBOR,
    (RoomKey.MH7, RoomKey.MH8): NEIGHBOR,
    (RoomKey.GH0, RoomKey.GH1): NEIGHBOR,
    (RoomKey.GH1, RoomKey.GH2): NEIGHBOR,
    (RoomKey.GH2, RoomKey.GH3): NEIGHBOR,
    (RoomKey.GH4, RoomKey.GH5): NEIGHBOR,
}

PASSTHROUGH_ROOM_KEYS: set[tuple[RoomKey, RoomKey]] = {
    passtrough_tuple
    for passtrough_tuple, closeness in ROOM_CLOSENESS.items()
    if closeness == PASSTHROUGH
}

PASSTHROUGH_CANDIDATE_KEYS: set[tuple[RoomUseKey, RoomUseKey]] = {
    (RoomUseKey.MB, RoomUseKey.WF),
    (RoomUseKey.AZ, RoomUseKey.LR),
}

assert (
    (N := len(ROOMS)) == len(ROOM_USES)
), "as we do 1-to-1 assignment, the number of rooms has to equal the number of room uses"
