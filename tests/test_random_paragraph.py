import random
import unittest


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

    def test_get_subject_pool_raises_overflow_error(self):
        random.seed(100)
        three_nouns = 'tests/test_files/three_nouns.csv'
        rp = RandomParagraph(uncountable_file=three_nouns, countable_file=three_nouns, p_pronoun=0.5)
        all_nouns_and_pronouns = rp.get_subject_pool(10)
        self.assertEqual(len(all_nouns_and_pronouns), 10)

        self.assertRaises(OverflowError, rp.get_subject_pool, 11)

    def test_create_pool_paragraph_subjects_in_subject_pool_and_not_in_predicate(self):
        random.seed(20)
        rp = RandomParagraph()
        paragraph = rp.create_pool_paragraph(pool_size=3, num_sentences=10)

        subjects = [Noun('cake'), Noun('child', 'children'), Noun('homework')]
        for sentence in paragraph:
            subject = sentence[0]
            predicate = sentence[1:]
            self.assertIn(subject, subjects)
            self.assertNotIn(subject, predicate)

    def test_create_pool_paragraph_raises_overflow_error_very_very_edge_case(self):
        random.seed(20)
        two_nouns = 'tests/test_files/two_nouns.csv'
        bring = 'tests/test_files/bring.csv'
        rp = RandomParagraph(uncountable_file=two_nouns, countable_file=two_nouns, verb_file=bring, p_pronoun=0.0)
        self.assertRaises(OverflowError, rp.create_pool_paragraph, 2, 10)


