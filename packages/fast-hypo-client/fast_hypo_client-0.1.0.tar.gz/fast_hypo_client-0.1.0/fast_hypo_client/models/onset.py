from enum import Enum


class Onset(str, Enum):
    I = "i"
    E = "e"
    VALUE_2 = " "

    def __str__(self) -> str:
        return str(self.value)
