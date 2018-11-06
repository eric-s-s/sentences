from enum import Enum


class StatusTag(Enum):
    RAW = 1
    HAS_PLURALS = 2
    HAS_NEGATIVES = 3
    GRAMMATICAL = 4
    HAS_ERRORS = 5

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return 'StatusTag.{}'.format(self.name)
