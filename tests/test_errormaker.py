import unittest


from sentences.errormaker import copy_paragraph, fuck_with_verb, fuck_with_noun, is_negative_verb, ErrorMaker

from sentences.words.noun import Noun, PluralNoun, IndefiniteNoun, UncountableNoun
from sentences.words.verb import BasicVerb, ConjugatedVerb
from sentences.words.punctuation import Punctuation


class TestErrorMaker(unittest.TestCase):
    pass
