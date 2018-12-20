import unittest

from sentences.words.wordtools.abstractword import AbstractWord
from sentences.words.punctuation import Punctuation
from sentences.words.basicword import BasicWord
from sentences.tags.wordtag import WordTag


class TestPunctuation(unittest.TestCase):
    def test_register_as_subclass_of_AbstractWord(self):
        self.assertTrue(isinstance(Punctuation.COMMA, AbstractWord))

    def test_values(self):
        self.assertEqual(Punctuation.COMMA.value, ',')
        self.assertEqual(Punctuation.PERIOD.value, '.')
        self.assertEqual(Punctuation.EXCLAMATION.value, '!')
        self.assertEqual(Punctuation.QUESTION.value, '?')

        self.assertEqual(Punctuation.BOLD_COMMA.value, '<bold>,</bold>')
        self.assertEqual(Punctuation.BOLD_PERIOD.value, '<bold>.</bold>')
        self.assertEqual(Punctuation.BOLD_EXCLAMATION.value, '<bold>!</bold>')
        self.assertEqual(Punctuation.BOLD_QUESTION.value, '<bold>?</bold>')

    def test_bold(self):
        self.assertEqual(Punctuation.COMMA.bold(), Punctuation.BOLD_COMMA)
        self.assertEqual(Punctuation.PERIOD.bold(), Punctuation.BOLD_PERIOD)
        self.assertEqual(Punctuation.EXCLAMATION.bold(), Punctuation.BOLD_EXCLAMATION)
        self.assertEqual(Punctuation.QUESTION.bold(), Punctuation.BOLD_QUESTION)

    def test_bold_already_bolded(self):
        self.assertEqual(Punctuation.BOLD_COMMA.bold(), Punctuation.BOLD_COMMA)
        self.assertEqual(Punctuation.BOLD_PERIOD.bold(), Punctuation.BOLD_PERIOD)
        self.assertEqual(Punctuation.BOLD_EXCLAMATION.bold(), Punctuation.BOLD_EXCLAMATION)
        self.assertEqual(Punctuation.BOLD_QUESTION.bold(), Punctuation.BOLD_QUESTION)

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
