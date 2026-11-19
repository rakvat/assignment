# Assignment Optimization

The code uses the CP-SAT solver from or-tools for two application areas.

## Room Assignment

Python script that solves a concrete room-assignment problem with various
constraints. The goal is to find the optimal 1-to-1 assignment of rooms to
their occupants ("uses").

The solver minimizes a weighted penalty for moving people out of their
current rooms, plus a bonus term for room-size suitability, subject to hard
constraints (room capacities, house/floor wishes, passthrough rules, etc.).

### Run

```
python -m room_assignment.assign
```

## Task Assignment

Python script that solves a concrete task-assignment problem with various
constraints. The goal is to find the optimal assignment of tasks to groups
of people (collectives).

The solver optimizes for a fair distribution of tasks.

### Run
```
python -m task_assignment.assign
```

### Data

Input data goes in `task_assignment/data/` as `people.csv` and
`tasks.csv` (gitignored). To get started, copy the anonymized examples
into `data/` and edit them:

```
cp task_assignment/example_data/people.csv task_assignment/example_data/tasks.csv task_assignment/data/
```
