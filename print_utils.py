from ortools.sat.python import cp_model

from constraints import Assignments
from data import ROOM_USES, ROOMS
from enums import RoomKey, RoomUseKey


def print_result(
    rank: int,
    status: cp_model.CpSolverStatus,
    solver: cp_model.CpSolver,
    room_assignments: Assignments,
) -> None:
    print(f"*Rank {rank:2}************")
    if status == cp_model.OPTIMAL:
        print("Optimal solution")
    elif status == cp_model.FEASIBLE:
        print("Feasible solution")
    else:
        print("No solution found")
        return

    print(f"Objective: {solver.objective_value:.2f}")
    print("********************")
    for room in RoomKey:
        assigned_use = next(use for use in RoomUseKey if solver.Value(room_assignments[room][use]))
        print(f"{ROOMS[room].__repr__():4} -> {ROOM_USES[assigned_use]}")

    print("********************")
