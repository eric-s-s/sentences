from enum import Enum


class StatusTag(Enum):
    RAW = 1
    HAS_PLURALS = 2
    HAS_NEGATIVES = 3
    GRAMMATICAL = 4

    NOUN_ERRORS = 5
    PRONOUN_ERRORS = 6
    VERB_ERRORS = 7
    IS_DO_ERRORS = 8
    PREPOSITION_ERRORS = 9
    PUNCTUATION_ERRORS = 10

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return 'StatusTag.{}'.format(self.name)
