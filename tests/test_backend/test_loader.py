import unittest

import os

from sentences.backend.loader import (load_csv, strip_spaces,
                                      countable_nouns, uncountable_nouns, verbs, proper_nouns,
                                      get_verb_dict, LoaderError)

from sentences.words.noun import Noun
from sentences.words.verb import Verb
from sentences.words.basicword import BasicWord
from sentences.tags.wordtag import WordTag
from sentences import DATA_PATH, VERBS_CSV, COUNTABLE_NOUNS_CSV
from tests import TESTS_FILES


class TestLoader(unittest.TestCase):
    def test_strip_spaces(self):
        self.assertEqual(strip_spaces([['  this ', ' is ', ' space words'],
                                       [' and   commas']]
                                      ),
                         [['this', 'is', 'space words'], ['and   commas']])

    def test_load_csv_ignores_blank_lines(self):
        filename = os.path.join(TESTS_FILES, 'blank_lines.csv')
        self.assertEqual(load_csv(filename), [['a', 'b'], ['c', 'd'], ['e', 'f']])

    def test_load_csv_empty(self):
        filename = os.path.join(TESTS_FILES, 'empty.csv')
        self.assertEqual(load_csv(filename), [])

    def test_load_csv_ignores_comments(self):
        filename = os.path.join(TESTS_FILES, 'commented_proper.csv')
        self.assertEqual(load_csv(filename), [])

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

    def test_load_csv_empty_values(self):
        filename = os.path.join(TESTS_FILES, 'only_commas.csv')
        self.assertEqual(load_csv(filename), [])

    def test_countable_nouns_and_uncountable_nouns_wrong_number_of_columns(self):
        too_many_cols = os.path.join(TESTS_FILES, 'too_many.csv')
        with open(too_many_cols, 'w') as f:
            f.write('one, two, three, four, five')

        one_val = uncountable_nouns(too_many_cols)
        self.assertEqual(one_val[0], Noun.uncountable_noun('one'))

        two_vals = countable_nouns(too_many_cols)
        self.assertEqual(two_vals[0], Noun('one', 'two'))

        os.remove(too_many_cols)

    def test_countable_and_uncountable_nouns_empty_csv(self):
        empty = os.path.join(TESTS_FILES, 'empty.csv')
        self.assertEqual(countable_nouns(empty), [])
        self.assertEqual(uncountable_nouns(empty), [])

    def test_proper_nouns_empty_csv(self):
        empty = os.path.join(TESTS_FILES, 'empty.csv')
        self.assertEqual(proper_nouns(empty), [])

    def test_proper_nouns_non_empty_csv(self):
        proper = os.path.join(TESTS_FILES, 'uncommented_proper.csv')
        expected = [
            Noun.proper_noun('Tom'),
            Noun.proper_noun('Dick'),
            Noun.proper_noun('Harry'),
            Noun.proper_noun('the Joneses', plural=True),
            Noun.proper_noun('the Kaohsiung Elephants', plural=True),
            Noun.proper_noun('Jaces, Cunning Castaways', plural=True),
            Noun.proper_noun('Jesse, "The Body", Ventura')
        ]
        self.assertEqual(proper_nouns(proper), expected)

    def test_get_verb_dict_empty_strings(self):
        expected = {'verb': Verb('play'), 'preposition': None, 'objects': 1, 'particle': None}
        self.assertEqual(get_verb_dict(['play', '', '', '', '']), expected)
        self.assertEqual(get_verb_dict(['play', '', '', ]), expected)
        self.assertEqual(get_verb_dict(['play']), expected)

    def test_get_verb_dict_empty_and_null_strings(self):
        expected = {'verb': Verb('play'), 'preposition': None, 'objects': 1, 'particle': None}
        self.assertEqual(get_verb_dict(['play', '', 'null', '', '']), expected)
        self.assertEqual(get_verb_dict(['play', 'null', '', ]), expected)

    def test_get_verb_dict_no_object_num(self):
        answer = get_verb_dict(['fly', 'flew', 'null'])
        self.assertEqual(
            answer,
            {'verb': Verb('fly', 'flew', ''), 'preposition': None, 'objects': 1, 'particle': None})

    def test_get_verb_dict_null_values(self):
        answer = get_verb_dict(['fly', 'null', 'null'])
        self.assertEqual(
            answer,
            {'verb': Verb('fly'), 'preposition': None, 'objects': 1, 'particle': None})

    def test_get_verb_dict_no_null_values(self):
        answer = get_verb_dict(['fly', 'flew', 'with', '2'])
        self.assertEqual(
            answer,
            {'verb': Verb('fly', 'flew', ''), 'preposition': BasicWord.preposition('with'),
             'objects': 2, 'particle': None})

    def test_get_verb_dict_too_many_values(self):
        answer = get_verb_dict(['fly', 'flew', 'with', '2', 'nsa', 'adfhgoerwi'])
        self.assertEqual(
            answer,
            {'verb': Verb('fly', 'flew', ''), 'preposition': BasicWord.preposition('with'),
             'objects': 2, 'particle': None})

    def test_get_verb_dict_preposition_has_correct_tag(self):
        answer = get_verb_dict(['fly', 'flew', 'with', '2'])
        self.assertTrue(answer['preposition'].has_tags(WordTag.PREPOSITION))

    def test_get_verb_dict_phrasal_verb(self):
        answer = get_verb_dict(['take away', 'took away', 'from'])
        self.assertEqual(
            answer,
            {'verb': Verb('take', 'took', ''), 'preposition': BasicWord.preposition('from'),
             'particle': BasicWord.particle('away'), 'objects': 1})

    def test_get_verb_dict_phrasal_verb_single_value(self):
        answer = get_verb_dict(['pick up'])
        self.assertEqual(
            answer,
            {'verb': Verb('pick'), 'preposition': None, 'particle': BasicWord.particle('up'), 'objects': 1})

    def test_get_verb_dict_phrasal_verb_different_particles_raises_loader_error(self):
        self.assertRaises(LoaderError, get_verb_dict, ['throw up', 'threw out'])

    def test_verbs_empty_csv(self):
        self.assertEqual(verbs(os.path.join(TESTS_FILES, 'empty.csv')), [])

    def test_verbs_with_insert_preposition(self):
        filename = os.path.join(TESTS_FILES, 'bring_to.csv')
        answer = verbs(filename)
        bring_to = {'verb': Verb('bring', 'brought', ''), 'preposition': BasicWord.preposition('to'),
                    'objects': 2, 'particle': None}
        self.assertEqual(answer, [bring_to])

    def test_verbs_bad_verb_file(self):
        bad_verbs = os.path.join(TESTS_FILES, 'bad_verbs.csv')
        with open(bad_verbs, 'w') as f:
            f.write('some, of, these, should, be, ints')

        self.assertRaises(LoaderError, verbs, bad_verbs)
        os.remove(bad_verbs)

    def test_verbs_bad_verb_mismatched_particles(self):
        bad_verbs = os.path.join(TESTS_FILES, 'bad_verbs.csv')
        with open(bad_verbs, 'w') as f:
            f.write('take out, took away')
        with self.assertRaises(LoaderError) as cm:
            verbs(bad_verbs)
        self.assertEqual(cm.exception.args[0], 'Phrasal verb, "take", has mismatched particles: "out" and "away".')
        os.remove(bad_verbs)
