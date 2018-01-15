import random
import unittest

from sentences.backend.random_sentences import RandomSentences
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb
from sentences.words.word import Preposition

period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun


class TestRawWordsRandomisation(unittest.TestCase):
    def setUp(self):
        self.countable = [Noun('dog'), Noun('cat'), Noun('pig'), Noun('frog')]
        self.uncountable = [Noun('water'), Noun('rice'), Noun('milk'), Noun('sand')]
        self.verbs = [
            {'verb': Verb('eat'), 'preposition': None, 'objects': 1, 'insert_preposition': False},
            {'verb': Verb('give'), 'preposition': None, 'objects': 2, 'insert_preposition': False},
            {'verb': Verb('jump'), 'preposition': Preposition('over'), 'objects': 1, 'insert_preposition': False},
            {'verb': Verb('give'), 'preposition': Preposition('to'), 'objects': 2, 'insert_preposition': True},
        ]
        self.generator = RandomSentences(self.verbs, self.countable, self.uncountable)

    def test_raises_error_if_no_verbs(self):
        self.assertRaises(ValueError, RandomSentences, [], [Noun('dog')], [Noun('cat')])

    def test_raises_error_if_no_nouns_in_both_countable_and_uncountable(self):
        self.assertRaises(ValueError, RandomSentences, [Verb('go')], [], [])
        self.assertIsInstance(RandomSentences([Verb('go')], [Noun('dog')], []), RandomSentences)
        self.assertIsInstance(RandomSentences([Verb('go')], [], [Noun('dog')]), RandomSentences)

    def test_makes_copy_of_input_list(self):
        random.seed(148)
        for index in range(4):
            self.countable[index] = 'oops'
            self.uncountable[index] = 'oops'
            self.verbs[index] = 'oops'
        answer = self.generator.sentence()
        self.assertEqual(answer,
                         [Noun('dog'), Verb('give'), Noun('water'), Preposition('to'), Noun('frog'), period])

    def test_subject_p_pronoun_zero(self):
        random.seed(10)

        answer = self.generator.subject(0)
        self.assertEqual(answer, Noun('milk'))

        answer = self.generator.subject(-1)
        self.assertEqual(answer, Noun('dog'))

        answer = self.generator.subject(-10)
        self.assertEqual(answer, Noun('sand'))

    def test_subject_p_pronoun_one(self):
        random.seed(10)

        answer = self.generator.subject(1)
        self.assertEqual(answer, she)

        answer = self.generator.subject(10)
        self.assertEqual(answer, i)

        answer = self.generator.subject(100)
        self.assertEqual(answer, it)

    def test_subject_p_pronoun_point_five(self):
        random.seed(10)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, Noun('milk'))

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, i)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, it)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, Noun('pig'))

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, it)

    def test_object_p_pronoun_zero(self):
        random.seed(10)

        answer = self.generator.object(0)
        self.assertEqual(answer, Noun('milk'))

        answer = self.generator.object(-1)
        self.assertEqual(answer, Noun('dog'))

        answer = self.generator.object(-10)
        self.assertEqual(answer, Noun('sand'))

    def test_object_p_pronoun_one(self):
        random.seed(10)

        answer = self.generator.object(1)
        self.assertEqual(answer, her)

        answer = self.generator.object(10)
        self.assertEqual(answer, me)

        answer = self.generator.object(100)
        self.assertEqual(answer, it)

    def test_object_p_pronoun_point_five(self):
        random.seed(10)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, Noun('milk'))

        answer = self.generator.object(0.5)
        self.assertEqual(answer, me)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, it)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, Noun('pig'))

        answer = self.generator.object(0.5)
        self.assertEqual(answer, it)

    def test_predicate(self):
        random.seed(5)
        answer = self.generator.predicate()
        self.assertEqual(answer, [Verb('jump'), Preposition('over'), Noun('dog'), period])

        answer = self.generator.predicate()
        self.assertEqual(answer, [Verb('give'), Noun('pig'), Noun('sand'), period])

        answer = self.generator.predicate()
        self.assertEqual(answer, [Verb('give'), Noun('frog'), Preposition('to'), Noun('pig'), period])

    def test_sentence(self):
        random.seed(1)
        answer = self.generator.sentence()
        self.assertEqual(answer, [i, Verb('jump'), Preposition('over'), it, period])

        answer = self.generator.sentence()
        self.assertEqual(answer, [Noun('frog'), Verb('eat'), Noun('milk'), period])

        answer = self.generator.sentence()
        self.assertEqual(answer, [Noun('dog'), Verb('give'), Noun('frog'), Preposition('to'), Noun('cat'), period])

    def test_assign_preposition(self):
        random.seed(1234)
        verb_list = [{'verb': Verb('jump'), 'preposition': Preposition('on'),
                      'objects': 1, 'insert_preposition': False}]
        generator = RandomSentences(verb_list, self.countable, self.uncountable)
        answer = generator.sentence()
        self.assertEqual(answer, [Noun('sand'), Verb('jump'), Preposition('on'), us, period])

        answer = generator.sentence()
        self.assertEqual(answer, [Noun('cat'), Verb('jump'), Preposition('on'), Noun('frog'), period])

    def test_assign_preposition_insert_preposition_true(self):
        random.seed(7890)
        verb_list = [{'verb': Verb('bring'), 'preposition': Preposition('to'),
                      'objects': 2, 'insert_preposition': True}]
        generator = RandomSentences(verb_list, self.countable, self.uncountable)
        answer = generator.sentence()
        self.assertEqual(answer, [Noun('milk'), Verb('bring'), Noun('water'), Preposition('to'),
                                  Noun('rice'), exclamation])

        answer = generator.sentence()
        self.assertEqual(answer, [Noun('water'), Verb('bring'), Noun('dog'),
                                  Preposition('to'), Noun('milk'), period])

    def test_two_objects_second_obj_is_never_pronoun(self):
        random.seed(456)
        verb_list = [
            {'verb': Verb('bring'), 'preposition': Preposition('to'), 'objects': 2, 'insert_preposition': True},
            {'verb': Verb('give'), 'preposition': None, 'objects': 2, 'insert_preposition': False},
        ]
        generator = RandomSentences(verb_list, self.countable, self.uncountable)
        answer = generator.predicate(1.0)
        self.assertEqual(answer, [Verb('give'), her, Noun('dog'), exclamation])

        answer = generator.predicate(1.0)
        self.assertEqual(answer, [Verb('bring'), me, Preposition('to'), Noun('sand'), period])

        answer = generator.predicate(1.0)
        self.assertEqual(answer, [Verb('give'), him, Noun('milk'), exclamation])

    def test_two_objects_are_never_the_same(self):
        verb_list = [
            {'verb': Verb('give'), 'preposition': None, 'objects': 2, 'insert_preposition': False},
        ]
        generator = RandomSentences(verb_list, [Noun('dog')], [Noun('water')])

        test_membership = (Noun('dog'), Noun('water'))
        for _ in range(100):
            predicate = generator.predicate(0.0)
            noun_1 = predicate[-2]
            noun_2 = predicate[-3]
            self.assertNotEqual(noun_1, noun_2)
            self.assertIn(noun_1, test_membership)
            self.assertIn(noun_2, test_membership)

    def test_two_objects_the_same_when_no_other_options(self):
        random.seed(101)
        verb_list = [
            {'verb': Verb('give'), 'preposition': None, 'objects': 2, 'insert_preposition': False},
        ]
        generator = RandomSentences(verb_list, [Noun('dog')], [])
        self.assertEqual(generator.predicate(), [Verb('give'), Noun('dog'), Noun('dog'), period])
