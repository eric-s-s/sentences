from enum import Enum

from sentences.words.word import Word


class Punctuation(Enum):
    COMMA = ','
    PERIOD = '.'
    EXCLAMATION = '!'
    QUESTION = '?'

    def bold(self):
        return Word('<bold>{}</bold>'.format(self.value))