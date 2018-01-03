import random
import unittest

from sentences.backend.random_paragraph import RandomParagraph, get_subj
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import BasicVerb
from sentences.words.word import Word, Preposition

period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION
i, me, you, he, him, she, her, it, we, us, they, them = Pronoun


class TestRandomParagraph(unittest.TestCase):
    def setUp(self):
        self.countable = [Noun('dog'), Noun('cat'), Noun('pig'), Noun('frog')]
        self.uncountable = [Noun('water'), Noun('rice'), Noun('milk'), Noun('sand')]
        self.verbs = [
            {'verb': BasicVerb('eat'), 'preposition': None, 'objects': 1, 'insert_preposition': False},
            {'verb': BasicVerb('give'), 'preposition': None, 'objects': 2, 'insert_preposition': False},
            {'verb': BasicVerb('jump'), 'preposition': Preposition('over'), 'objects': 1, 'insert_preposition': False},
            {'verb': BasicVerb('give'), 'preposition': Preposition('to'), 'objects': 2, 'insert_preposition': True},
        ]
        self.rp = RandomParagraph(0.2, self.verbs, self.countable, self.uncountable)

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

        answer = self.rp.get_subject_pool(15)
        self.assertEqual(answer,
                         [Noun('milk'), Noun('dog'), Noun('sand'), Noun('pig'), it, Noun('frog'), Noun('rice'),
                          you, Noun('water'), i, Noun('cat'), we, they, she, he])

        answer = self.rp.get_subject_pool(15)
        self.assertEqual(answer,
                         [Noun('cat'), Noun('water'), Noun('sand'), Noun('milk'), Noun('frog'), Noun('rice'),
                          they, she, Noun('dog'), we, Noun('pig'), i, it, you, he])

    def test_get_subject_pool_raises_overflow_error(self):
        self.assertRaises(OverflowError, self.rp.get_subject_pool, 16)

    def test_create_pool_paragraph_is_correct_length(self):
        verb_list = [{'verb': BasicVerb('play'), 'preposition': None, 'objects': 0, 'insert_preposition': False}]
        rp = RandomParagraph(0.2, verb_list, self.countable, self.uncountable)

        for length in range(3, 11):
            pool = length - 2
            answer = rp.create_pool_paragraph(pool, length)
            self.assertEqual(len(answer), length)

    def test_create_pool_paragraph_subjects_in_subject_pool_and_not_in_predicate(self):
        random.seed(20)
        paragraph = self.rp.create_pool_paragraph(pool_size=3, num_sentences=20)

        subjects = [Noun('pig'), Noun('cat'), she]
        for sentence in paragraph:
            subject = sentence[0]
            predicate = sentence[1:]
            self.assertIn(subject, subjects)
            self.assertNotIn(subject, predicate)

    def test_create_pool_paragraph_raises_overflow_error_very_very_edge_case(self):
        random.seed(20)
        verb_list = [{'verb': BasicVerb('give'), 'preposition': None, 'objects': 2, 'insert_preposition': False}]

        raise_error = RandomParagraph(0.0, verb_list, [Noun('cat')], [Noun('water')])

        self.assertRaises(OverflowError, raise_error.create_pool_paragraph, 2, 10)
        no_error = RandomParagraph(0.0, self.verbs, [Noun('cat')], [Noun('water')])
        no_error.create_pool_paragraph(2, 100)

    def test_create_pool_paragraph_output(self):
        random.seed(3)
        paragraph = self.rp.create_pool_paragraph(2, 5)
        expected = [
            [Noun('pig'), BasicVerb('eat'), Noun('sand'), period],
            [Noun('pig'), BasicVerb('give'), Noun('cat'), Preposition('to'), Noun('dog'), period],
            [Noun('sand'), BasicVerb('jump'), Preposition('over'), Noun('milk'), exclamation],
            [Noun('sand'), BasicVerb('eat'), him, period],
            [Noun('sand'), BasicVerb('jump'), Preposition('over'), Noun('milk'), exclamation]
        ]
        self.assertEqual(paragraph, expected)

    def test_create_chain_paragraph_is_correct_length(self):
        for length in range(3, 11):
            answer = self.rp.create_chain_paragraph(length)
            self.assertEqual(len(answer), length)

    def test_create_chain_paragraph_loop_safety_finally_returns_paragraph_with_repeat_words(self):
        random.seed(20)
        verb_list = [{'verb': BasicVerb('give'), 'preposition': None, 'objects': 2, 'insert_preposition': False}]

        repeats = RandomParagraph(0.0, verb_list, [Noun('joe')], [Noun('bob')])
        paragraph = repeats.create_chain_paragraph(3)
        expected = [
            [Noun('joe'), BasicVerb('give'), Noun('joe'), Noun('bob'), period],
            [Noun('bob'), BasicVerb('give'), Noun('bob'), Noun('joe'), exclamation],
            [Noun('joe'), BasicVerb('give'), Noun('bob'), Noun('joe'), period],
        ]
        self.assertEqual(expected, paragraph)

    def test_create_chain_paragraph_pronouns(self):
        verb_list = [{'verb': BasicVerb('eat'), 'preposition': None, 'objects': 1, 'insert_preposition': False}]

        rp = RandomParagraph(1.0, verb_list, self.countable, self.uncountable)
        answer = rp.create_chain_paragraph(10)
        for back_index, sentence in enumerate(answer[1:]):
            previous_obj = answer[back_index][-2]
            current_subj = sentence[0]
            self.assertEqual(previous_obj.subject(), current_subj)

    def test_create_chain_paragraph_nouns(self):
        rp = RandomParagraph(0.0, self.verbs, self.countable, self.uncountable)
        answer = rp.create_chain_paragraph(10)
        for back_index, sentence in enumerate(answer[1:]):
            previous_obj = answer[back_index][-2]
            current_subj = sentence[0]
            self.assertEqual(previous_obj, current_subj)

    def test_create_chain_paragraph_assigns_random_subj_if_no_obj(self):
        random.seed(11)
        verb_list = [{'verb': BasicVerb('jump'), 'preposition': None, 'objects': 0, 'insert_preposition': False}]
        rp = RandomParagraph(0.2, verb_list, self.countable, self.uncountable)
        answer = rp.create_chain_paragraph(3)
        expected = [
            [Noun('sand'), BasicVerb('jump'), exclamation],
            [Noun('frog'), BasicVerb('jump'), exclamation],
            [Noun('pig'), BasicVerb('jump'), period]
        ]
        self.assertEqual(expected, answer)

    def test_create_chain_paragraph_output(self):
        random.seed(4567)
        answer = self.rp.create_chain_paragraph(4)
        expected = [
            [Noun('water'), BasicVerb('eat'), Noun('rice'), exclamation],
            [Noun('rice'), BasicVerb('give'), us, Preposition('to'), Noun('cat'), period],
            [Noun('cat'), BasicVerb('eat'), Noun('dog'), period],
            [Noun('dog'), BasicVerb('jump'), Preposition('over'), Noun('sand'), period],
        ]
        self.assertEqual(answer, expected)