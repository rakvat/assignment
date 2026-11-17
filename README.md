# Room Assignment Optimization

Python script that solves a concrete room-assignment problem with various
constraints. The goal is to find the optimal 1-to-1 assignment of rooms to
their occupants ("uses").

The solver minimizes a weighted penalty for moving people out of their
current rooms, plus a bonus term for room-size suitability, subject to hard
constraints (room capacities, house/floor wishes, passthrough rules, etc.).

The code uses the CP-SAT solver from or-tools.

## Run

```
python cp_sat_assignment.py
```
