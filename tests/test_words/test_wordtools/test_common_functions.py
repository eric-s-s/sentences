import unittest

from sentences.words.wordtools.common_functions import (bold, add_s, add_ed, needs_es, is_y_as_long_vowel_sound,
                                                        ends_with_short_vowel_and_consonant)


class TestCommonFunctions(unittest.TestCase):
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

    def test_is_y_as_long_vowel_edge_case_with_space(self):
        self.assertFalse(is_y_as_long_vowel_sound('this is a y'))

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

    def test_bold_regular(self):
        self.assertEqual(bold('x'), '<bold>x</bold>')

    def test_bold_half_tag(self):
        self.assertEqual(bold('<bold>x'), '<bold><bold>x</bold>')
        self.assertEqual(bold('x</bold>'), '<bold>x</bold></bold>')

    def test_bold_full_tag(self):
        self.assertEqual(bold('<bold>x</bold>'), '<bold>x</bold>')
        
    def test_add_s_needs_es(self):
        es_words = ('buzz', 'fitch', 'fess', 'ax', 'dish', 'bobo')
        for word in es_words:
            self.assertEqual(add_s(word), word + 'es')

    def test_add_s_ies(self):
        self.assertEqual(add_s('baby'), 'babies')
        self.assertEqual(add_s('harpy'), 'harpies')
        self.assertEqual(add_s('cry'), 'cries')

        self.assertNotEqual(add_s('play'), 'plaies')

    def test_add_s_others(self):
        self.assertEqual(add_s('play'), 'plays')
        self.assertEqual(add_s('baa'), 'baas')
        self.assertEqual(add_s('egg'), 'eggs')
        
    def test_add_ed_doubles_consonant(self):
        self.assertEqual(add_ed('pit'), 'pitted')

    def test_add_ed_regular_case(self):
        self.assertEqual(add_ed('plait'), 'plaited')
        self.assertEqual(add_ed('play'), 'played')
        self.assertEqual(add_ed('plow'), 'plowed')
        self.assertEqual(add_ed('bark'), 'barked')

    def test_add_ed_y_to_ied(self):
        self.assertEqual(add_ed('ply'), 'plied')
        self.assertEqual(add_ed('baby'), 'babied')

    def test_add_ed_does_not_duplicate_d(self):
        self.assertEqual(add_ed('like'), 'liked')


