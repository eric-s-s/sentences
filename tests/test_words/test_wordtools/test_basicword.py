import unittest

from sentences.words.basicword import BasicWord
from sentences.words.wordtools.tags import Tags
from sentences.words.wordtools.wordtag import WordTag


class TestBasicWord(unittest.TestCase):

    def setUp(self):
        self.preposition = Tags([WordTag.PREPOSITION])
        self.particle = Tags([WordTag.SEPARABLE_PARTICLE])


    def test_init_empty_tags(self):
        word = BasicWord('hi')
        self.assertEqual(word.value, 'hi')
        self.assertEqual(word.tags, Tags())

    def test_init_non_empty_tags(self):
        word = BasicWord('a', tags=self.preposition)
        self.assertEqual(word.value, 'a')
        self.assertEqual(word.tags, self.preposition)

    def test_equality_true_and_then_false_by_value(self):
        word = BasicWord('a', tags=self.particle)
        equal = BasicWord('a', tags=self.particle)
        not_equal = BasicWord('b', tags=self.particle)
        self.assertEqual(word, equal)
        self.assertNotEqual(word, not_equal)

    def test_equality_true_and_then_false_by_tags(self):
        word = BasicWord('a', tags=self.particle)
        equal = BasicWord('a', tags=self.particle)
        not_equal = BasicWord('a', tags=self.preposition)
        self.assertEqual(word, equal)
        self.assertNotEqual(word, not_equal)

    def test_capitalize(self):
        word = BasicWord('abc', tags=self.preposition)
        self.assertEqual(word.capitalize(), BasicWord('Abc', tags=self.preposition))

        capital = BasicWord('ABC')
        self.assertEqual(capital.capitalize(), capital)

    def test_de_capitalize(self):
        word = BasicWord('ABC', tags=self.particle)
        self.assertEqual(word.de_capitalize(), BasicWord('aBC', tags=self.particle))

        lower = BasicWord('abc')
        self.assertEqual(lower.de_capitalize(), lower)

    def test_bold(self):
        word = BasicWord('a', tags=self.preposition)
        bolded = BasicWord('<bold>a</bold>', tags=self.preposition)

        self.assertEqual(word.bold(), bolded)
        self.assertEqual(word.bold().bold().bold(), bolded)

    def test_repr(self):
        word = BasicWord('a', tags=self.preposition)
        self.assertEqual(repr(word), "BasicWord('a', Tags([WordTag.PREPOSITION]))")

    def test_hash(self):
        word = BasicWord('a', tags=self.preposition)
        hash_val = "hash of BasicWord('a', Tags([WordTag.PREPOSITION]))"
        self.assertEqual(hash(word), hash(hash_val))
