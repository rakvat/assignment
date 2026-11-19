from dataclasses import dataclass, field


@dataclass(frozen=True)
class Person:
    name: str
    group: str
    capacity: float


@dataclass(frozen=True)
class Task:
    id: int
    label: str
    description: str
    score: float

    def __repr__(self) -> str:
        return self.label


@dataclass
class Group:
    name: str
    members: list[Person]
    liked_tasks: list[Task]
    disliked_tasks: list[Task]
    capacity: float = field(init=False, default=0.0)
    target_score: float = field(init=False, default=0.0)
    assigned_score: float = field(init=False, default=0.0)
    assigned_tasks: list[Task] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self.capacity = sum(person.capacity for person in self.members)

    def __repr__(self) -> str:
        return self.name

    def set_target_score(self, total_task_score: float, total_capacity: float) -> None:
        self.target_score = total_task_score * self.capacity / total_capacity

    def set_assigned_tasks(self, tasks: list[Task]) -> None:
        self.assigned_tasks = tasks
        self.assigned_score = sum(task.score for task in tasks)


@dataclass
class Data:
    people: list[Person]
    tasks: list[Task]
    groups: list[Group]
    total_task_score: float = field(init=False, default=0.0)
    total_capacity: float = field(init=False, default=0.0)
    score_per_capacity_unit: float = field(init=False, default=0.0)

    def __post_init__(self) -> None:
        self.total_task_score = sum(task.score for task in self.tasks)
        self.total_capacity = sum(person.capacity for person in self.people)
        self.score_per_capacity_unit = self.total_task_score / self.total_capacity

        for group in self.groups:
            group.set_target_score(total_task_score=self.total_task_score, total_capacity=self.total_capacity)

        self._validate()

    def _validate(self) -> None:
        task_ids = [task.id for task in self.tasks]
        if len(task_ids) != len(set(task_ids)):
            raise ValueError("task ids are not unique")

        group_name_list = [group.name for group in self.groups]
        if len(group_name_list) != len(set(group_name_list)):
            raise ValueError("group names are not unique")
        group_names = set(group_name_list)

        known_task_ids = set(task_ids)
        for group in self.groups:
            liked_ids = {task.id for task in group.liked_tasks}
            disliked_ids = {task.id for task in group.disliked_tasks}
            unknown_ids = (liked_ids | disliked_ids) - known_task_ids
            if unknown_ids:
                raise ValueError(f"group {group.name} references unknown task ids: {sorted(unknown_ids)}")
            if liked_ids & disliked_ids:
                raise ValueError(
                    f"group {group.name} likes and dislikes the same tasks: {sorted(liked_ids & disliked_ids)}"
                )

        for person in self.people:
            if person.capacity > 0 and person.group not in group_names:
                raise ValueError(f"person {person.name} has capacity but is not in any group")

        if self.total_capacity != sum(group.capacity for group in self.groups):
            raise ValueError("capacity numbers are inconsistent")
        if abs(self.total_task_score - sum(group.target_score for group in self.groups)) > 0.001:
            raise ValueError("target scores are inconsistent")
