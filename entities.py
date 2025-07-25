from dataclasses import dataclass
from enums import House, RoomUseKey, RoomKey


@dataclass(frozen=True)
class Person:
    key: RoomUseKey
    current_room_key: RoomKey
    current_activity: float
    """ 0 is low, 1 is high """
    past_activity: float
    """ 0 is low, 1 is high """
    was_lucky_with_room_before: float
    """ 0 is no, 1 is yes """
    child: bool = False
    reluctance_to_move: float = 0.0
    """ 0.0 means no reluctance, 1.0 is very reluctant """
    min_room_size_wish: float | None = None

    def __repr__(self) -> str:
        return self.key.name

    @property
    def activity(self) -> float:
        if self.child:
            return 0.9  # children are not expected to work
        return 0.3 * self.past_activity + 0.7 * self.current_activity


@dataclass(frozen=True)
class Function:
    key: RoomUseKey

    def __repr__(self) -> str:
        return self.key.name


@dataclass(frozen=True)
class Room:
    key: RoomKey
    house: House
    floor: int
    size: float
    """ in square meter """
    window_to_street: bool = False

    def __repr__(self) -> str:
        return self.key.name
