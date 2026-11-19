from dataclasses import dataclass


@dataclass(frozen=True)
class Person:
    name: str
    group: str
    score: float


@dataclass(frozen=True)
class Task:
    id: int
    label: str
    description: str
    score: float

    def __repr__(self) -> str:
        return self.label


@dataclass(frozen=True)
class Group:
    name: str
    target_score: float
    members: list[Person]
    liked_tasks: list[Task]
    disliked_tasks: list[Task]
    assigned_score: float
    assigned_tasks: list[Task]

    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Data:
    people: list[Person]
    tasks: list[Task]
    groups: list[Group]
