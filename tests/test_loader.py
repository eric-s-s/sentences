import unittest

from sentences.loader import load_csv, countable_nouns, uncountable_nouns, verbs, get_verb_dict
from sentences.words.noun import Noun
from sentences.words.verb import BasicVerb
from sentences.words.word import Word


class TestLoader(unittest.TestCase):
    def test_load_csv_nouns(self):
        answer = load_csv('nouns.csv')
        self.assertIn(['person', 'people'], answer)
        self.assertIn(['witch'], answer)

    def test_load_csv_verbs(self):
        answer = load_csv('verbs.csv')
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
        self.assertEqual(answer, {'verb': BasicVerb('fly', 'flew'), 'preposition': None, 'objects': 0})

    def test_get_verb_dict_no_object_num(self):
        answer = get_verb_dict(['fly', 'flew', 'null'])
        self.assertEqual(answer, {'verb': BasicVerb('fly', 'flew'), 'preposition': None, 'objects': 1})

    def test_get_verb_dict_null_values(self):
        answer = get_verb_dict(['fly', 'null', 'null'])
        self.assertEqual(answer, {'verb': BasicVerb('fly', ''), 'preposition': None, 'objects': 1})

    def test_get_verb_dict_no_null_values(self):
        answer = get_verb_dict(['fly', 'flew', 'with', '2'])
        self.assertEqual(answer, {'verb': BasicVerb('fly', ''), 'preposition': Word('with'), 'objects': 2})

    def test_verbs(self):
        answer = verbs()
        give = {'verb': BasicVerb('give', 'gave'), 'preposition': None, 'objects': 2}
        grab = {'verb': BasicVerb('grab', ''), 'preposition': None, 'objects': 1}
        fall = {'verb': BasicVerb('fall', 'fell'), 'preposition': Word('on'), 'objects': 1}

        self.assertIn(give, answer)
        self.assertIn(grab, answer)
        self.assertIn(fall, answer)
