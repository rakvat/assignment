from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExprT

from .entities import Data

# nested dict of group name/task id to 1 or 0 indicating assignment
Assignments = dict[str, dict[int, cp_model.IntVar]]

# scores and target scores are floats; CP-SAT variables and abs-equality
# need integer expressions, so all penalty terms use scaled integer scores
SCORE_SCALE = 100


def _scaled_score(score: float) -> int:
    return round(score * SCORE_SCALE)


def _build_model(data: Data, dislikes_hard_constraint: bool) -> tuple[cp_model.CpModel, Assignments]:
    model = cp_model.CpModel()
    assignments: Assignments = {
        group.name: {task.id: model.new_bool_var(f"{group.name}_{task.id}") for task in data.tasks}
        for group in data.groups
    }

    # each task is in exactly one group
    for task in data.tasks:
        model.add_exactly_one(assignments[group.name][task.id] for group in data.groups)

    # no disliked tasks
    if dislikes_hard_constraint:
        for group in data.groups:
            if not group.disliked_tasks:
                continue

            for task in group.disliked_tasks:
                model.add_forbidden_assignments([assignments[group.name][task.id]], [[1]])

    # define objective
    penalty_terms: list[LinearExprT] = []
    for group in data.groups:
        # 1. distance from target score to assigned score
        assigned_score = sum(_scaled_score(task.score) * assignments[group.name][task.id] for task in data.tasks)
        deviation = model.new_int_var(0, _scaled_score(data.total_task_score), f"deviation_{group.name}")
        model.add_abs_equality(deviation, assigned_score - _scaled_score(group.target_score))
        penalty_terms.append(deviation)

        # 2. assigned disliked tasks
        penalty_terms.append(
            sum(_scaled_score(task.score) * assignments[group.name][task.id] for task in group.disliked_tasks)
        )

        # 3. not assigned liked tasks
        penalty_terms.append(
            sum(_scaled_score(task.score) * (1 - assignments[group.name][task.id]) for task in group.liked_tasks)
        )

    model.minimize(sum(penalty_terms))

    return model, assignments


def _solve(data: Data, model: cp_model.CpModel, assignments: Assignments) -> bool:
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL:
        print("---Optimal solution---")
    elif status == cp_model.FEASIBLE:
        print("---Feasible solution---")
    else:
        print("---No solution found---")
        return False

    # assign results to groups
    for group in data.groups:
        group.set_assigned_tasks([task for task in data.tasks if solver.Value(assignments[group.name][task.id])])

    return True


def assign_tasks(data: Data) -> None:
    for dislikes_hard_constraint in (True, False):
        model, assignments = _build_model(data, dislikes_hard_constraint)
        if _solve(data, model, assignments):
            return
