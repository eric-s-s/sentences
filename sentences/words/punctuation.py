from enum import Enum

from sentences.words.word import Word


class Punctuation(Enum):
    COMMA = ','
    PERIOD = '.'
    EXCLAMATION = '!'
    QUESTION = '?'

    def bold(self):
        return Word(self.value).bold()

    @staticmethod
    def has_tags(*tags):
        return False

    def capitalize(self):
        return self

    def de_capitalize(self):
        return self


