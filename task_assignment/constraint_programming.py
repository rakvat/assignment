from ortools.sat.python import cp_model

from .entities import Data

# nested dict of group name/task id to 1 or 0 indicating assignment
Assignments = dict[str, dict[int, cp_model.IntVar]]


def _build_model(data: Data) -> tuple[cp_model.CpModel, Assignments]:
    model = cp_model.CpModel()
    assignments: Assignments = {
        group.name: {task.id: model.new_bool_var(f"{group.name}_{task.id}") for task in data.tasks}
        for group in data.groups
    }

    # each task is in exactly one group
    for task in data.tasks:
        model.add_exactly_one(assignments[group.name][task.id] for group in data.groups)

    # TODO add more constraints

    # TODO add objetive

    return model, assignments


def _solve(data: Data, model: cp_model.CpModel, assignments: Assignments) -> None:
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL:
        print("---Optimal solution---")
    elif status == cp_model.FEASIBLE:
        print("---Feasible solution---")
    else:
        print("---No solution found---")
        return

    # assign results to groups
    for group in data.groups:
        group.set_assigned_tasks([task for task in data.tasks if solver.Value(assignments[group.name][task.id])])


def assign_tasks(data: Data) -> None:
    model, assignments = _build_model(data)

    _solve(data, model, assignments)
