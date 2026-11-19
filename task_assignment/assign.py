from .ingestion import import_data
from .print_utils import print_assignment


def main() -> None:
    data = import_data()
    # build model
    # assign
    print_assignment(data)


if __name__ == "__main__":
    main()
