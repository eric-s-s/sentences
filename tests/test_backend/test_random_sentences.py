import random
import unittest

from sentences.backend.random_sentences import RandomSentences, assign_objects
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.new_word import NewNoun
from sentences.words.new_verb import NewVerb
from sentences.words.basicword import BasicWord

period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun.__members__.values()


class TestRawWordsRandomisation(unittest.TestCase):
    def setUp(self):
        self.countable = [NewNoun('dog'), NewNoun('cat'), NewNoun('pig'), NewNoun('frog')]
        self.uncountable = [NewNoun('water'), NewNoun('rice'), NewNoun('milk'), NewNoun('sand')]
        self.verbs = [
            {'verb': NewVerb('eat'), 'preposition': None, 'objects': 1, 'particle': None},
            {'verb': NewVerb('give'), 'preposition': None, 'objects': 2, 'particle': None},
            {'verb': NewVerb('jump'), 'preposition': BasicWord.preposition('over'), 'objects': 1, 'particle': None},
            {'verb': NewVerb('give'), 'preposition': BasicWord.preposition('to'), 'objects': 2, 'particle': None},
        ]
        self.generator = RandomSentences(self.verbs, self.countable + self.uncountable)

    def test_raises_error_if_no_verbs(self):
        self.assertRaises(ValueError, RandomSentences, [], [NewNoun('dog'), NewNoun('cat')])

    def test_raises_error_if_no_nouns(self):
        self.assertRaises(ValueError, RandomSentences, [NewVerb('go')], [])
        self.assertIsInstance(RandomSentences([NewVerb('go')], [NewNoun('dog')]), RandomSentences)
        self.assertIsInstance(RandomSentences([NewVerb('go')], [NewNoun('dog')]), RandomSentences)

    def test_makes_copy_of_input_list(self):
        random.seed(148)
        for index in range(4):
            self.countable[index] = 'oops'
            self.uncountable[index] = 'oops'
            self.verbs[index] = 'oops'
        answer = self.generator.sentence()
        expected = [NewNoun('dog'), NewVerb('give'), NewNoun('water'), BasicWord.preposition('to'),
                    NewNoun('frog'), period]
        self.assertEqual(answer, expected)

    def test_subject_p_pronoun_zero(self):
        random.seed(10)

        answer = self.generator.subject(0)
        self.assertEqual(answer, NewNoun('milk'))

        answer = self.generator.subject(-1)
        self.assertEqual(answer, NewNoun('dog'))

        answer = self.generator.subject(-10)
        self.assertEqual(answer, NewNoun('sand'))

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
        self.assertEqual(answer, NewNoun('milk'))

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, i)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, it)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, NewNoun('pig'))

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, it)

    def test_object_p_pronoun_zero(self):
        random.seed(10)

        answer = self.generator.object(0)
        self.assertEqual(answer, NewNoun('milk'))

        answer = self.generator.object(-1)
        self.assertEqual(answer, NewNoun('dog'))

        answer = self.generator.object(-10)
        self.assertEqual(answer, NewNoun('sand'))

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
        self.assertEqual(answer, NewNoun('milk'))

        answer = self.generator.object(0.5)
        self.assertEqual(answer, me)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, it)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, NewNoun('pig'))

        answer = self.generator.object(0.5)
        self.assertEqual(answer, it)

    def test_predicate(self):
        random.seed(5)
        answer = self.generator.predicate()
        self.assertEqual(answer, [NewVerb('jump'), BasicWord.preposition('over'), NewNoun('dog'), period])

        answer = self.generator.predicate()
        self.assertEqual(answer, [NewVerb('give'), NewNoun('pig'), NewNoun('sand'), period])

        answer = self.generator.predicate()
        expected = [NewVerb('give'), NewNoun('frog'), BasicWord.preposition('to'), NewNoun('pig'), period]
        self.assertEqual(answer, expected)

    def test_sentence(self):
        random.seed(1)
        answer = self.generator.sentence()
        self.assertEqual(answer, [i, NewVerb('jump'), BasicWord.preposition('over'), it, period])

        answer = self.generator.sentence()
        self.assertEqual(answer, [NewNoun('frog'), NewVerb('eat'), NewNoun('milk'), period])

        answer = self.generator.sentence()
        expected = [NewNoun('dog'), NewVerb('give'), NewNoun('frog'), BasicWord.preposition('to'),
                    NewNoun('cat'), period]
        self.assertEqual(answer, expected)

    def test_assign_preposition(self):
        random.seed(1234)
        verb_list = [{'verb': NewVerb('jump'), 'preposition': BasicWord.preposition('on'),
                      'objects': 1, 'particle': None}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        self.assertEqual(answer, [NewNoun('sand'), NewVerb('jump'), BasicWord.preposition('on'), us, period])

        answer = generator.sentence()
        expected = [NewNoun('cat'), NewVerb('jump'), BasicWord.preposition('on'), NewNoun('frog'), period]
        self.assertEqual(answer, expected)

    def test_assign_preposition_insert_preposition_true(self):
        random.seed(7890)
        verb_list = [{'verb': NewVerb('bring'), 'preposition': BasicWord.preposition('to'),
                      'objects': 2, 'particle': None}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        self.assertEqual(answer, [NewNoun('milk'), NewVerb('bring'), NewNoun('water'), BasicWord.preposition('to'),
                                  NewNoun('rice'), exclamation])

        answer = generator.sentence()
        self.assertEqual(answer, [NewNoun('water'), NewVerb('bring'), NewNoun('dog'),
                                  BasicWord.preposition('to'), NewNoun('milk'), period])

    def test_two_objects_second_obj_is_never_pronoun(self):
        random.seed(456)
        verb_list = [
            {'verb': NewVerb('bring'), 'preposition': BasicWord.preposition('to'), 'objects': 2, 'particle': None},
            {'verb': NewVerb('give'), 'preposition': None, 'objects': 2, 'particle': None},
        ]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.predicate(1.0)
        self.assertEqual(answer, [NewVerb('give'), her, NewNoun('dog'), exclamation])

        answer = generator.predicate(1.0)
        self.assertEqual(answer, [NewVerb('bring'), me, BasicWord.preposition('to'), NewNoun('sand'), period])

        answer = generator.predicate(1.0)
        self.assertEqual(answer, [NewVerb('give'), him, NewNoun('milk'), exclamation])

    def test_two_objects_are_never_the_same(self):
        verb_list = [
            {'verb': NewVerb('give'), 'preposition': None, 'objects': 2, 'particle': None},
        ]
        generator = RandomSentences(verb_list, [NewNoun('dog'), NewNoun('water')])

        test_membership = (NewNoun('dog'), NewNoun('water'))
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
            {'verb': NewVerb('give'), 'preposition': None, 'objects': 2, 'particle': None},
        ]
        generator = RandomSentences(verb_list, [NewNoun('dog')])
        self.assertEqual(generator.predicate(), [NewVerb('give'), NewNoun('dog'), NewNoun('dog'), period])

    def test_assign_objects_no_objects_no_particle_no_preposition(self):
        verb_dict = {'verb': NewVerb('chill'), 'preposition': None, 'objects': 0, 'particle': None}
        self.assertEqual(assign_objects(verb_dict, []), [NewVerb('chill')])

    def test_assign_objects_no_objects_particle_or_preposition(self):
        verb_dict = {'verb': NewVerb('chill'),
                     'preposition': BasicWord.preposition('out'),
                     'objects': 0,
                     'particle': None}
        self.assertEqual(assign_objects(verb_dict, []), [NewVerb('chill'), BasicWord.preposition('out')])

        verb_dict = {'verb': NewVerb('run'), 'preposition': None, 'objects': 0, 'particle': BasicWord.particle('away')}
        self.assertEqual(assign_objects(verb_dict, []), [NewVerb('run'), BasicWord.particle('away')])

    def test_assign_objects_one_object_no_particle_no_preposition(self):
        verb_dict = {'verb': NewVerb('like'), 'preposition': None, 'objects': 1, 'particle': None}
        self.assertEqual(assign_objects(verb_dict, [NewNoun('dog')]), [NewVerb('like'), NewNoun('dog')])

    def test_assign_objects_one_object_particle(self):
        verb_dict = {'verb': NewVerb('pick'),
                     'preposition': None,
                     'objects': 1,
                     'particle': BasicWord.particle('up')}
        self.assertEqual(assign_objects(verb_dict, [Pronoun.IT]),
                         [NewVerb('pick'), Pronoun.IT, BasicWord.particle('up')])

        self.assertEqual(assign_objects(verb_dict, [NewNoun('dog')]),
                         [NewVerb('pick'), BasicWord.particle('up'), NewNoun('dog')])

    def test_assign_objects_one_object_preposition(self):
        verb_dict = {'verb': NewVerb('play'),
                     'preposition': BasicWord.preposition('with'),
                     'objects': 1,
                     'particle': None}
        self.assertEqual(assign_objects(verb_dict, [Pronoun.IT]),
                         [NewVerb('play'), BasicWord.preposition('with'), Pronoun.IT])

        self.assertEqual(assign_objects(verb_dict, [NewNoun('dog')]),
                         [NewVerb('play'), BasicWord.preposition('with'), NewNoun('dog')])

    def test_assign_objects_one_object_particle_and_preposition(self):
        verb_dict = {'verb': NewVerb('put'), 'preposition': BasicWord.preposition('with'),
                     'objects': 1, 'particle': BasicWord.particle('up')}
        self.assertEqual(assign_objects(verb_dict, [Pronoun.IT]),
                         [NewVerb('put'), BasicWord.particle('up'), BasicWord.preposition('with'), Pronoun.IT])
        self.assertEqual(assign_objects(verb_dict, [NewNoun('dog')]),
                         [NewVerb('put'), BasicWord.particle('up'), BasicWord.preposition('with'), NewNoun('dog')])

    def test_assign_objects_two_objects_no_particle_no_preposition(self):
        verb_dict = {'verb': NewVerb('show'), 'preposition': None, 'objects': 2, 'particle': None}
        self.assertEqual(assign_objects(verb_dict, [NewNoun('dog'), NewNoun('cat')]),
                         [NewVerb('show'), NewNoun('dog'), NewNoun('cat')])

    def test_assign_objects_two_objects_preposition(self):
        verb_dict = {'verb': NewVerb('bring'),
                     'preposition': BasicWord.preposition('to'),
                     'objects': 2,
                     'particle': None}
        self.assertEqual(assign_objects(verb_dict, [Pronoun.HIM, Pronoun.IT]),
                         [NewVerb('bring'), Pronoun.HIM, BasicWord.preposition('to'), Pronoun.IT])

        self.assertEqual(assign_objects(verb_dict, [NewNoun('cat'), NewNoun('dog')]),
                         [NewVerb('bring'), NewNoun('cat'), BasicWord.preposition('to'), NewNoun('dog')])

    def test_assign_objects_two_objects_particle_and_preposition(self):
        verb_dict = {'verb': NewVerb('throw'), 'preposition': BasicWord.preposition('for'),
                     'objects': 2, 'particle': BasicWord.particle('away')}
        self.assertEqual(
            assign_objects(verb_dict, [Pronoun.HIM, Pronoun.IT]),
            [NewVerb('throw'), Pronoun.HIM, BasicWord.particle('away'), BasicWord.preposition('for'), Pronoun.IT]
        )
        self.assertEqual(
            assign_objects(verb_dict, [NewNoun('cat'), NewNoun('dog')]),
            [NewVerb('throw'), BasicWord.particle('away'), NewNoun('cat'),
             BasicWord.preposition('for'), NewNoun('dog')]
        )

    def test_random_sentences_sentence_with_phrasal_verb_no_preposition(self):
        random.seed(1234)
        verb_list = [{'verb': NewVerb('pick'), 'preposition': None, 'objects': 1, 'particle': BasicWord.particle('up')}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        self.assertEqual(answer, [NewNoun('sand'), NewVerb('pick'), us, BasicWord.particle('up'), period])

        answer = generator.sentence()
        self.assertEqual(answer, [NewNoun('cat'), NewVerb('pick'), BasicWord.particle('up'), NewNoun('frog'), period])

    def test_random_sentences_sentence_with_phrasal_verb_one_obj_and_preposition(self):
        random.seed(456123)
        verb_list = [{'verb': NewVerb('put'), 'preposition': BasicWord.preposition('with'),
                     'objects': 1, 'particle': BasicWord.particle('up')}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        expected = [NewNoun('pig'), NewVerb('put'), BasicWord.particle('up'), BasicWord.preposition('with'),
                    you, period]
        self.assertEqual(answer, expected)

        answer = generator.sentence()
        expected = [NewNoun('water'), NewVerb('put'), BasicWord.particle('up'), BasicWord.preposition('with'),
                    NewNoun('pig'), exclamation]
        self.assertEqual(answer, expected)

    def test_random_sentences_sentence_with_phrasal_verb_two_obj_and_preposition(self):
        random.seed(789)
        verb_list = [{'verb': NewVerb('throw'), 'preposition': BasicWord.preposition('for'),
                     'objects': 2, 'particle': BasicWord.particle('away')}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        expected = [NewNoun('dog'), NewVerb('throw'), us, BasicWord.particle('away'), BasicWord.preposition('for'),
                    NewNoun('water'), exclamation]
        self.assertEqual(answer, expected)

        answer = generator.sentence()
        self.assertEqual(answer, [NewNoun('rice'), NewVerb('throw'), BasicWord.particle('away'), NewNoun('water'),
                                  BasicWord.preposition('for'), NewNoun('frog'), period])
