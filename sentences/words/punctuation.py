from abc import ABCMeta
from enum import Enum

from sentences.words.wordtools.abstractword import AbstractWord
from sentences.words.wordtools.common_functions import bold


class Punctuation(Enum):
    COMMA = ','
    PERIOD = '.'
    EXCLAMATION = '!'
    QUESTION = '?'

    BOLD_COMMA = bold(',')
    BOLD_PERIOD = bold('.')
    BOLD_EXCLAMATION = bold('!')
    BOLD_QUESTION = bold('?')

    def bold(self):
        try:
            return getattr(Punctuation, 'BOLD_{}'.format(self.name))
        except AttributeError:
            return self

    @staticmethod
    def has_tags(*tags):
        return False

    def capitalize(self):
        return self

    def de_capitalize(self):
        return self


ABCMeta.register(AbstractWord, Punctuation)
