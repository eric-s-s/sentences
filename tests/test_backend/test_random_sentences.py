import random
import unittest

from sentences.backend.random_sentences import RandomSentences
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import BasicVerb
from sentences.words.word import Word

period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun


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
        self.assertEqual(answer, [BasicVerb('marry', ''), Noun('octopus', ''), exclamation])

        answer = self.generator.predicate()
        self.assertEqual(answer, [BasicVerb('wash'), Noun('gold', ''), exclamation])

        answer = self.generator.predicate()
        self.assertEqual(answer, [BasicVerb('bang'), Noun('poop', ''), period])

    def test_sentence(self):
        random.seed(1)
        answer = self.generator.sentence()
        self.assertEqual(answer, [i, BasicVerb('excite'), it, period])

        answer = self.generator.sentence()
        self.assertEqual(answer, [Noun('rice', ''), BasicVerb('disgust'), me, period])

        answer = self.generator.sentence()
        self.assertEqual(answer, [Noun('pizza', ''), BasicVerb('shake', 'shook'), it, period])

    def test_assign_preposition(self):
        file_name = 'tests/test_files/jump_on.csv'
        random.seed(10)
        generator = RandomSentences(verb_file=file_name)
        answer = generator.sentence()
        self.assertEqual(answer, [Noun('pony'), BasicVerb('jump'), Word('on'), Noun('elephant'), period])

        answer = generator.sentence()
        self.assertEqual(answer, [Noun('stinky tofu'), BasicVerb('jump'), Word('on'), Noun('cow'), period])

    def test_assign_preposition_insert_preposition_true(self):
        file_name = 'tests/test_files/bring_to.csv'
        random.seed(10)
        generator = RandomSentences(verb_file=file_name)
        answer = generator.sentence()
        self.assertEqual(answer, [Noun('pony'), BasicVerb('bring', 'brought'), Noun('elephant'),
                                  Word('to'), Noun('table'), period])

        answer = generator.sentence()
        self.assertEqual(answer, [Noun('cow'), BasicVerb('bring', 'brought'), Noun('leaf'),
                                  Word('to'), Noun('money'), period])

    def test_two_subjects_second_subj_is_never_pronoun(self):
        file_name = 'tests/test_files/bring.csv'
        random.seed(10)
        generator = RandomSentences(verb_file=file_name)
        answer = generator.predicate(p_pronoun=0.8)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'), us, Noun('shark'), period])

        answer = generator.predicate(p_pronoun=0.8)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'), you, Noun('table'), period])

        answer = generator.predicate(p_pronoun=0.8)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'), them, Noun('baby'), period])

    def test_two_subjects_are_never_the_same(self):
        verb_file = 'tests/test_files/bring.csv'
        countable = 'tests/test_files/three_nouns.csv'
        uncountable = 'tests/test_files/three_nouns.csv'
        random.seed(10)
        generator = RandomSentences(verb_file=verb_file, countable_file=countable, uncountable_file=uncountable)

        answer = generator.predicate(p_pronoun=0.0)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'),  Noun('dick'), Noun('tom'), period])

        answer = generator.predicate(p_pronoun=0.0)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'),  Noun('dick'), Noun('tom'), period])

        answer = generator.predicate(p_pronoun=0.0)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'),  Noun('harry'), Noun('tom'), period])

        answer = generator.predicate(p_pronoun=0.0)
        self.assertEqual(answer, [BasicVerb('bring', 'brought'),  Noun('tom'), Noun('harry'), period])
