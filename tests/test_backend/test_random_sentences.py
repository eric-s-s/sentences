import random
import unittest

from sentences.backend.random_sentences import RandomSentences, assign_objects

from sentences.word_groups.sentence import Sentence
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
            {'verb': Verb('lend'), 'preposition': BasicWord.preposition('to'), 'objects': 2, 'particle': None},
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
            self.countable[index] = Noun('oops')
            self.uncountable[index] = Noun('oops')
            self.verbs[index] = {'oops': 1}
        answer = self.generator.predicate()
        expected = [Verb('lend'), Noun('dog'), BasicWord.preposition('to'), Noun('milk'), PERIOD]
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
        expected = [Verb('lend'), Noun('frog'), BasicWord.preposition('to'), Noun('pig'), PERIOD]
        self.assertEqual(answer, expected)

    def test_predicate_p_pronoun_one_or_greater(self):
        verbs = [{'verb': Verb('eat'), 'objects': 1, 'particle': None, 'preposition': None}]
        generator = RandomSentences(verbs, self.countable)

        pronoun = generator.predicate(1.0)[1]
        self.assertIsInstance(pronoun, Pronoun)

        pronoun = generator.predicate(1.1)[1]
        self.assertIsInstance(pronoun, Pronoun)

    def test_predicate_p_pronoun_zero_or_less(self):
        verbs = [{'verb': Verb('eat'), 'objects': 1, 'particle': None, 'preposition': None}]
        generator = RandomSentences(verbs, self.countable)

        noun = generator.predicate(0.0)[1]
        self.assertIsInstance(noun, Noun)

        noun = generator.predicate(-0.1)[1]
        self.assertIsInstance(noun, Noun)

    def test_predicate_p_pronoun_between_zero_and_one(self):
        verbs = [{'verb': Verb('eat'), 'objects': 1, 'particle': None, 'preposition': None}]
        generator = RandomSentences(verbs, self.countable)
        random.seed(347859)
        nouns = [0, 1, 4, 5, 6]
        for iteration in range(10):
            word = generator.predicate(0.5)[1]
            if iteration in nouns:
                self.assertIsInstance(word, Noun)
            else:
                self.assertIsInstance(word, Pronoun)

    def test_predicate_chooses_from_all_verbs(self):
        random.seed(100)
        verbs = [el['verb'] for el in self.verbs]
        self.assertEqual(len(verbs), 4)
        verbs_indices = [1, 0, 3, 1, 3, 0, 1, 1, 1, 2]
        for iteration in range(10):
            verb = self.generator.predicate()[0]
            expected_verb_index = verbs_indices[iteration]
            self.assertEqual(verb, verbs[expected_verb_index])

    def test_predicate_two_objects_second_obj_is_never_pronoun(self):
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

    def test_predicate_two_objects_are_never_the_same(self):
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

    def test_predicate_two_objects_the_same_when_no_other_options(self):
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

    def test_predicate_uses_all_endings(self):
        random.seed(475)
        periods = [1, 2, 3, 5, 6, 8, 9]
        for iteration in range(10):
            punctuation = self.generator.predicate()[-1]

            if iteration in periods:
                self.assertEqual(punctuation, PERIOD)
            else:
                self.assertEqual(punctuation, EXCLAMATION)

    def test_sentence_p_pronoun_gte_one(self):
        verbs = [{'verb': Verb('eat'), 'objects': 1, 'preposition': None, 'particle': None}]
        generator = RandomSentences(verbs, self.countable)
        subject = HE

        obj = generator.sentence(subject, p_pronoun=1.0).get(2)
        self.assertIsInstance(obj, Pronoun)

        obj = generator.sentence(subject, p_pronoun=1.1).get(2)
        self.assertIsInstance(obj, Pronoun)

    def test_sentence_p_pronoun_lte_zero(self):
        verbs = [{'verb': Verb('eat'), 'objects': 1, 'preposition': None, 'particle': None}]
        generator = RandomSentences(verbs, self.countable)
        subject = HE

        obj = generator.sentence(subject, p_pronoun=0.0).get(2)
        self.assertIsInstance(obj, Noun)

        obj = generator.sentence(subject, p_pronoun=-0.1).get(2)
        self.assertIsInstance(obj, Noun)

    def test_sentence_p_pronoun_between_one_and_zero(self):
        random.seed(38754)

        verbs = [{'verb': Verb('eat'), 'objects': 1, 'preposition': None, 'particle': None}]
        generator = RandomSentences(verbs, self.countable)
        subject = HE
        nouns = [2, 3, 6, 9]
        for iteration in range(10):
            obj = generator.sentence(subject, p_pronoun=0.5).get(2)
            if iteration in nouns:
                self.assertIsInstance(obj, Noun)
            else:
                self.assertIsInstance(obj, Pronoun)

    def test_sentence_noun_subject_not_in_predicate(self):
        subject = Noun('cat')
        self.assertIn(subject, self.countable)
        generator = RandomSentences(self.verbs, self.countable)
        for _ in range(20):
            sentence = generator.sentence(subject)
            predicate = sentence.word_list()[1:]
            self.assertNotIn(subject, predicate)

    def test_sentence_pronoun_subject_not_in_predicate(self):
        subject = HE
        for _ in range(20):
            sentence = self.generator.sentence(subject, p_pronoun=1.0)
            predicate = sentence.word_list()[1:]
            self.assertNotIn(subject, predicate)

    def test_sentence_must_repeat_subject(self):
        nouns = [Noun('dog')]
        verbs = [{'verb': Verb('eat'), 'objects': 1, 'preposition': None, 'particle': None}]
        generator = RandomSentences(verbs, nouns)
        subject = Noun('dog')

        sentence = generator.sentence(subject, p_pronoun=0.0)
        possibles = [
            Sentence([Noun('dog'), Verb('eat'), Noun('dog'), PERIOD]),
            Sentence([Noun('dog'), Verb('eat'), Noun('dog'), EXCLAMATION])
        ]
        self.assertIn(sentence, possibles)

    def test_sentence_particle(self):
        random.seed(47)
        nouns = [Noun('dog')]
        verbs = [{'verb': Verb('pick'), 'objects': 1, 'preposition': None, 'particle': BasicWord.particle('up')}]
        generator = RandomSentences(verbs, nouns)
        subj = HE

        sentence = generator.sentence(subj, p_pronoun=1.0)
        expected = Sentence([HE, Verb('pick'), US, BasicWord.particle('up'), PERIOD])
        self.assertEqual(sentence, expected)

        sentence = generator.sentence(subj, p_pronoun=0.0)
        expected = Sentence([HE, Verb('pick'), BasicWord.particle('up'), Noun('dog'), PERIOD])
        self.assertEqual(sentence, expected)

    def test_sentence_particle_preposition(self):
        random.seed(2743)
        nouns = [Noun('dog'), Noun('cat')]
        verbs = [{'verb': Verb('pick'), 'objects': 2, 'preposition': BasicWord.preposition('with'),
                  'particle': BasicWord.particle('up')}]
        generator = RandomSentences(verbs, nouns)
        subj = HE

        sentence = generator.sentence(subj, p_pronoun=1.0)
        expected = Sentence([HE, Verb('pick'), THEM, BasicWord.particle('up'), BasicWord.preposition('with'),
                             Noun('cat'), PERIOD])
        self.assertEqual(sentence, expected)

        sentence = generator.sentence(subj, p_pronoun=0.0)
        expected = Sentence([HE, Verb('pick'), BasicWord.particle('up'), Noun('cat'),
                             BasicWord.preposition('with'), Noun('dog'), EXCLAMATION])
        self.assertEqual(sentence, expected)
