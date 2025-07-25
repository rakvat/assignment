from ortools.sat import cp_model_pb2
from ortools.sat.python import cp_model

from data import ROOM_USES, ROOMS, N
from enums import RoomKey, RoomUseKey


def print_result(
    rank: int,
    status: cp_model_pb2.CpSolverStatus,
    solver: cp_model.CpSolver,
    room_assignments: list[list[cp_model.IntVar]],
) -> None:
    print(f"*Rank {rank:2}************")
    if status is cp_model.OPTIMAL:
        print("Optimal solution")
    elif status is cp_model.FEASIBLE:
        print("Feasible solution")
    else:
        print("No solution found")
        return

    print(f"Objective: {solver.objective_value:.2f}")
    print("********************")
    for room in range(N):
        assigned_use = [
            use for use in range(N) if solver.Value(room_assignments[room][use])
        ][0]
        print(
            f"{ROOMS[RoomKey(room)].__repr__():4} -> {ROOM_USES[RoomUseKey(assigned_use)]}"
        )

    print("********************")
