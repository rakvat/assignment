from ortools.sat.python import cp_model

from constants import NEIGHBOR, OTHER_HOUSE, SAME_FLOOR, SAME_HOUSE
from constraints import (
    max_distance_allowed_constraint,
    min_distance_allowed_constraint,
    small_distance_forbidden_constraint,
)
from data import (
    FUNCTIONAL_USES,
    MIN_ROOM_SIZE,
    PASSTHROUGH_CANDIDATE_KEYS,
    PASSTHROUGH_ROOM_KEYS,
    ROOM_USES,
    ROOMS,
    N,
)
from entities import Person
from enums import House, RoomKey, RoomUseKey
from print_utils import print_result
from utils import (
    room_to_use,
    use_to_room,
)

TOP_N = 10

model = cp_model.CpModel()

assignments = [
    [model.new_bool_var(f"room_{room}/use_{use}") for use in range(N)]
    for room in range(N)
]
for room in range(N):
    model.add_exactly_one(assignments[room][use] for use in range(N))
for use in range(N):
    model.add_exactly_one(assignments[room][use] for room in range(N))


# kh1 can have only 2 uses
model.add_allowed_assignments(
    assignments[RoomKey.KH1.value],
    [room_to_use(RoomUseKey.P), room_to_use(RoomUseKey.B)],
)

# min/max sizes for special rooms uses
model.add_allowed_assignments(
    [
        *[assignments[room][RoomUseKey.B.value] for room in range(N)],
    ],
    [use_to_room(room) for room in RoomKey if ROOMS[room].size >= 20],
)
model.add_allowed_assignments(
    [
        *[assignments[room][RoomUseKey.P.value] for room in range(N)],
    ],
    [use_to_room(room) for room in RoomKey if ROOMS[room].size >= 16],
)
model.add_allowed_assignments(
    [
        *[assignments[room][RoomUseKey.G.value] for room in range(N)],
    ],
    [use_to_room(room) for room in RoomKey if ROOMS[room].size <= 15],
)

# FW and JW in separate houses
min_distance_allowed_constraint(
    model, assignments, RoomUseKey.FW, RoomUseKey.JH, OTHER_HOUSE
)

# AZ in GH
model.add_allowed_assignments(
    [
        *[assignments[room][RoomUseKey.AZ.value] for room in range(N)],
    ],
    [use_to_room(room) for room in RoomKey if ROOMS[room].house is House.GH],
)

# AZ not next to CJ
small_distance_forbidden_constraint(
    model, assignments, RoomUseKey.AZ, RoomUseKey.CJ, NEIGHBOR
)

# passthrough room restrictions (room1 is the one you need to pass through to reach room2)
for room1, room2 in PASSTHROUGH_ROOM_KEYS:
    model.add_allowed_assignments(
        [*assignments[room1.value], *assignments[room2.value]],
        [
            [*room_to_use(use1), *room_to_use(use2)]
            for use1 in RoomUseKey
            for use2 in RoomUseKey
            if use1 is not RoomUseKey.G
            and
            # use2 is functional -> use1 needs to be functional
            not (use2 in FUNCTIONAL_USES and use1 not in FUNCTIONAL_USES)
            and
            # use1 and use2 non functiona -> only selected used allowed
            not (
                use1 not in FUNCTIONAL_USES
                and use2 not in FUNCTIONAL_USES
                and (use1, use2) not in PASSTHROUGH_CANDIDATE_KEYS
            )
        ],
    )

# same floor wishes
for person1, person2 in [
    (RoomUseKey.JL, RoomUseKey.FW),
    (RoomUseKey.CH, RoomUseKey.FW),
    (RoomUseKey.VH, RoomUseKey.JH),
    (RoomUseKey.MB, RoomUseKey.WF),
]:
    max_distance_allowed_constraint(model, assignments, person1, person2, SAME_FLOOR)

# same house wishes
for person1, person2 in [
    (RoomUseKey.JL, RoomUseKey.CL),
    (RoomUseKey.CH, RoomUseKey.CL),
    (RoomUseKey.CH, RoomUseKey.FW),
    (RoomUseKey.KE, RoomUseKey.CL),
    (RoomUseKey.KE, RoomUseKey.FW),
    (RoomUseKey.SW, RoomUseKey.LW),
    (RoomUseKey.AZ, RoomUseKey.LR),
    (RoomUseKey.VH, RoomUseKey.LR),
]:
    max_distance_allowed_constraint(model, assignments, person1, person2, SAME_HOUSE)

# size wishes
for use_key in RoomUseKey:
    if use_key in FUNCTIONAL_USES:
        continue
    person = ROOM_USES[use_key]
    assert isinstance(person, Person)
    if person.min_room_size_wish:
        model.add_allowed_assignments(
            [assignments[room][use_key.value] for room in range(N)],
            [
                use_to_room(room_key)
                for room_key in RoomKey
                if ROOMS[room_key].size >= person.min_room_size_wish
            ],
        )


# ----------------- objective: minimize moves that people are reluctant to
move_resistence_penality = {}
size_penality = {}

for use in RoomUseKey:
    if use in FUNCTIONAL_USES:
        continue

    person = ROOM_USES[use]
    assert isinstance(person, Person)
    current_room_key = person.current_room_key

    move_resistence_penality[use] = sum(
        assignments[room.value][use.value]
        * (
            0
            if room is current_room_key
            # reluctance to move gets more weight if person is more active
            else 80 * (person.reluctance_to_move * pow(person.activity, 2))
        )
        for room in RoomKey
    )

    min_room_size_wish = person.min_room_size_wish or MIN_ROOM_SIZE

    size_penality[use] = sum(
        assignments[room.value][use.value]
        * (
            # bonus room size (size of room - wished size) is weighted with past room size luck and activity
            (ROOMS[room].size - min_room_size_wish)
            * person.was_lucky_with_room_before
            / person.activity
        )
        for room in RoomKey
    )


total_penality = sum([*move_resistence_penality.values(), *size_penality.values()])
model.minimize(total_penality)
previous_solutions = []

for rank in range(1, TOP_N + 1):
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    print_result(rank, status, solver, assignments)
    solution = [
        solver.Value(assignments[room.value][use.value])
        for use in RoomUseKey
        for room in RoomKey
    ]
    previous_solutions.append(solution)
    model.add_forbidden_assignments(
        [assignments[room.value][use.value] for use in RoomUseKey for room in RoomKey],
        previous_solutions,
    )
