import operator
from collections.abc import Callable, Iterable, Sequence

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import Constraint, CpModel, IntegralT, LinearExprT

from enums import RoomKey, RoomUseKey
from utils import distance, room_to_use, use_to_room

Assignments = dict[RoomKey, dict[RoomUseKey, cp_model.IntVar]]


def max_distance_allowed_constraint(
    model: CpModel,
    assignments: Assignments,
    person1: RoomUseKey,
    person2: RoomUseKey,
    distance_threshold: int,
) -> None:
    _distance_constraint(
        model.add_allowed_assignments,
        assignments,
        person1,
        person2,
        distance_threshold,
        operator.le,
    )


def min_distance_allowed_constraint(
    model: CpModel,
    assignments: Assignments,
    person1: RoomUseKey,
    person2: RoomUseKey,
    distance_threshold: int,
) -> None:
    _distance_constraint(
        model.add_allowed_assignments,
        assignments,
        person1,
        person2,
        distance_threshold,
        operator.ge,
    )


def small_distance_forbidden_constraint(
    model: CpModel,
    assignments: Assignments,
    person1: RoomUseKey,
    person2: RoomUseKey,
    distance_threshold: int,
) -> None:
    _distance_constraint(
        model.add_forbidden_assignments,
        assignments,
        person1,
        person2,
        distance_threshold,
        operator.le,
    )


ModelMethodType = Callable[[Sequence[LinearExprT], Iterable[Sequence[IntegralT]]], Constraint]


def allowed_rooms_for_use(
    model: CpModel,
    assignments: Assignments,
    use_key: RoomUseKey,
    room_predicate: Callable[[RoomKey], bool],
) -> None:
    model.add_allowed_assignments(
        [assignments[room][use_key] for room in RoomKey],
        [use_to_room(room_key) for room_key in RoomKey if room_predicate(room_key)],
    )


def allowed_uses_for_room(
    model: CpModel,
    assignments: Assignments,
    room_key: RoomKey,
    allowed_uses: Iterable[RoomUseKey],
) -> None:
    model.add_allowed_assignments(
        [assignments[room_key][use] for use in RoomUseKey],
        [room_to_use(use_key) for use_key in allowed_uses],
    )


def allowed_use_pairs_for_room_pair(
    model: CpModel,
    assignments: Assignments,
    room1_key: RoomKey,
    room2_key: RoomKey,
    use_pair_predicate: Callable[[RoomUseKey, RoomUseKey], bool],
) -> None:
    model.add_allowed_assignments(
        [
            *(assignments[room1_key][use] for use in RoomUseKey),
            *(assignments[room2_key][use] for use in RoomUseKey),
        ],
        [
            [*room_to_use(use1), *room_to_use(use2)]
            for use1 in RoomUseKey
            for use2 in RoomUseKey
            if use_pair_predicate(use1, use2)
        ],
    )


def _distance_constraint(
    model_method: ModelMethodType,
    assignments: Assignments,
    person1: RoomUseKey,
    person2: RoomUseKey,
    distance_threshold: int,
    comparison_operator: Callable[[int, int], bool],
) -> None:
    model_method(
        [
            *[assignments[room][person1] for room in RoomKey],
            *[assignments[room][person2] for room in RoomKey],
        ],
        [
            [*use_to_room(room1), *use_to_room(room2)]
            for room1 in RoomKey
            for room2 in RoomKey
            if comparison_operator(distance(room1, room2), distance_threshold)
        ],
    )
