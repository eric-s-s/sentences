import random
import unittest

from sentences.backend.random_paragraph import RandomParagraph, get_subj
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.new_word import NewNoun
from sentences.words.new_verb import NewVerb
from sentences.words.basicword import BasicWord

period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION
i, me, you, he, him, she, her, it, we, us, they, them = Pronoun.__members__.values()


class TestRandomParagraph(unittest.TestCase):
    def setUp(self):
        self.countable = [NewNoun('dog'), NewNoun('cat'), NewNoun('pig'), NewNoun('frog')]
        self.uncountable = [NewNoun('water'), NewNoun('rice'), NewNoun('milk'), NewNoun('sand')]
        self.verbs = [
            {'verb': NewVerb('eat'), 'preposition': None, 'objects': 1, 'particle': None},
            {'verb': NewVerb('give'), 'preposition': None, 'objects': 2, 'particle': None},
            {'verb': NewVerb('jump'), 'preposition': BasicWord.preposition('over'), 'objects': 1, 'particle': None},
            {'verb': NewVerb('give'), 'preposition': BasicWord.preposition('to'), 'objects': 2, 'particle': None},
        ]
        self.rp = RandomParagraph(0.2, self.verbs, self.countable + self.uncountable)

    def test_get_subj_does_not_pick_subj_in_predicate(self):
        predicate = [BasicWord('hi')]
        pool = [BasicWord('hi'), BasicWord('ho')]
        random.seed(5)
        for _ in range(10):
            self.assertEqual(get_subj(pool, predicate), BasicWord('ho'))

    def test_get_subj_raises_value_error(self):
        predicate = [BasicWord('hi')]
        pool = [BasicWord('hi')]
        self.assertRaises(ValueError, get_subj, pool, predicate)

    def test_get_subj_random_selection(self):
        predicate = [BasicWord('oops'), BasicWord('I'), BasicWord('orangutan')]
        pool = [BasicWord('orangutan'), BasicWord('chimpanzee'), BasicWord('monkey'), BasicWord('loser'),
                BasicWord('baby')]

        random.seed(10)
        self.assertEqual(get_subj(pool, predicate), BasicWord('baby'))
        self.assertEqual(get_subj(pool, predicate), BasicWord('baby'))
        self.assertEqual(get_subj(pool, predicate), BasicWord('loser'))
        self.assertEqual(get_subj(pool, predicate), BasicWord('loser'))
        self.assertEqual(get_subj(pool, predicate), BasicWord('chimpanzee'))
        self.assertEqual(get_subj(pool, predicate), BasicWord('chimpanzee'))
        self.assertEqual(get_subj(pool, predicate), BasicWord('monkey'))

    def test_get_subject_pool_never_repeats(self):
        random.seed(10)

        answer = self.rp.get_subject_pool(15)
        self.assertEqual(answer,
                         [NewNoun('milk'), NewNoun('dog'), NewNoun('sand'), NewNoun('pig'), it, NewNoun('frog'),
                          NewNoun('rice'), you, NewNoun('water'), i, NewNoun('cat'), we, they, she, he])

        answer = self.rp.get_subject_pool(15)
        self.assertEqual(answer,
                         [NewNoun('cat'), NewNoun('water'), NewNoun('sand'), NewNoun('milk'), NewNoun('frog'),
                          NewNoun('rice'), they, she, NewNoun('dog'), we, NewNoun('pig'), i, it, you, he])

    def test_get_subject_pool_raises_value_error(self):
        self.assertRaises(ValueError, self.rp.get_subject_pool, 16)

    def test_create_pool_paragraph_is_correct_length(self):
        verb_list = [{'verb': NewVerb('play'), 'preposition': None, 'objects': 0, 'particle': None}]
        rp = RandomParagraph(0.2, verb_list, self.countable + self.uncountable)

        for length in range(3, 11):
            pool = length - 2
            answer = rp.create_pool_paragraph(pool, length)
            self.assertEqual(len(answer), length)

    def test_create_pool_paragraph_subjects_in_subject_pool_and_not_in_predicate(self):
        random.seed(20)
        paragraph = self.rp.create_pool_paragraph(pool_size=3, num_sentences=20)

        subjects = [NewNoun('pig'), NewNoun('cat'), she]
        for sentence in paragraph:
            subject = sentence[0]
            predicate = sentence[1:]
            self.assertIn(subject, subjects)
            self.assertNotIn(subject, predicate)

    def test_create_pool_paragraph_repeats_very_very_edge_case(self):
        random.seed(20)
        verb_list = [{'verb': NewVerb('give'), 'preposition': None, 'objects': 2, 'particle': None}]

        repeats = RandomParagraph(0.0, verb_list, [NewNoun('cat'), NewNoun('water')])

        answer = repeats.create_pool_paragraph(2, 2)
        expected = [
            [NewNoun('water'), NewVerb('give'), NewNoun('cat'), NewNoun('water'), period],
            [NewNoun('cat'), NewVerb('give'), NewNoun('cat'), NewNoun('water'), period]
        ]
        self.assertEqual(answer, expected)

        no_prepositions = [verb_dict for verb_dict in self.verbs if verb_dict['preposition'] is None]
        no_repeats = RandomParagraph(0.0, no_prepositions, [NewNoun('cat'), NewNoun('water')])
        answer = no_repeats.create_pool_paragraph(2, 100)
        for sentence in answer:
            self.assertEqual(len(sentence), 4)
            self.assertNotEqual(sentence[0], sentence[2])

    def test_create_pool_paragraph_output(self):
        random.seed(3)
        paragraph = self.rp.create_pool_paragraph(2, 5)
        expected = [
            [NewNoun('pig'), NewVerb('eat'), NewNoun('sand'), period],
            [NewNoun('pig'), NewVerb('give'), NewNoun('cat'), BasicWord.preposition('to'), NewNoun('dog'), period],
            [NewNoun('sand'), NewVerb('jump'), BasicWord.preposition('over'), NewNoun('milk'), exclamation],
            [NewNoun('sand'), NewVerb('eat'), him, period],
            [NewNoun('sand'), NewVerb('jump'), BasicWord.preposition('over'), NewNoun('milk'), exclamation]
        ]
        self.assertEqual(paragraph, expected)

    def test_create_chain_paragraph_is_correct_length(self):
        for length in range(3, 11):
            answer = self.rp.create_chain_paragraph(length)
            self.assertEqual(len(answer), length)

    def test_create_chain_paragraph_loop_safety_finally_returns_paragraph_with_repeat_words(self):
        random.seed(20)
        verb_list = [{'verb': NewVerb('give'), 'preposition': None, 'objects': 2, 'particle': None}]

        repeats = RandomParagraph(0.0, verb_list, [NewNoun('joe'), NewNoun('bob')])
        paragraph = repeats.create_chain_paragraph(3)
        expected = [
            [NewNoun('joe'), NewVerb('give'), NewNoun('joe'), NewNoun('bob'), period],
            [NewNoun('bob'), NewVerb('give'), NewNoun('bob'), NewNoun('joe'), exclamation],
            [NewNoun('joe'), NewVerb('give'), NewNoun('bob'), NewNoun('joe'), period],
        ]
        self.assertEqual(expected, paragraph)

    def test_create_chain_paragraph_pronouns(self):
        verb_list = [{'verb': NewVerb('eat'), 'preposition': None, 'objects': 1, 'particle': None}]

        rp = RandomParagraph(1.0, verb_list, self.countable + self.uncountable)
        answer = rp.create_chain_paragraph(10)
        for back_index, sentence in enumerate(answer[1:]):
            previous_obj = answer[back_index][-2]
            current_subj = sentence[0]
            self.assertEqual(previous_obj.subject(), current_subj)

    def test_create_chain_paragraph_nouns(self):
        rp = RandomParagraph(0.0, self.verbs, self.countable + self.uncountable)
        answer = rp.create_chain_paragraph(10)
        for back_index, sentence in enumerate(answer[1:]):
            previous_obj = answer[back_index][-2]
            current_subj = sentence[0]
            self.assertEqual(previous_obj, current_subj)

    def test_create_chain_paragraph_assigns_random_subj_if_no_obj(self):
        random.seed(11)
        verb_list = [{'verb': NewVerb('jump'), 'preposition': None, 'objects': 0, 'particle': None}]
        rp = RandomParagraph(0.2, verb_list, self.countable + self.uncountable)
        answer = rp.create_chain_paragraph(3)
        expected = [
            [NewNoun('sand'), NewVerb('jump'), exclamation],
            [NewNoun('frog'), NewVerb('jump'), exclamation],
            [NewNoun('pig'), NewVerb('jump'), period]
        ]
        self.assertEqual(expected, answer)

    def test_create_chain_paragraph_output(self):
        random.seed(4567)
        answer = self.rp.create_chain_paragraph(4)
        expected = [
            [NewNoun('water'), NewVerb('eat'), NewNoun('rice'), exclamation],
            [NewNoun('rice'), NewVerb('give'), us, BasicWord.preposition('to'), NewNoun('cat'), period],
            [NewNoun('cat'), NewVerb('eat'), NewNoun('dog'), period],
            [NewNoun('dog'), NewVerb('jump'), BasicWord.preposition('over'), NewNoun('sand'), period],
        ]
        self.assertEqual(answer, expected)
