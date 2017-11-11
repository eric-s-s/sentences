import random
import unittest


from sentences.raw_word_randomisation import RawWordsRandomisation

from sentences.words.word import Word
from sentences.words.noun import Noun
from sentences.words.verb import BasicVerb
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation

period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun


class TestRawWordsRandomisation(unittest.TestCase):
    def setUp(self):
        self.generator = RawWordsRandomisation()

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
        self.assertEqual(answer, [BasicVerb('play', ''), Word('with'), Noun('octopus', ''), exclamation])

        answer = self.generator.predicate()
        self.assertEqual(answer, [BasicVerb('throw', 'threw'), Noun('tiger', ''), period])

        answer = self.generator.predicate()
        self.assertEqual(answer, [BasicVerb('throw', 'threw'), Noun('fire fighter', ''), exclamation])

    def test_sentence(self):
        random.seed(1)
        answer = self.generator.sentence()
        self.assertEqual(answer, [i, BasicVerb('feed', 'fed'), it, period])

        answer = self.generator.sentence()
        self.assertEqual(answer, [Noun('rice', ''), BasicVerb('eat', 'ate'), me, period])

        answer = self.generator.sentence()
        self.assertEqual(answer, [Noun('pizza', ''), BasicVerb('steal', 'stole'), it, period])
