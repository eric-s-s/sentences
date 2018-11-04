import random
import unittest

from sentences.backend.random_paragraph import RandomParagraph

from sentences.word_groups.sentence import Sentence
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.noun import Noun
from sentences.words.verb import Verb
from sentences.words.basicword import BasicWord

PERIOD = Punctuation.PERIOD
EXCLAMATION = Punctuation.EXCLAMATION
I, ME, YOU, HE, HIM, SHE, HER, IT, WE, US, THEY, THEM = Pronoun.__members__.values()


class TestRandomParagraph(unittest.TestCase):
    def setUp(self):
        self.countable = [Noun('dog'), Noun('cat'), Noun('pig'), Noun('frog')]
        self.uncountable = [Noun('water'), Noun('rice'), Noun('milk'), Noun('sand')]
        self.verbs = [
            {'verb': Verb('eat'), 'preposition': None, 'objects': 1, 'particle': None},
            {'verb': Verb('give'), 'preposition': None, 'objects': 2, 'particle': None},
            {'verb': Verb('jump'), 'preposition': BasicWord.preposition('over'), 'objects': 1, 'particle': None},
            {'verb': Verb('give'), 'preposition': BasicWord.preposition('to'), 'objects': 2, 'particle': None},
        ]
        self.rp = RandomParagraph(0.2, self.verbs, self.countable + self.uncountable)

    def test_get_subject_pool_never_repeats(self):
        random.seed(10)

        answer = self.rp.get_subject_pool(15)
        self.assertEqual(answer,
                         [Noun('milk'), Noun('dog'), Noun('sand'), Noun('pig'), IT, Noun('frog'),
                          Noun('rice'), YOU, Noun('water'), I, Noun('cat'), WE, THEY, SHE, HE])

        answer = self.rp.get_subject_pool(15)
        self.assertEqual(answer,
                         [Noun('cat'), Noun('water'), Noun('sand'), Noun('milk'), Noun('frog'),
                          Noun('rice'), THEY, SHE, Noun('dog'), WE, Noun('pig'), I, IT, YOU, HE])

    def test_get_subject_pool_raises_value_error(self):
        self.assertRaises(ValueError, self.rp.get_subject_pool, 16)

    def test_create_pool_paragraph_is_correct_length(self):
        verb_list = [{'verb': Verb('play'), 'preposition': None, 'objects': 0, 'particle': None}]
        rp = RandomParagraph(0.2, verb_list, self.countable + self.uncountable)

        for length in range(3, 11):
            pool = length - 2
            answer = rp.create_pool_paragraph(pool, length)
            self.assertEqual(len(answer), length)

    def test_create_pool_paragraph_subjects_in_subject_pool_and_not_in_predicate(self):
        random.seed(20)
        paragraph = self.rp.create_pool_paragraph(pool_size=3, num_sentences=20)

        subjects = [Noun('pig'), Noun('cat'), SHE]
        for sentence in paragraph:
            subject = sentence.get(0)
            predicate = sentence.word_list()[1:]
            self.assertIn(subject, subjects)
            self.assertNotIn(subject, predicate)

    def test_create_pool_paragraph_repeats_very_very_edge_case(self):
        random.seed(25)
        verb_list = [{'verb': Verb('give'), 'preposition': None, 'objects': 2, 'particle': None}]

        repeats = RandomParagraph(0.0, verb_list, [Noun('cat'), Noun('water')])

        answer = repeats.create_pool_paragraph(2, 2)
        expected = [
            Sentence([Noun('water'), Verb('give'), Noun('cat'), Noun('water'), PERIOD]),
            Sentence([Noun('cat'), Verb('give'), Noun('cat'), Noun('water'), PERIOD])
        ]
        self.assertEqual(answer, expected)

        no_prepositions = [verb_dict for verb_dict in self.verbs if verb_dict['preposition'] is None]
        no_repeats = RandomParagraph(0.0, no_prepositions, [Noun('cat'), Noun('water')])
        answer = no_repeats.create_pool_paragraph(2, 100)
        for sentence in answer:
            self.assertEqual(len(sentence), 4)
            self.assertNotEqual(sentence.get(0), sentence.get(2))

    def test_create_pool_paragraph_output(self):
        random.seed(3)
        paragraph = self.rp.create_pool_paragraph(2, 5)
        expected = [
            Sentence([Noun('pig'), Verb('eat'), Noun('sand'), PERIOD]),
            Sentence([Noun('pig'), Verb('give'), Noun('milk'), Noun('cat'), PERIOD]),
            Sentence([Noun('pig'), Verb('jump'), BasicWord.preposition('over'), Noun('water'), PERIOD]),
            Sentence([Noun('sand'), Verb('eat'), IT, PERIOD]),
            Sentence([Noun('sand'), Verb('give'), Noun('water'), BasicWord.preposition('to'), Noun('milk'),
                      EXCLAMATION])
        ]
        self.assertEqual(paragraph, expected)

    def test_create_chain_paragraph_is_correct_length(self):
        for length in range(3, 11):
            answer = self.rp.create_chain_paragraph(length)
            self.assertEqual(len(answer), length)

    def test_create_chain_paragraph_loop_safety_finally_returns_paragraph_with_repeat_words(self):
        random.seed(4564)
        verb_list = [{'verb': Verb('give'), 'preposition': None, 'objects': 2, 'particle': None}]

        repeats = RandomParagraph(0.0, verb_list, [Noun('joe'), Noun('bob')])
        paragraph = repeats.create_chain_paragraph(3)
        expected = [
            Sentence([Noun('bob'), Verb('give'), Noun('joe'), Noun('bob'), PERIOD]),
            Sentence([Noun('bob'), Verb('give'), Noun('bob'), Noun('joe'), PERIOD]),
            Sentence([Noun('joe'), Verb('give'), Noun('bob'), Noun('joe'), PERIOD]),
        ]
        self.assertEqual(expected, paragraph)

    def test_create_chain_paragraph_pronouns(self):
        verb_list = [{'verb': Verb('eat'), 'preposition': None, 'objects': 1, 'particle': None}]

        rp = RandomParagraph(1.0, verb_list, self.countable + self.uncountable)
        answer = rp.create_chain_paragraph(10)
        for back_index, sentence in enumerate(answer[1:]):
            previous_obj = answer[back_index].get(-2)
            current_subj = sentence.get(0)
            self.assertEqual(previous_obj.subject(), current_subj)

    def test_create_chain_paragraph_nouns(self):
        rp = RandomParagraph(0.0, self.verbs, self.countable + self.uncountable)
        answer = rp.create_chain_paragraph(10)
        for back_index, sentence in enumerate(answer[1:]):
            previous_obj = answer[back_index].get(-2)
            current_subj = sentence.get(0)
            self.assertEqual(previous_obj, current_subj)

    def test_create_chain_paragraph_assigns_random_subj_if_no_obj(self):
        random.seed(11)
        verb_list = [{'verb': Verb('jump'), 'preposition': None, 'objects': 0, 'particle': None}]
        rp = RandomParagraph(0.2, verb_list, self.countable + self.uncountable)
        answer = rp.create_chain_paragraph(3)
        expected = [
            Sentence([Noun('sand'), Verb('jump'), EXCLAMATION]),
            Sentence([Noun('frog'), Verb('jump'), EXCLAMATION]),
            Sentence([Noun('pig'), Verb('jump'), PERIOD])
        ]
        self.assertEqual(expected, answer)

    def test_create_chain_paragraph_output(self):
        random.seed(4567)
        answer = self.rp.create_chain_paragraph(4)
        expected = [
            Sentence([Noun('water'), Verb('eat'), Noun('rice'), EXCLAMATION]),
            Sentence([Noun('rice'), Verb('give'), US, BasicWord.preposition('to'), Noun('cat'), PERIOD]),
            Sentence([Noun('cat'), Verb('eat'), Noun('dog'), PERIOD]),
            Sentence([Noun('dog'), Verb('jump'), BasicWord.preposition('over'), Noun('sand'), PERIOD]),
        ]
        self.assertEqual(answer, expected)
