from enums import RoomKey, RoomUseKey
from data import N
from utils import use_to_room, distance


def max_distance_allowed_constraint(
    model,
    assignments,
    person1: RoomUseKey,
    person2: RoomUseKey,
    distance_threshold: int,
) -> None:
    model.add_allowed_assignments(
        [
            *[assignments[room][person1.value] for room in range(N)],
            *[assignments[room][person2.value] for room in range(N)],
        ],
        [
            [*use_to_room(room1), *use_to_room(room2)]
            for room1 in RoomKey
            for room2 in RoomKey
            if distance(room1, room2) <= distance_threshold
        ],
    )


def min_distance_allowed_constraint(
    model,
    assignments,
    person1: RoomUseKey,
    person2: RoomUseKey,
    distance_threshold: int,
) -> None:
    model.add_allowed_assignments(
        [
            *[assignments[room][person1.value] for room in range(N)],
            *[assignments[room][person2.value] for room in range(N)],
        ],
        [
            [*use_to_room(room1), *use_to_room(room2)]
            for room1 in RoomKey
            for room2 in RoomKey
            if distance(room1, room2) >= distance_threshold
        ],
    )


def small_distance_forbidden_constraint(
    model,
    assignments,
    person1: RoomUseKey,
    person2: RoomUseKey,
    distance_threshold: int,
) -> None:
    model.add_forbidden_assignments(
        [
            *[assignments[room][person1] for room in range(N)],
            *[assignments[room][person2] for room in range(N)],
        ],
        [
            [*use_to_room(room1), *use_to_room(room2)]
            for room1 in RoomKey
            for room2 in RoomKey
            if distance(room1, room2) <= distance_threshold
        ],
    )
