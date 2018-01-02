import unittest

from sentences.backend.loader import load_csv, split_and_strip, countable_nouns, uncountable_nouns, verbs, get_verb_dict
from sentences.words.noun import Noun
from sentences.words.verb import BasicVerb
from sentences.words.word import Word, Preposition


class TestLoader(unittest.TestCase):
    def test_split_and_strip(self):
        self.assertEqual(split_and_strip('  this , is , space words, and   commas'),
                         ['this', 'is', 'space words', 'and   commas'])

    def test_load_csv_ignores_blank_lines(self):
        filename = 'tests/test_files/blank_lines.csv'
        self.assertEqual(load_csv(filename), [['a', 'b'], ['c', 'd'], ['e', 'f']])

    def test_load_csv_nouns(self):
        answer = load_csv('sentences/data/nouns.csv')
        self.assertIn(['person', 'people'], answer)
        self.assertIn(['witch'], answer)

    def test_load_csv_verbs(self):
        answer = load_csv('sentences/data/verbs.csv')
        self.assertIn(['hit', 'hit', 'null'], answer)
        self.assertIn(['play', 'null', 'with'], answer)
        self.assertIn(['give', 'gave', 'null', '2'], answer)

    def test_countable_nouns(self):
        answer = countable_nouns()
        self.assertIn(Noun('person', 'people'), answer)
        self.assertIn(Noun('sheep', 'sheep'), answer)
        self.assertIn(Noun('apple'), answer)

    def test_uncountable_nouns(self):
        answer = uncountable_nouns()
        self.assertIn(Noun('water'), answer)

    def test_get_verb_dict_intransitive(self):
        answer = get_verb_dict(['fly', 'flew', 'null', '100'], True)
        self.assertEqual(
            answer,
            {'verb': BasicVerb('fly', 'flew'), 'preposition': None, 'objects': 0, 'insert_preposition': False})

    def test_get_verb_dict_no_object_num(self):
        answer = get_verb_dict(['fly', 'flew', 'null'])
        self.assertEqual(
            answer,
            {'verb': BasicVerb('fly', 'flew'), 'preposition': None, 'objects': 1, 'insert_preposition': False})

    def test_get_verb_dict_null_values(self):
        answer = get_verb_dict(['fly', 'null', 'null'])
        self.assertEqual(
            answer,
            {'verb': BasicVerb('fly', ''), 'preposition': None, 'objects': 1, 'insert_preposition': False})

    def test_get_verb_dict_no_null_values(self):
        answer = get_verb_dict(['fly', 'flew', 'with', '2'])
        self.assertEqual(
            answer,
            {'verb': BasicVerb('fly', ''), 'preposition': Word('with'), 'objects': 2, 'insert_preposition': False})

    def test_get_verb_dict_preposition_is_Preposition(self):
        answer = get_verb_dict(['fly', 'flew', 'with', '2'])
        self.assertIsInstance(answer['preposition'], Preposition)

    def test_verbs(self):
        answer = verbs()
        give = {'verb': BasicVerb('give', 'gave'), 'preposition': None, 'objects': 2, 'insert_preposition': False}
        grab = {'verb': BasicVerb('grab', ''), 'preposition': None, 'objects': 1, 'insert_preposition': False}
        fall = {'verb': BasicVerb('fall', 'fell'), 'preposition': Word('on'), 'objects': 1, 'insert_preposition': False}

        self.assertIn(give, answer)
        self.assertIn(grab, answer)
        self.assertIn(fall, answer)

    def test_load_verbs_with_insert_preposition(self):
        answer = verbs('tests/test_files/bring_to.csv')
        bring_to = {'verb': BasicVerb('bring', 'brought'), 'preposition': Word('to'),
                    'objects': 2, 'insert_preposition': True}
        self.assertEqual(answer, [bring_to])
