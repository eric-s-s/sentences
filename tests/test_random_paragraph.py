import random
import unittest
from unittest.mock import patch


from sentences.words.word import Word
from sentences.words.verb import BasicVerb
from sentences.words.noun import Noun
from sentences.words.punctuation import Punctuation
from sentences.words.pronoun import Pronoun

from sentences.random_paragraph import RandomParagraph, get_subj


class TestRandomParagraph(unittest.TestCase):
    def test_get_subj_does_not_pick_subj_in_predicate(self):
        predicate = [Word('hi')]
        pool = [Word('hi'), Word('ho')]
        random.seed(5)
        for _ in range(10):
            self.assertEqual(get_subj(pool, predicate), Word('ho'))

    def test_get_subj_raises_value_error(self):
        predicate = [Word('hi')]
        pool = [Word('hi')]
        self.assertRaises(ValueError, get_subj, pool, predicate)

    def test_get_subj_random_selection(self):
        predicate = [Word('oops'), Word('I'), Word('orangutan')]
        pool = [Word('orangutan'), Word('chimpanzee'), Word('monkey'), Word('loser'), Word('baby')]

        random.seed(10)
        self.assertEqual(get_subj(pool, predicate), Word('baby'))
        self.assertEqual(get_subj(pool, predicate), Word('baby'))
        self.assertEqual(get_subj(pool, predicate), Word('loser'))
        self.assertEqual(get_subj(pool, predicate), Word('loser'))
        self.assertEqual(get_subj(pool, predicate), Word('chimpanzee'))
        self.assertEqual(get_subj(pool, predicate), Word('chimpanzee'))
        self.assertEqual(get_subj(pool, predicate), Word('monkey'))

    def test_get_subject_pool_never_repeats(self):
        random.seed(10)
        rp = RandomParagraph()

        answer = rp.get_subject_pool(10)
        self.assertEqual(answer,
                         [Noun('pony'), Noun('ant'), Noun('stinky tofu'), Noun('house'), Noun('cow'), Pronoun.IT,
                          Noun('fire fighter'), Noun('money'), Noun('baby'), Noun('car')])

        answer = rp.get_subject_pool(10)
        self.assertEqual(answer,
                         [Noun('pen'), Noun('stinky tofu'), Noun('shark'), Pronoun.HE, Noun('car'), Noun('water'),
                          Noun('school'), Noun('baby'), Noun('fire fighter'), Noun('poop')])

        answer = rp.get_subject_pool(10)
        self.assertEqual(answer,
                         [Noun('leaf'), Noun('school'), Noun('bicycle'), Noun('cow'), Noun('pineapple'),
                          Noun('baby'), Noun('stinky tofu'), Noun('thunder'), Pronoun.SHE, Noun('orange')])

    def test_create_pool_paragraph(self):
        pass
