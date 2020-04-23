from enum import Enum

class AtomicStates(Enum):
    KICKSTART = 1
    CALIBRATION = 2
    CALIBRATION_DONE = 3
    ACTIVE = 4
    READY = 5
    DONE = 6
    FULL = 7