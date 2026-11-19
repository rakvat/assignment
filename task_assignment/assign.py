from .constraint_programming import assign_tasks
from .ingestion import import_data
from .print_utils import print_assignment


def main() -> None:
    data = import_data()
    assign_tasks(data)
    print_assignment(data)


if __name__ == "__main__":
    main()
