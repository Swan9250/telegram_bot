from enum import Enum, IntEnum


class Place(IntEnum):
    RETURN: int = 0
    GENERATE: int = 1
    BASE: int = 2


class Level(IntEnum):
    EXIT: int = 0
    EASY: int = 1
    MEDIUM: int = 2
    HARD: int = 3
