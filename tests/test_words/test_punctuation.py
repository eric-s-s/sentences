import unittest

from sentences.words.punctuation import Punctuation
from sentences.words.basicword import BasicWord
from sentences.words.wordtools.wordtag import WordTag

comma, period, exclamation, question = Punctuation


class TestPunctuation(unittest.TestCase):
    def test_values(self):
        self.assertEqual(comma.value, ',')
        self.assertEqual(period.value, '.')
        self.assertEqual(exclamation.value, '!')
        self.assertEqual(question.value, '?')

    def test_bold(self):
        self.assertEqual(comma.bold(), BasicWord('<bold>,</bold>'))
        self.assertEqual(period.bold(), BasicWord('<bold>.</bold>'))
        self.assertEqual(exclamation.bold(), BasicWord('<bold>!</bold>'))
        self.assertEqual(question.bold(), BasicWord('<bold>?</bold>'))

    def test_has_tags(self):
        for tag in WordTag.__members__.values():
            for punctuation in Punctuation.__members__.values():
                self.assertFalse(punctuation.has_tags(tag))

    def test_capitalize(self):
        for punctuation in Punctuation.__members__.values():
            self.assertEqual(punctuation, punctuation.capitalize())

    def test_de_capitalize(self):
        for punctuation in Punctuation.__members__.values():
            self.assertEqual(punctuation, punctuation.de_capitalize())

