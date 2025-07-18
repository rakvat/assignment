from ortools.sat.python import cp_model
from data import (
    ROOMS,
    ROOM_USES,
    PASSTHROUGH_ROOM_KEYS,
    PASSTHROUGH_CANDIDATE_KEYS,
    FUNCTIONAL_USES,
)
from enums import RoomKey, RoomUseKey
from constants import OTHER_HOUSE, NEIGHBOR
from print_utils import print_result
from utils import room_to_use, use_to_room, distance

assert (N := len(ROOMS)) == len(
    ROOM_USES
), "as we do 1-to-1 assignment, the number of rooms has to equal the number of room uses"


model = cp_model.CpModel()

room_assignments = [
    [model.new_bool_var(f"room_{room}/use_{use}") for use in range(N)]
    for room in range(N)
]
for room in range(N):
    model.add_exactly_one(room_assignments[room][use] for use in range(N))
for use in range(N):
    model.add_exactly_one(room_assignments[room][use] for room in range(N))


# kh1 can have only 2 uses
model.add_allowed_assignments(
    room_assignments[RoomKey.KH1.value],
    [room_to_use(RoomUseKey.P), room_to_use(RoomUseKey.B)],
)

# min sizes for special rooms uses
model.add_allowed_assignments(
    [
        *[room_assignments[room][RoomUseKey.B.value] for room in range(N)],
    ],
    [use_to_room(room) for room in RoomKey if ROOMS[room].size >= 20],
)
model.add_allowed_assignments(
    [
        *[room_assignments[room][RoomUseKey.P.value] for room in range(N)],
    ],
    [use_to_room(room) for room in RoomKey if ROOMS[room].size >= 16],
)

# FW and JW in separate houses
model.add_allowed_assignments(
    [
        *[room_assignments[room][RoomUseKey.FW.value] for room in range(N)],
        *[room_assignments[room][RoomUseKey.JH.value] for room in range(N)],
    ],
    [
        [*use_to_room(room1), *use_to_room(room2)]
        for room1 in RoomKey
        for room2 in RoomKey
        if distance(room1, room2) >= OTHER_HOUSE
    ],
)

# AZ not next to CJ
model.add_forbidden_assignments(
    [
        *[room_assignments[room][RoomUseKey.AZ.value] for room in range(N)],
        *[room_assignments[room][RoomUseKey.CJ.value] for room in range(N)],
    ],
    [
        [*use_to_room(room1), *use_to_room(room2)]
        for room1 in RoomKey
        for room2 in RoomKey
        if distance(room1, room2) <= NEIGHBOR
    ],
)

# passthrough room restrictions (room1 is the one you need to pass through to reach room2)
for room1, room2 in PASSTHROUGH_ROOM_KEYS:
    model.add_allowed_assignments(
        [*room_assignments[room1.value], *room_assignments[room2.value]],
        [
            [*room_to_use(use1), *room_to_use(use2)]
            for use1 in RoomUseKey
            for use2 in RoomUseKey
            if use1 is not RoomUseKey.G and
            # use2 is functional -> use1 needs to be functional
            not (use2 in FUNCTIONAL_USES and not use1 in FUNCTIONAL_USES) and
            # use1 and use2 non functiona -> only selected used allowed
            not (
                use1 not in FUNCTIONAL_USES
                and use2 not in FUNCTIONAL_USES
                and (use1, use2) not in PASSTHROUGH_CANDIDATE_KEYS
            )
        ],
    )


solver = cp_model.CpSolver()
status = solver.Solve(model)
print_result(status, solver, room_assignments)
