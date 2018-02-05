from enum import Enum

from sentences.words.basicword import BasicWord


class Punctuation(Enum):
    COMMA = ','
    PERIOD = '.'
    EXCLAMATION = '!'
    QUESTION = '?'

    def bold(self):
        return BasicWord(self.value).bold()

    @staticmethod
    def has_tags(*tags):
        return False

    def capitalize(self):
        return self

    def de_capitalize(self):
        return self
