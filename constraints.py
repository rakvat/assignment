import operator
from typing import Callable, Iterable, Sequence

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import Constraint, CpModel, IntegralT, LinearExprT

from data import N
from enums import RoomKey, RoomUseKey
from utils import distance, use_to_room


def max_distance_allowed_constraint(
    model: CpModel,
    assignments: list[list[cp_model.IntVar]],
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
    assignments: list[list[cp_model.IntVar]],
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
    assignments: list[list[cp_model.IntVar]],
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


ModelMethodType = Callable[
    [Sequence[LinearExprT], Iterable[Sequence[IntegralT]]], Constraint
]


def _distance_constraint(
    model_method: ModelMethodType,
    assignments: list[list[cp_model.IntVar]],
    person1: RoomUseKey,
    person2: RoomUseKey,
    distance_threshold: int,
    comparison_operator,
) -> None:
    model_method(
        [
            *[assignments[room][person1.value] for room in range(N)],
            *[assignments[room][person2.value] for room in range(N)],
        ],
        [
            [*use_to_room(room1), *use_to_room(room2)]
            for room1 in RoomKey
            for room2 in RoomKey
            if comparison_operator(distance(room1, room2), distance_threshold)
        ],
    )
