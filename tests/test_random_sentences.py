import random
import unittest
from unittest.mock import patch

from sentences.random_sentences import RandomSentences

from sentences.words.word import Word
from sentences.words.noun import Noun
from sentences.words.verb import BasicVerb
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation

period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun


def two_subject_verbs():
    return [{'verb': BasicVerb('bring', 'brought'), 'preposition': None, 'objects': 2}]


def with_preposition():
    return [{'verb': BasicVerb('jump'), 'preposition': Word('on'), 'objects': 1}]


def three_nouns():
    return [Noun('tom'), Noun('dick'), Noun('harry')]


class TestRawWordsRandomisation(unittest.TestCase):
    def setUp(self):
        self.generator = RandomSentences()

    def test_subject_p_pronoun_zero(self):
        random.seed(10)

        answer = self.generator.subject(0)
        self.assertEqual(answer, Noun('pony', ''))

        answer = self.generator.subject(-1)
        self.assertEqual(answer, Noun('ant', ''))

        answer = self.generator.subject(-10)
        self.assertEqual(answer, Noun('stinky tofu', ''))

        answer = self.generator.subject(-100)
        self.assertEqual(answer, Noun('house', ''))

        answer = self.generator.subject(-1000)
        self.assertEqual(answer, Noun('cow', ''))

    def test_subject_p_pronoun_one(self):
        random.seed(10)

        answer = self.generator.subject(1)
        self.assertEqual(answer, she)

        answer = self.generator.subject(10)
        self.assertEqual(answer, i)

        answer = self.generator.subject(100)
        self.assertEqual(answer, it)

        answer = self.generator.subject(1000)
        self.assertEqual(answer, they)

        answer = self.generator.subject(10000)
        self.assertEqual(answer, i)

    def test_subject_p_pronoun_point_five(self):
        random.seed(10)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, Noun('pony', ''))

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, i)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, it)

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, Noun('gold', ''))

        answer = self.generator.subject(0.5)
        self.assertEqual(answer, Noun('baby', ''))

    def test_object_p_pronoun_zero(self):
        random.seed(10)

        answer = self.generator.object(0)
        self.assertEqual(answer, Noun('pony', ''))

        answer = self.generator.object(-1)
        self.assertEqual(answer, Noun('ant', ''))

        answer = self.generator.object(-10)
        self.assertEqual(answer, Noun('stinky tofu', ''))

        answer = self.generator.object(-100)
        self.assertEqual(answer, Noun('house', ''))

        answer = self.generator.object(-1000)
        self.assertEqual(answer, Noun('cow', ''))

    def test_object_p_pronoun_one(self):
        random.seed(10)

        answer = self.generator.object(1)
        self.assertEqual(answer, her)

        answer = self.generator.object(10)
        self.assertEqual(answer, me)

        answer = self.generator.object(100)
        self.assertEqual(answer, it)

        answer = self.generator.object(1000)
        self.assertEqual(answer, them)

        answer = self.generator.object(10000)
        self.assertEqual(answer, me)

    def test_object_p_pronoun_point_five(self):
        random.seed(10)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, Noun('pony', ''))

        answer = self.generator.object(0.5)
        self.assertEqual(answer, me)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, it)

        answer = self.generator.object(0.5)
        self.assertEqual(answer, Noun('gold', ''))

        answer = self.generator.object(0.5)
        self.assertEqual(answer, Noun('baby', ''))

    def test_predicate(self):
        random.seed(5)
        answer = self.generator.predicate()
        self.assertEqual(answer, [BasicVerb('pull', ''), Noun('octopus', ''), exclamation])

        answer = self.generator.predicate()
        self.assertEqual(answer, [BasicVerb('use'), Noun('tiger', ''), period])

        answer = self.generator.predicate()
        self.assertEqual(answer, [BasicVerb('use'), Noun('fire fighter', ''), exclamation])

    def test_sentence(self):
        random.seed(1)
        answer = self.generator.sentence()
        self.assertEqual(answer, [i, BasicVerb('feed', 'fed'), it, period])

        answer = self.generator.sentence()
        self.assertEqual(answer, [Noun('rice', ''), BasicVerb('eat', 'ate'), me, period])

        answer = self.generator.sentence()
        self.assertEqual(answer, [Noun('pizza', ''), BasicVerb('surprise'), it, period])

    @patch('sentences.random_sentences.verbs', with_preposition)
    def test_assign_preposition(self):
        random.seed(10)
        generator = RandomSentences()
        answer = generator.sentence()
        self.assertEqual(answer, [Noun('pony'), BasicVerb('jump'), Word('on'), Noun('elephant'), period])

        answer = generator.sentence()
        self.assertEqual(answer, [Noun('stinky tofu'), BasicVerb('jump'), Word('on'), Noun('cow'), period])

    @patch('sentences.random_sentences.verbs', two_subject_verbs)
    def test_two_subjects_second_subj_is_never_pronoun(self):
        random.seed(10)
        generator = RandomSentences()
        answer = generator.predicate(p_pronoun=0.8)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'), us, Noun('shark'), period])

        answer = generator.predicate(p_pronoun=0.8)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'), you, Noun('table'), period])

        answer = generator.predicate(p_pronoun=0.8)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'), them, Noun('baby'), period])

    @patch('sentences.random_sentences.verbs', two_subject_verbs)
    @patch('sentences.random_sentences.countable_nouns', three_nouns)
    @patch('sentences.random_sentences.uncountable_nouns', three_nouns)
    def test_two_subjects_are_never_the_same(self):
        random.seed(10)
        generator = RandomSentences()

        answer = generator.predicate(p_pronoun=0.0)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'),  Noun('dick'), Noun('tom'), period])

        answer = generator.predicate(p_pronoun=0.0)
        self.assertEqual(answer,[BasicVerb('bring', 'brought'),  Noun('dick'), Noun('tom'), period])

        answer = generator.predicate(p_pronoun=0.0)
        self.assertEqual(answer,[BasicVerb('bring', 'brought'),  Noun('harry'), Noun('tom'), period])

        answer = generator.predicate(p_pronoun=0.0)
        self.assertEqual(answer,[BasicVerb('bring', 'brought'),  Noun('tom'), Noun('harry'), period])

