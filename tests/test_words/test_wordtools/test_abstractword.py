import unittest

from sentences.words.wordtools.abstractword import AbstractWord
from sentences.tags.wordtag import WordTag
from sentences.tags.tags import Tags


class DummyWord(AbstractWord):
    def __init__(self, value, tags=None):
        self._value = value
        if not tags:
            tags = Tags()
        self._tags = tags.copy()

    @property
    def value(self):
        return self._value

    @property
    def tags(self):
        return self._tags.copy()

    def capitalize(self):
        return DummyWord(self.value[0].upper() + self.value[1:])

    def de_capitalize(self):
        return DummyWord(self.value[0].lower() + self.value[1:])

    def bold(self):
        return DummyWord('<bold>{}</bold>'.format(self.value))


class TestAbstractWord(unittest.TestCase):
    def test_value(self):
        test = DummyWord('x')
        self.assertEqual(test.value, 'x')

    def test_tags(self):
        test = DummyWord('a', Tags([WordTag.PAST, WordTag.PROPER]))
        self.assertEqual(test.tags, Tags([WordTag.PAST, WordTag.PROPER]))

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

    def test_has_tags_no_tags(self):
        test = DummyWord('')
        self.assertTrue(test.has_tags())

        self.assertFalse(test.has_tags(WordTag.PLURAL))
        self.assertFalse(test.has_tags(WordTag.PLURAL, WordTag.UNCOUNTABLE))

    def test_has_tags_one_tag(self):
        test = DummyWord('', tags=Tags([WordTag.UNCOUNTABLE]))

        self.assertTrue(test.has_tags())
        self.assertTrue(test.has_tags(WordTag.UNCOUNTABLE))

        self.assertFalse(test.has_tags(WordTag.PLURAL))
        self.assertFalse(test.has_tags(WordTag.PLURAL, WordTag.UNCOUNTABLE))
        self.assertFalse(test.has_tags(WordTag.PLURAL, WordTag.PROPER))

    def test_has_tags_two_tags(self):
        test = DummyWord('', tags=Tags([WordTag.UNCOUNTABLE, WordTag.PAST]))

        self.assertTrue(test.has_tags())
        self.assertTrue(test.has_tags(WordTag.UNCOUNTABLE))
        self.assertTrue(test.has_tags(WordTag.PAST))
        self.assertTrue(test.has_tags(WordTag.PAST, WordTag.UNCOUNTABLE))

        self.assertFalse(test.has_tags(WordTag.PLURAL))
        self.assertFalse(test.has_tags(WordTag.PLURAL, WordTag.UNCOUNTABLE))
        self.assertFalse(test.has_tags(WordTag.PAST, WordTag.PLURAL, WordTag.UNCOUNTABLE))
        self.assertFalse(test.has_tags(WordTag.PLURAL, WordTag.PROPER))
