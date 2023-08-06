from enum import Enum


class FirstMotion(str, Enum):
    UP_WEAK = "UP_WEAK"
    UP = "UP"
    DOWN_WEAK = "DOWN_WEAK"
    DOWN = "DOWN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    Z = "Z"
    N = "N"
    DOT = "DOT"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
