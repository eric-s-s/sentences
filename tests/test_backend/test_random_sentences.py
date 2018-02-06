import random
import unittest

from sentences.backend.random_sentences import RandomSentences, assign_objects
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.noun import Noun
from sentences.words.verb import Verb
from sentences.words.basicword import BasicWord

PERIOD = Punctuation.PERIOD
EXCLAMATION = Punctuation.EXCLAMATION

I, ME, YOU, HE, HIM, SHE, HER, IT, WE, US, THEY, THEM = Pronoun.__members__.values()


class TestRawWordsRandomisation(unittest.TestCase):
    def setUp(self):
        self.countable = [Noun('dog'), Noun('cat'), Noun('pig'), Noun('frog')]
        self.uncountable = [Noun('water'), Noun('rice'), Noun('milk'), Noun('sand')]
        self.verbs = [
            {'verb': Verb('eat'), 'preposition': None, 'objects': 1, 'particle': None},
            {'verb': Verb('give'), 'preposition': None, 'objects': 2, 'particle': None},
            {'verb': Verb('jump'), 'preposition': BasicWord.preposition('over'), 'objects': 1, 'particle': None},
            {'verb': Verb('give'), 'preposition': BasicWord.preposition('to'), 'objects': 2, 'particle': None},
        ]
        self.generator = RandomSentences(self.verbs, self.countable + self.uncountable)

    def test_raises_error_if_no_verbs(self):
        self.assertRaises(ValueError, RandomSentences, [], [Noun('dog'), Noun('cat')])

    def test_raises_error_if_no_nouns(self):
        self.assertRaises(ValueError, RandomSentences, [Verb('go')], [])
        self.assertIsInstance(RandomSentences([Verb('go')], [Noun('dog')]), RandomSentences)
        self.assertIsInstance(RandomSentences([Verb('go')], [Noun('dog')]), RandomSentences)

    def test_makes_copy_of_input_list(self):
        random.seed(148)
        for index in range(4):
            self.countable[index] = 'oops'
            self.uncountable[index] = 'oops'
            self.verbs[index] = 'oops'
        answer = self.generator.sentence()
        expected = [Noun('dog'), Verb('give'), Noun('water'), BasicWord.preposition('to'),
                    Noun('frog'), PERIOD]
        self.assertEqual(answer, expected)

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
        self.assertEqual(answer, SHE)

        answer = self.generator.subject(10)
        self.assertEqual(answer, I)

        answer = self.generator.subject(100)
        self.assertEqual(answer, IT)

    def test_subject_p_pronoun_point_five(self):
        random.seed(10)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, Noun('milk'))

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, I)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, IT)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, Noun('pig'))

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, IT)

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
        self.assertEqual(answer, HER)

        answer = self.generator.object(10)
        self.assertEqual(answer, ME)

        answer = self.generator.object(100)
        self.assertEqual(answer, IT)

    def test_object_p_pronoun_point_five(self):
        random.seed(10)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, Noun('milk'))

        answer = self.generator.object(0.5)
        self.assertEqual(answer, ME)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, IT)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, Noun('pig'))

        answer = self.generator.object(0.5)
        self.assertEqual(answer, IT)

    def test_predicate(self):
        random.seed(5)
        answer = self.generator.predicate()
        self.assertEqual(answer, [Verb('jump'), BasicWord.preposition('over'), Noun('dog'), PERIOD])

        answer = self.generator.predicate()
        self.assertEqual(answer, [Verb('give'), Noun('pig'), Noun('sand'), PERIOD])

        answer = self.generator.predicate()
        expected = [Verb('give'), Noun('frog'), BasicWord.preposition('to'), Noun('pig'), PERIOD]
        self.assertEqual(answer, expected)

    def test_sentence(self):
        random.seed(1)
        answer = self.generator.sentence()
        self.assertEqual(answer, [I, Verb('jump'), BasicWord.preposition('over'), IT, PERIOD])

        answer = self.generator.sentence()
        self.assertEqual(answer, [Noun('frog'), Verb('eat'), Noun('milk'), PERIOD])

        answer = self.generator.sentence()
        expected = [Noun('dog'), Verb('give'), Noun('frog'), BasicWord.preposition('to'),
                    Noun('cat'), PERIOD]
        self.assertEqual(answer, expected)

    def test_assign_preposition(self):
        random.seed(1234)
        verb_list = [{'verb': Verb('jump'),
                      'preposition': BasicWord.preposition('on'),
                      'objects': 1,
                      'particle': None}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        self.assertEqual(answer,
                         [Noun('sand'), Verb('jump'), BasicWord.preposition('on'), US, PERIOD])

        answer = generator.sentence()
        expected = [Noun('cat'), Verb('jump'), BasicWord.preposition('on'), Noun('frog'), PERIOD]
        self.assertEqual(answer, expected)

    def test_assign_preposition_insert_preposition_true(self):
        random.seed(7890)
        verb_list = [{'verb': Verb('bring'),
                      'preposition': BasicWord.preposition('to'),
                      'objects': 2,
                      'particle': None}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        self.assertEqual(answer, [Noun('milk'), Verb('bring'), Noun('water'), BasicWord.preposition('to'),
                                  Noun('rice'), EXCLAMATION])

        answer = generator.sentence()
        self.assertEqual(answer, [Noun('water'), Verb('bring'), Noun('dog'),
                                  BasicWord.preposition('to'), Noun('milk'), PERIOD])

    def test_two_objects_second_obj_is_never_pronoun(self):
        random.seed(456)
        verb_list = [
            {'verb': Verb('bring'), 'preposition': BasicWord.preposition('to'), 'objects': 2, 'particle': None},
            {'verb': Verb('give'), 'preposition': None, 'objects': 2, 'particle': None},
        ]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.predicate(1.0)
        self.assertEqual(answer, [Verb('give'), HER, Noun('dog'), EXCLAMATION])

        answer = generator.predicate(1.0)
        self.assertEqual(answer, [Verb('bring'), ME, BasicWord.preposition('to'), Noun('sand'), PERIOD])

        answer = generator.predicate(1.0)
        self.assertEqual(answer, [Verb('give'), HIM, Noun('milk'), EXCLAMATION])

    def test_two_objects_are_never_the_same(self):
        verb_list = [
            {'verb': Verb('give'), 'preposition': None, 'objects': 2, 'particle': None},
        ]
        generator = RandomSentences(verb_list, [Noun('dog'), Noun('water')])

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
        verb_list = [{'verb': Verb('give'),
                      'preposition': None,
                      'objects': 2,
                      'particle': None}]
        generator = RandomSentences(verb_list, [Noun('dog')])
        self.assertEqual(generator.predicate(),
                         [Verb('give'), Noun('dog'), Noun('dog'), PERIOD])

    def test_assign_objects_no_objects_no_particle_no_preposition(self):
        verb_dict = {'verb': Verb('chill'),
                     'preposition': None,
                     'objects': 0,
                     'particle': None}
        self.assertEqual(assign_objects(verb_dict, []),
                         [Verb('chill')])

    def test_assign_objects_no_objects_particle_or_preposition(self):
        verb_dict = {'verb': Verb('chill'),
                     'preposition': BasicWord.preposition('out'),
                     'objects': 0,
                     'particle': None}
        self.assertEqual(assign_objects(verb_dict, []),
                         [Verb('chill'), BasicWord.preposition('out')])

        verb_dict = {'verb': Verb('run'),
                     'preposition': None,
                     'objects': 0,
                     'particle': BasicWord.particle('away')}
        self.assertEqual(assign_objects(verb_dict, []),
                         [Verb('run'), BasicWord.particle('away')])

    def test_assign_objects_one_object_no_particle_no_preposition(self):
        verb_dict = {'verb': Verb('like'),
                     'preposition': None,
                     'objects': 1,
                     'particle': None}
        self.assertEqual(assign_objects(verb_dict, [Noun('dog')]),
                         [Verb('like'), Noun('dog')])

    def test_assign_objects_one_object_particle(self):
        verb_dict = {'verb': Verb('pick'),
                     'preposition': None,
                     'objects': 1,
                     'particle': BasicWord.particle('up')}
        self.assertEqual(assign_objects(verb_dict, [IT]),
                         [Verb('pick'), IT, BasicWord.particle('up')])

        self.assertEqual(assign_objects(verb_dict, [Noun('dog')]),
                         [Verb('pick'), BasicWord.particle('up'), Noun('dog')])

    def test_assign_objects_one_object_preposition(self):
        verb_dict = {'verb': Verb('play'),
                     'preposition': BasicWord.preposition('with'),
                     'objects': 1,
                     'particle': None}
        self.assertEqual(assign_objects(verb_dict, [IT]),
                         [Verb('play'), BasicWord.preposition('with'), IT])

        self.assertEqual(assign_objects(verb_dict, [Noun('dog')]),
                         [Verb('play'), BasicWord.preposition('with'), Noun('dog')])

    def test_assign_objects_one_object_particle_and_preposition(self):
        verb_dict = {'verb': Verb('put'),
                     'preposition': BasicWord.preposition('with'),
                     'objects': 1,
                     'particle': BasicWord.particle('up')}
        self.assertEqual(assign_objects(verb_dict, [IT]),
                         [Verb('put'), BasicWord.particle('up'), BasicWord.preposition('with'), IT])
        self.assertEqual(assign_objects(verb_dict, [Noun('dog')]),
                         [Verb('put'), BasicWord.particle('up'), BasicWord.preposition('with'), Noun('dog')])

    def test_assign_objects_two_objects_no_particle_no_preposition(self):
        verb_dict = {'verb': Verb('show'), 'preposition': None, 'objects': 2, 'particle': None}
        self.assertEqual(assign_objects(verb_dict, [Noun('dog'), Noun('cat')]),
                         [Verb('show'), Noun('dog'), Noun('cat')])

    def test_assign_objects_two_objects_preposition(self):
        verb_dict = {'verb': Verb('bring'),
                     'preposition': BasicWord.preposition('to'),
                     'objects': 2,
                     'particle': None}
        self.assertEqual(assign_objects(verb_dict, [HIM, IT]),
                         [Verb('bring'), HIM, BasicWord.preposition('to'), IT])

        self.assertEqual(assign_objects(verb_dict, [Noun('cat'), Noun('dog')]),
                         [Verb('bring'), Noun('cat'), BasicWord.preposition('to'), Noun('dog')])

    def test_assign_objects_two_objects_particle_and_preposition(self):
        verb_dict = {'verb': Verb('throw'),
                     'preposition': BasicWord.preposition('for'),
                     'objects': 2,
                     'particle': BasicWord.particle('away')}
        self.assertEqual(
            assign_objects(verb_dict, [HIM, IT]),
            [Verb('throw'), HIM, BasicWord.particle('away'), BasicWord.preposition('for'), IT]
        )
        self.assertEqual(
            assign_objects(verb_dict, [Noun('cat'), Noun('dog')]),
            [Verb('throw'), BasicWord.particle('away'), Noun('cat'), BasicWord.preposition('for'), Noun('dog')]
        )

    def test_random_sentences_sentence_with_phrasal_verb_no_preposition(self):
        random.seed(1234)
        verb_list = [{'verb': Verb('pick'),
                      'preposition': None,
                      'objects': 1,
                      'particle': BasicWord.particle('up')}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        self.assertEqual(answer, [Noun('sand'), Verb('pick'), US, BasicWord.particle('up'), PERIOD])

        answer = generator.sentence()
        self.assertEqual(answer, [Noun('cat'), Verb('pick'), BasicWord.particle('up'), Noun('frog'), PERIOD])

    def test_random_sentences_sentence_with_phrasal_verb_one_obj_and_preposition(self):
        random.seed(456123)
        verb_list = [{'verb': Verb('put'),
                      'preposition': BasicWord.preposition('with'),
                      'objects': 1,
                      'particle': BasicWord.particle('up')}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        expected = [Noun('pig'), Verb('put'), BasicWord.particle('up'), BasicWord.preposition('with'),
                    YOU, PERIOD]
        self.assertEqual(answer, expected)

        answer = generator.sentence()
        expected = [Noun('water'), Verb('put'), BasicWord.particle('up'), BasicWord.preposition('with'),
                    Noun('pig'), EXCLAMATION]
        self.assertEqual(answer, expected)

    def test_random_sentences_sentence_with_phrasal_verb_two_obj_and_preposition(self):
        random.seed(789)
        verb_list = [{'verb': Verb('throw'),
                      'preposition': BasicWord.preposition('for'),
                      'objects': 2,
                      'particle': BasicWord.particle('away')}]
        generator = RandomSentences(verb_list, self.countable + self.uncountable)
        answer = generator.sentence()
        expected = [Noun('dog'), Verb('throw'), US, BasicWord.particle('away'), BasicWord.preposition('for'),
                    Noun('water'), EXCLAMATION]
        self.assertEqual(answer, expected)

        answer = generator.sentence()
        expected = [Noun('rice'), Verb('throw'), BasicWord.particle('away'), Noun('water'),
                    BasicWord.preposition('for'), Noun('frog'), PERIOD]
        self.assertEqual(answer, expected)
