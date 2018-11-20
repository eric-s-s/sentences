from enum import Enum


class StatusTag(Enum):
    RAW = 1
    HAS_PLURALS = 2
    HAS_NEGATIVES = 3
    GRAMMATICAL = 4

    SIMPLE_PRESENT = 5
    SIMPLE_PAST = 6

    NOUN_ERRORS = 7
    PRONOUN_ERRORS = 8
    VERB_ERRORS = 9
    IS_DO_ERRORS = 10
    PREPOSITION_ERRORS = 11
    PUNCTUATION_ERRORS = 12

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return 'StatusTag.{}'.format(self.name)
