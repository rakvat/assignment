from .ingestion import import_data, validate_data


def main() -> None:
    data = import_data()
    validate_data(data)
    # build model
    # assign
    # output


if __name__ == "__main__":
    main()
