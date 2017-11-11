import unittest

from sentences.investigation_tools import (requires_third_person, is_third_person, find_subject, is_countable,
                                           is_word_in_sentence)
from sentences.words.noun import Noun
from sentences.words.verb import BasicVerb
from sentences.words.pronoun import Pronoun

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun


class TestInvestigationTools(unittest.TestCase):
    def test_is_countable(self):
        self.assertTrue(is_countable(Noun('child', 'children')))
        self.assertFalse(is_countable(Noun('water', '')))

    def test_is_countable_defaults_to_true_unless_in_loaded_uncountable_words(self):
        self.assertTrue(is_countable(Noun('not-in-the-list juice', '')))

    def test_is_countable_correctly_identifies_definite_uncountable_from_list(self):
        self.assertFalse(is_countable(Noun('water', '').definite()))


