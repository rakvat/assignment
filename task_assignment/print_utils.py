from .entities import Data, Group

SEPARATOR_LENGTH = 60
LEFT_COLUMN_WIDTH_GROUPS = 16
LEFT_COLUMN_WIDTH_HEADER = 24


def _print_group(group: Group) -> None:
    print(f"{'=' * SEPARATOR_LENGTH}\nGroup: {group.name}\n{'=' * SEPARATOR_LENGTH}")
    print(f"{'Members':<{LEFT_COLUMN_WIDTH_GROUPS}}{', '.join(person.name for person in group.members) or '(none)'}")
    print(f"{'Capacity':<{LEFT_COLUMN_WIDTH_GROUPS}}{group.capacity:g}")
    print(f"{'Target score':<{LEFT_COLUMN_WIDTH_GROUPS}}{group.target_score:.2f}")
    print(f"{'Assigned score':<{LEFT_COLUMN_WIDTH_GROUPS}}{group.assigned_score:.2f}")
    print("Assigned tasks:")
    for task in group.assigned_tasks:
        print(f"  - {task.label}: {task.description} (score: {task.score:g})")
    if not group.assigned_tasks:
        print("  (none)")
    print()


def print_assignment(data: Data) -> None:
    print(f"{'=' * SEPARATOR_LENGTH}")
    print(f"{'Total task score':<{LEFT_COLUMN_WIDTH_HEADER}}{data.total_task_score:.2f}")
    print(f"{'Total capacity':<{LEFT_COLUMN_WIDTH_HEADER}}{data.total_capacity:.2f}")
    print(f"{'Score per capacity unit':<{LEFT_COLUMN_WIDTH_HEADER}}{data.score_per_capacity_unit:.2f}")
    print(f"{'=' * SEPARATOR_LENGTH}\n")

    for group in data.groups:
        _print_group(group)
