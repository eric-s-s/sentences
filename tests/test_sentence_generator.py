import random
import unittest


from sentences.sentence_generator import SentenceGenerator

from sentences.words.word import Word
from sentences.words.noun import Noun
from sentences.words.verb import BasicVerb
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation

period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun


class TestSentenceGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = SentenceGenerator()

    def test_random_sentence(self):
        random.seed(1)
        answer = self.generator.random_sentence()
        self.assertEqual(answer, [i, BasicVerb('feed', 'fed'), it, period])