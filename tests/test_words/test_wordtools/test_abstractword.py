import unittest

from sentences.words.wordtools.abstractword import AbstractWord
from sentences.words.wordtools.wordtag import WordTag


class DummyWord(AbstractWord):
    def __init__(self, value):
        self._value = value
        self._tags = [WordTag.INDEFINITE, WordTag.PAST]

    @property
    def value(self):
        return self._value

    def capitalize(self):
        return DummyWord(self.value[0].upper() + self.value[1:])

    def de_capitalize(self):
        return DummyWord(self.value[0].lower() + self.value[1:])

    def bold(self):
        return DummyWord('<bold>{}</bold>'.format(self.value))

    def has_tags(self, *tags):
        return all(tag in self._tags for tag in tags)


class TestAbstractWord(unittest.TestCase):
    def test_value(self):
        test = DummyWord('x')
        self.assertEqual(test.value, 'x')

    def test_capitalize(self):
        test = DummyWord('abc')
        answer = test.capitalize()
        self.assertIsInstance(answer, AbstractWord)
        self.assertEqual(answer.value, 'Abc')

    def test_capitalize_all_caps(self):
        test = DummyWord('ABC')
        answer = test.capitalize()
        self.assertEqual(answer.value, 'ABC')

    def test_de_capitalize(self):
        test = DummyWord('ABC')
        answer = test.de_capitalize()
        self.assertIsInstance(answer, AbstractWord)
        self.assertEqual(answer.value, 'aBC')

    def test_bold(self):
        test = DummyWord('a')
        answer = test.bold()
        self.assertIsInstance(answer, AbstractWord)
        self.assertEqual(answer.value, '<bold>a</bold>')

    def test_has_tags_all_true(self):
        test = DummyWord('')
        self.assertTrue(test.has_tags(WordTag.INDEFINITE))
        self.assertTrue(test.has_tags(WordTag.PAST))
        self.assertTrue(test.has_tags(WordTag.INDEFINITE, WordTag.PAST))
        self.assertTrue(test.has_tags(WordTag.PAST, WordTag.INDEFINITE))

    def test_has_tags_all_false(self):
        test = DummyWord('')
        self.assertFalse(test.has_tags(WordTag.DEFINITE))
        self.assertFalse(test.has_tags(WordTag.PROPER, WordTag.PLURAL))

    def test_has_tags_some_true(self):
        test = DummyWord('')
        self.assertFalse(test.has_tags(WordTag.DEFINITE, WordTag.INDEFINITE, WordTag.PAST))
