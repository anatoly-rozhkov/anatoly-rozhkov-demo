from enum import Enum


class EventState(Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3
