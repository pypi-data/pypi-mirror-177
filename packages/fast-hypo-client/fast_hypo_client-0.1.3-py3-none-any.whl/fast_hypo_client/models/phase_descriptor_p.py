from enum import Enum


class PhaseDescriptorP(str, Enum):
    P = "P"
    G = "G"
    N = "N"
    E = "E"
    VALUE_4 = " "

    def __str__(self) -> str:
        return str(self.value)
