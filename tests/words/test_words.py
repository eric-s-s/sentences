import unittest

from sentences.words.word import Word, needs_es, is_y_as_long_vowel_sound, ends_with_short_vowel_and_consonant


class TestWord(unittest.TestCase):

    def test_needs_es_true(self):
        self.assertTrue(needs_es('fizz'))
        self.assertTrue(needs_es('fitch'))
        self.assertTrue(needs_es('fess'))
        self.assertTrue(needs_es('fix'))
        self.assertTrue(needs_es('fish'))
        self.assertTrue(needs_es('sh'))
        self.assertTrue(needs_es('z'))
        self.assertTrue(needs_es('go'))

    def test_needs_es_false(self):
        for ending in 'abcdefghijklmnpqrtuvwy':
            word = 'ba' + ending
            self.assertFalse(needs_es(word))

        self.assertFalse(needs_es('pea'))
        self.assertFalse(needs_es('lib'))
        self.assertFalse(needs_es('mic'))
        self.assertFalse(needs_es('did'))

    def test_is_y_as_long_vowel_only_y(self):
        self.assertFalse(is_y_as_long_vowel_sound('y'))

    def test_is_y_as_long_vowel_y_is_a_helper(self):
        self.assertFalse(is_y_as_long_vowel_sound('key'))
        self.assertFalse(is_y_as_long_vowel_sound('play'))
        self.assertFalse(is_y_as_long_vowel_sound('boy'))

    def test_is_y_as_long_vowel_y_no_y_ending(self):
        self.assertFalse(is_y_as_long_vowel_sound('babyboo'))
        self.assertFalse(is_y_as_long_vowel_sound('crying'))

    def test_is_y_as_long_vowel_y_true(self):
        self.assertTrue(is_y_as_long_vowel_sound('cry'))
        self.assertTrue(is_y_as_long_vowel_sound('my'))
        self.assertTrue(is_y_as_long_vowel_sound('baby'))
        self.assertTrue(is_y_as_long_vowel_sound('tummy'))

    def test_ends_with_short_vowel_and_consonant_y_w(self):
        self.assertFalse(ends_with_short_vowel_and_consonant('show'))
        self.assertFalse(ends_with_short_vowel_and_consonant('play'))

    def test_ends_with_short_vowel_and_consonant_ends_with_vowel(self):
        self.assertFalse(ends_with_short_vowel_and_consonant('pee'))
        self.assertFalse(ends_with_short_vowel_and_consonant('why'))
        self.assertFalse(ends_with_short_vowel_and_consonant('happy'))
        self.assertFalse(ends_with_short_vowel_and_consonant('bola'))
        self.assertFalse(ends_with_short_vowel_and_consonant('yo'))
        self.assertFalse(ends_with_short_vowel_and_consonant('et tu'))
        self.assertFalse(ends_with_short_vowel_and_consonant('ski'))

    def test_ends_with_short_vowel_and_consonant_double_vowels(self):
        self.assertFalse(ends_with_short_vowel_and_consonant('week'))
        self.assertFalse(ends_with_short_vowel_and_consonant('weak'))
        self.assertFalse(ends_with_short_vowel_and_consonant('rain'))
        self.assertFalse(ends_with_short_vowel_and_consonant('rein'))
        self.assertFalse(ends_with_short_vowel_and_consonant('noun'))
        self.assertFalse(ends_with_short_vowel_and_consonant('lion'))
        self.assertFalse(ends_with_short_vowel_and_consonant('pool'))
        self.assertFalse(ends_with_short_vowel_and_consonant('loud'))

    def test_ends_with_short_vowel_and_consonant_double_consonant(self):
        self.assertFalse(ends_with_short_vowel_and_consonant('bowl'))
        self.assertFalse(ends_with_short_vowel_and_consonant('sign'))
        self.assertFalse(ends_with_short_vowel_and_consonant('roll'))
        self.assertFalse(ends_with_short_vowel_and_consonant('old'))
        self.assertFalse(ends_with_short_vowel_and_consonant('jump'))
        self.assertFalse(ends_with_short_vowel_and_consonant('butt'))

    def test_ends_with_short_vowel_and_consonant_true(self):
        self.assertTrue('bit')
        self.assertTrue('habit')
        self.assertTrue('rabbit')
        self.assertTrue('bat')
        self.assertTrue('bet')
        self.assertTrue('hop')
        self.assertTrue('cut')

    def test_word_value(self):
        word = Word('hi')
        self.assertEqual(word.value, 'hi')

    def test_word_str(self):
        word = Word('hi')
        self.assertEqual(str(word), 'hi')

    def test_word_repr(self):
        word = Word('hi')
        self.assertEqual(repr(word), "Word('hi')")

    def test_word_value_str_repr_remove_external_white_space(self):
        value = '   hi there  '
        expected = 'hi there'

        word = Word(value)
        self.assertEqual(word.value, expected)
        self.assertEqual(str(word), expected)
        self.assertEqual(repr(word), 'Word({!r})'.format(expected))

    def test_word_equal(self):
        word = Word('hi')
        eq = Word('hi')
        also_eq = Word('  hi  ')
        ne = Word('hiiii')
        self.assertTrue(word.__eq__(eq))
        self.assertTrue(word.__eq__(also_eq))
        self.assertFalse(word.__eq__(ne))
        self.assertFalse(word.__eq__('hi'))

    def test_word_equal_case_sensitive(self):
        self.assertEqual(Word('Hi'), Word('Hi'))
        self.assertNotEqual(Word('hi'), Word('Hi'))

    def test_word_not_equal(self):
        word = Word('hi')
        eq = Word('hi')
        also_eq = Word('  hi  ')
        ne = Word('hiiii')
        self.assertFalse(word.__ne__(eq))
        self.assertFalse(word.__ne__(also_eq))
        self.assertTrue(word.__ne__(ne))
        self.assertTrue(word.__ne__('hi'))

    def test_word_lt(self):
        word = Word('ab')
        lt = Word('a')
        gt = Word('aba')
        eq = Word('ab')

        self.assertTrue(word.__lt__(gt))
        self.assertFalse(word.__lt__(eq))
        self.assertFalse(word.__lt__(lt))

    def test_word_le(self):
        word = Word('ab')
        lt = Word('a')
        gt = Word('aba')
        eq = Word('ab')

        self.assertTrue(word.__le__(gt))
        self.assertTrue(word.__le__(eq))
        self.assertFalse(word.__le__(lt))

    def test_word_gt(self):
        word = Word('ab')
        lt = Word('a')
        gt = Word('aba')
        eq = Word('ab')

        self.assertFalse(word.__gt__(gt))
        self.assertFalse(word.__gt__(eq))
        self.assertTrue(word.__gt__(lt))

    def test_word_ge(self):
        word = Word('ab')
        lt = Word('a')
        gt = Word('aba')
        eq = Word('ab')

        self.assertFalse(word.__ge__(gt))
        self.assertTrue(word.__ge__(eq))
        self.assertTrue(word.__ge__(lt))

    def test_hash(self):
        word = Word('asjdkfj')
        self.assertEqual(hash(word), hash('hash of ' + repr(word)))

    def test_word_add_s(self):
        word = Word('buzz')
        self.assertEqual(word.add_s(), Word('buzzes'))

        word = Word('fly')
        self.assertEqual(word.add_s(), Word('flies'))

        word = Word('half')
        self.assertEqual(word.add_s(), Word('halves'))

        word = Word('bake')
        self.assertEqual(word.add_s(), Word('bakes'))

    def test_word_add_ed(self):
        word = Word('pit')
        self.assertEqual(word.add_ed(), Word('pitted'))

        word = Word('plait')
        self.assertEqual(word.add_ed(), Word('plaited'))

        word = Word('ply')
        self.assertEqual(word.add_ed(), Word('plied'))

        word = Word('play')
        self.assertEqual(word.add_ed(), Word('played'))

        word = Word('plow')
        self.assertEqual(word.add_ed(), Word('plowed'))

        word = Word('like')
        self.assertEqual(word.add_ed(), Word('liked'))

    def test_word_capitalize(self):
        word = Word(' my word ')
        self.assertEqual(word.capitalize(), Word('My word'))
