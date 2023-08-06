from enum import Enum, auto

class ProxyStatus(Enum):
    UNDEFINED = auto()
    STOPPED = auto()
    STARTING = auto()
    RUNNING = auto()
    READY = auto()
    ERRORED = auto()
    MARKED_FOR_DELETION = auto()
    DELETING = auto()
    DELETED = auto()