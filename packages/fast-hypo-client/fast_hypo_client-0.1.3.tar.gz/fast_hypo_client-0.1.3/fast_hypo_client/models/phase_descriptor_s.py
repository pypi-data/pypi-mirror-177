from enum import Enum


class PhaseDescriptorS(str, Enum):
    S = "S"
    N = "N"
    E = "E"
    VALUE_3 = " "

    def __str__(self) -> str:
        return str(self.value)
