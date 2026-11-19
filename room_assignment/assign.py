from ortools.sat.python import cp_model

from .constants import NEIGHBOR, OTHER_HOUSE, SAME_FLOOR, SAME_HOUSE
from .constraints import (
    Assignments,
    allowed_rooms_for_use,
    allowed_use_pairs_for_room_pair,
    allowed_uses_for_room,
    max_distance_allowed_constraint,
    min_distance_allowed_constraint,
    small_distance_forbidden_constraint,
)
from .data import (
    FUNCTIONAL_USES,
    MIN_ROOM_SIZE,
    PASSTHROUGH_CANDIDATE_KEYS,
    PASSTHROUGH_ROOM_KEYS,
    ROOM_USES,
    ROOMS,
)
from .entities import Person
from .enums import House, RoomKey, RoomUseKey
from .print_utils import print_result

TOP_N = 10


def build_model() -> tuple[cp_model.CpModel, Assignments]:
    model = cp_model.CpModel()

    assignments: Assignments = {
        room: {use: model.new_bool_var(f"{room.name}_{use.name}") for use in RoomUseKey} for room in RoomKey
    }
    for room in RoomKey:
        model.add_exactly_one(assignments[room][use] for use in RoomUseKey)
    for use in RoomUseKey:
        model.add_exactly_one(assignments[room][use] for room in RoomKey)

    # kh1 can have only 2 uses
    allowed_uses_for_room(model, assignments, RoomKey.KH1, [RoomUseKey.P, RoomUseKey.B])

    # min/max sizes for special rooms uses
    allowed_rooms_for_use(model, assignments, RoomUseKey.B, lambda room: ROOMS[room].size >= 20)
    allowed_rooms_for_use(model, assignments, RoomUseKey.P, lambda room: ROOMS[room].size >= 16)
    allowed_rooms_for_use(model, assignments, RoomUseKey.G, lambda room: ROOMS[room].size <= 15)

    # FW and JH in separate houses
    min_distance_allowed_constraint(model, assignments, RoomUseKey.FW, RoomUseKey.JH, OTHER_HOUSE)

    # AZ in GH
    allowed_rooms_for_use(model, assignments, RoomUseKey.AZ, lambda room: ROOMS[room].house is House.GH)

    # AZ not next to CJ
    small_distance_forbidden_constraint(model, assignments, RoomUseKey.AZ, RoomUseKey.CJ, NEIGHBOR)

    # passthrough room restrictions (room1 is the one you need to pass through to reach room2)
    for room1, room2 in PASSTHROUGH_ROOM_KEYS:
        allowed_use_pairs_for_room_pair(
            model,
            assignments,
            room1,
            room2,
            lambda use1, use2: (
                use1 is not RoomUseKey.G
                # use2 is functional -> use1 needs to be functional
                and not (use2 in FUNCTIONAL_USES and use1 not in FUNCTIONAL_USES)
                # use1 and use2 non functional -> only selected uses allowed
                and not (
                    use1 not in FUNCTIONAL_USES
                    and use2 not in FUNCTIONAL_USES
                    and (use1, use2) not in PASSTHROUGH_CANDIDATE_KEYS
                )
            ),
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
            allowed_rooms_for_use(
                model,
                assignments,
                use_key,
                lambda room, min_size=person.min_room_size_wish: ROOMS[room].size >= min_size,
            )

    # ----------------- objective: minimize moves that people are reluctant to
    move_resistance_penalty = {}
    size_penalty = {}

    for use in RoomUseKey:
        if use in FUNCTIONAL_USES:
            continue

        person = ROOM_USES[use]
        assert isinstance(person, Person)
        current_room_key = person.current_room_key

        move_resistance_penalty[use] = sum(
            assignments[room][use]
            * (
                0
                if room is current_room_key
                # reluctance to move gets more weight if person is more active
                else 80 * (person.reluctance_to_move * pow(person.activity, 2))
            )
            for room in RoomKey
        )

        min_room_size_wish = person.min_room_size_wish or MIN_ROOM_SIZE

        size_penalty[use] = sum(
            assignments[room][use]
            * (
                # bonus room size (size of room - wished size) is weighted with past room size luck and activity
                (ROOMS[room].size - min_room_size_wish) * person.was_lucky_with_room_before / person.activity
            )
            for room in RoomKey
        )

    total_penalty = sum([*move_resistance_penalty.values(), *size_penalty.values()])
    model.minimize(total_penalty)

    return model, assignments


def solve_top_solutions(
    model: cp_model.CpModel,
    assignments: Assignments,
    top_n: int = TOP_N,
) -> None:
    for rank in range(1, top_n + 1):
        solver = cp_model.CpSolver()
        status = solver.solve(model)
        print_result(rank, status, solver, assignments)
        solution = [solver.Value(assignments[room][use]) for room in RoomKey for use in RoomUseKey]
        model.add_forbidden_assignments(
            [assignments[room][use] for room in RoomKey for use in RoomUseKey],
            [solution],
        )


def main() -> None:
    model, assignments = build_model()
    solve_top_solutions(model, assignments)


if __name__ == "__main__":
    main()
