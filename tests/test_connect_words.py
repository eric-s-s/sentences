import unittest

from sentences.words.pronoun import Pronoun, Word
from sentences.words.verb import BasicVerb
from sentences.words.noun import Noun
from sentences.words.punctuation import Punctuation

from sentences.wordconnector import connect_words


class TestWordConnector(unittest.TestCase):
    def test_connect_words_no_punctuation(self):
        lst = [Pronoun.I, Word('like'), Word('big'), Word('butts')]
        self.assertEqual(connect_words(lst), 'I like big butts')

    def test_connect_words_with_punctuation(self):
        lst = [Word('on').capitalize(), Word('Tuesday'), Punctuation.COMMA, Pronoun.I,
               BasicVerb('see', 'saw').past_tense(), Noun('A').indefinite(), Punctuation.COMMA, Noun('B').indefinite(),
               Punctuation.COMMA, Word('and'), Noun('C').indefinite(), Punctuation.EXCLAMATION]
        self.assertEqual(connect_words(lst), "On Tuesday, I saw an A, a B, and a C!")

    def test_complex_case(self):
        lst = [Pronoun.US.subject().capitalize(), BasicVerb('eat', 'ate').negative().past_tense(),
               Noun('cake').plural().capitalize().definite(), Word('or'),
               Noun('octopus', 'octopodes').definite().plural().capitalize(), Punctuation.PERIOD]
        self.assertEqual(connect_words(lst), "We didn't eat the Cakes or The octopodes.")
