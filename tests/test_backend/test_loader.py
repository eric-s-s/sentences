import unittest

import os

from sentences.backend.loader import (load_csv, split_and_strip,
                                      countable_nouns, uncountable_nouns, verbs, get_verb_dict, LoaderError)
from sentences.words.noun import Noun, UncountableNoun
from sentences.words.verb import Verb
from sentences.words.word import Preposition
from sentences import DATA_PATH, VERBS_CSV, COUNTABLE_NOUNS_CSV
from tests import TESTS_FILES


class TestLoader(unittest.TestCase):
    def test_split_and_strip(self):
        self.assertEqual(split_and_strip('  this , is , space words, and   commas'),
                         ['this', 'is', 'space words', 'and   commas'])

    def test_load_csv_ignores_blank_lines(self):
        filename = os.path.join(TESTS_FILES, 'blank_lines.csv')
        self.assertEqual(load_csv(filename), [['a', 'b'], ['c', 'd'], ['e', 'f']])

    def test_load_csv_LoaderError(self):
        self.assertRaises(LoaderError, load_csv, os.path.join(DATA_PATH, 'go_time.ico'))
        self.assertRaises(LoaderError, load_csv, 'does_not_exist')

    def test_load_csv_nouns(self):
        filename = os.path.join(DATA_PATH, COUNTABLE_NOUNS_CSV)

        answer = load_csv(filename)
        self.assertIn(['person', 'people'], answer)
        self.assertIn(['witch'], answer)

    def test_load_csv_verbs(self):
        filename = os.path.join(DATA_PATH, VERBS_CSV)

        answer = load_csv(filename)
        self.assertIn(['hit', 'hit'], answer)
        self.assertIn(['play', 'null', 'with'], answer)
        self.assertIn(['give', 'gave', 'null', '2'], answer)

    def test_countable_nouns_empty(self):
        answer = countable_nouns()
        self.assertIn(Noun('person', 'people'), answer)
        self.assertIn(Noun('sheep', 'sheep'), answer)
        self.assertIn(Noun('apple'), answer)

    def test_uncountable_nouns_empty(self):
        answer = uncountable_nouns()
        self.assertIn(UncountableNoun('water'), answer)

    def test_countable_nouns_and_uncountable_nouns_wrong_number_of_columns(self):
        too_many_cols = os.path.join(TESTS_FILES, 'too_many.csv')
        with open(too_many_cols, 'w') as f:
            f.write('one, two, three, four, five')

        one_val = uncountable_nouns(too_many_cols)
        self.assertEqual(one_val[0], UncountableNoun('one', ''))

        two_vals = countable_nouns(too_many_cols)
        self.assertEqual(two_vals[0], Noun('one', 'two'))

        os.remove(too_many_cols)

    def test_countable_and_uncountable_nouns_empty_csv(self):
        empty = os.path.join(TESTS_FILES, 'empty.csv')
        self.assertEqual(countable_nouns(empty), [])
        self.assertEqual(uncountable_nouns(empty), [])

    def test_get_verb_dict_empty_strings(self):
        expected = {'verb': Verb('play'), 'preposition': None, 'objects': 1, 'insert_preposition': False}
        self.assertEqual(get_verb_dict(['play', '', '', '', '']), expected)
        self.assertEqual(get_verb_dict(['play', '', '', ]), expected)
        self.assertEqual(get_verb_dict(['play']), expected)

    def test_get_verb_dict_empty_and_null_strings(self):
        expected = {'verb': Verb('play'), 'preposition': None, 'objects': 1, 'insert_preposition': False}
        self.assertEqual(get_verb_dict(['play', '', 'null', '', '']), expected)
        self.assertEqual(get_verb_dict(['play', 'null', '', ]), expected)

    def test_get_verb_dict_no_object_num(self):
        answer = get_verb_dict(['fly', 'flew', 'null'])
        self.assertEqual(
            answer,
            {'verb': Verb('fly', 'flew', ''), 'preposition': None, 'objects': 1, 'insert_preposition': False})

    def test_get_verb_dict_null_values(self):
        answer = get_verb_dict(['fly', 'null', 'null'])
        self.assertEqual(
            answer,
            {'verb': Verb('fly'), 'preposition': None, 'objects': 1, 'insert_preposition': False})

    def test_get_verb_dict_no_null_values(self):
        answer = get_verb_dict(['fly', 'flew', 'with', '2'])
        self.assertEqual(
            answer,
            {'verb': Verb('fly', 'flew', ''), 'preposition': Preposition('with'),
             'objects': 2, 'insert_preposition': False})

    def test_get_verb_dict_too_many_values(self):
        answer = get_verb_dict(['fly', 'flew', 'with', '2', 'true', 'nsa', 'adfhgoerwi'])
        self.assertEqual(
            answer,
            {'verb': Verb('fly', 'flew', ''), 'preposition': Preposition('with'),
             'objects': 2, 'insert_preposition': True})

    def test_get_verb_dict_preposition_is_Preposition(self):
        answer = get_verb_dict(['fly', 'flew', 'with', '2'])
        self.assertIsInstance(answer['preposition'], Preposition)

    def test_verbs_empty(self):
        answer = verbs()
        give = {'verb': Verb('give', 'gave', ''), 'preposition': None, 'objects': 2, 'insert_preposition': False}
        grab = {'verb': Verb('grab'), 'preposition': None, 'objects': 1, 'insert_preposition': False}
        fall = {'verb': Verb('fall', 'fell', ''), 'preposition': Preposition('on'), 'objects': 1,
                'insert_preposition': False}

        self.assertIn(give, answer)
        self.assertIn(grab, answer)
        self.assertIn(fall, answer)

    def test_verbs_empty_csv(self):
        self.assertEqual(verbs(os.path.join(TESTS_FILES, 'empty.csv')), [])

    def test_verbs_with_insert_preposition(self):
        filename = os.path.join(TESTS_FILES, 'bring_to.csv')
        answer = verbs(filename)
        bring_to = {'verb': Verb('bring', 'brought', ''), 'preposition': Preposition('to'),
                    'objects': 2, 'insert_preposition': True}
        self.assertEqual(answer, [bring_to])

    def test_verbs_bad_verb_file(self):
        bad_verbs = os.path.join(TESTS_FILES, 'bad_verbs.csv')
        with open(bad_verbs, 'w') as f:
            f.write('some, of, these, should, be, ints, or, bools')

        self.assertRaises(LoaderError, verbs, bad_verbs)
        os.remove(bad_verbs)
