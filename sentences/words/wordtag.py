from enum import Enum


class WordTag(Enum):
    UNCOUNTABLE = 1
    PLURAL = 2
    DEFINITE = 3
    INDEFINITE = 4
    PROPER = 5

    THIRD_PERSON = 6
    NEGATIVE = 7
    PAST = 8

    PREPOSITION = 9
    SEPARABLE_PARTICLE = 10

    def __lt__(self, other):
        return self.value < other.value

