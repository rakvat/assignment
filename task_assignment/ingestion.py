import csv
from pathlib import Path

from .entities import Data, Group, Person, Task

DATA_DIR = Path(__file__).parent / "data"


def _read_csv(filename: str) -> list[dict[str, str]]:
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _parse_task_ids(value: str) -> list[int]:
    return [int(part) for part in value.split(",") if part.strip()]


def import_data() -> Data:
    people = [
        Person(
            name=row["name"],
            group=row["group"],
            capacity=float(row["capacity"]),
        )
        for row in _read_csv("people.csv")
    ]
    tasks = [
        Task(
            id=int(row["id"]),
            label=row["label"],
            description=row["description"],
            score=float(row["score"]),
        )
        for row in _read_csv("tasks.csv")
    ]
    tasks_by_id = {task.id: task for task in tasks}
    groups = [
        Group(
            name=row["group"],
            members=[person for person in people if person.group == row["group"]],
            liked_tasks=[tasks_by_id[task_id] for task_id in _parse_task_ids(row["like_tasks"])],
            disliked_tasks=[tasks_by_id[task_id] for task_id in _parse_task_ids(row["dislike_tasks"])],
        )
        for row in _read_csv("preferences.csv")
    ]

    return Data(people=people, tasks=tasks, groups=groups)
