from .entities import Data


def import_data() -> Data:
    return Data(people=[], tasks=[], groups=[])


def validate_data(data: Data) -> None:
    pass
