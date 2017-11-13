import unittest

import random

from sentences.investigation_tools import (requires_third_person, is_third_person, find_subject, is_countable,
                                           is_word_in_sentence)
from sentences.words.noun import Noun
from sentences.words.verb import BasicVerb
from sentences.words.word import Word
from sentences.raw_word_randomisation import RawWordsRandomisation

from sentences.words.punctuation import Punctuation
from sentences.words.pronoun import Pronoun

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun
period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION


class TestInvestigationTools(unittest.TestCase):
    def test_is_countable(self):
        self.assertTrue(is_countable(Noun('child', 'children')))
        self.assertFalse(is_countable(Noun('water', '')))
        self.assertFalse(is_countable(he))
        self.assertFalse(is_countable(BasicVerb('eat', 'ate')))
        self.assertFalse(is_countable(Word('brick')))

    def test_is_countable_defaults_to_true_unless_in_loaded_uncountable_words(self):
        self.assertTrue(is_countable(Noun('not-in-the-list juice', '')))

    def test_is_countable_correctly_identifies_definite_uncountable_from_list(self):
        self.assertFalse(is_countable(Noun('water', '').definite()))

    def test_find_subject_on_standard_sentence(self):
        random.seed(5)
        maker = RawWordsRandomisation()
        sentence = maker.sentence()

        self.assertEqual(find_subject(sentence), 0)

        words = [Noun('orangutan'), Noun('bunny')]
        self.assertEqual(find_subject(words + sentence), 2)

    def test_find_subject_on_standard_predicate(self):
        random.seed(10)
        maker = RawWordsRandomisation()
        predicate = maker.predicate()

        self.assertEqual(find_subject(predicate), -1)

    def test_find_subject_limitations(self):
        sentence = [Word('to'), Word('boldly'), BasicVerb('go')]
        self.assertEqual(find_subject(sentence), 1)

        sentence = [Word('to'), Word('boldly'), Word('go')]
        self.assertEqual(find_subject(sentence), -1)

    def test_is_third_person_fails_on_word(self):
        self.assertFalse(is_third_person(Word('dog')))

    def test_is_third_person_pronouns_true(self):
        for third_person in [he, she, it, him, her]:
            self.assertTrue(is_third_person(third_person))

    def test_is_third_person_pronouns_false(self):
        for not_it in [i, me, you, we, us, they, them]:
            self.assertFalse(is_third_person(not_it))

    def test_is_third_person_all_non_plural_nouns(self):
        noun = Noun('dog')
        self.assertTrue(is_third_person(noun))
        self.assertTrue(is_third_person(noun.definite()))
        self.assertTrue(is_third_person(noun.indefinite()))

    def test_is_third_person_plural_nouns(self):
        noun = Noun('dog')
        self.assertFalse(is_third_person(noun.plural()))
        self.assertFalse(is_third_person(noun.definite().plural()))
        self.assertFalse(is_third_person(noun.plural().definite()))

    def test_requires_third_person(self):
        answer = [it, BasicVerb('steal', 'stole'), her, exclamation]
        self.assertTrue(requires_third_person(answer))

        answer = [Noun('teacher', ''), BasicVerb('take', 'took'), me, period]
        self.assertTrue(requires_third_person(answer))

        answer[0] = answer[0].plural()
        self.assertFalse(requires_third_person(answer))

        answer[0] = you
        self.assertFalse(requires_third_person(answer))

    def test_requires_third_person_no_subject(self):
        answer = [BasicVerb('STOP'), Word('in'), Noun('name').definite(), Word('of'), Noun('love'),
                  period, period, period]
        self.assertFalse(requires_third_person(answer))

    def test_is_word_in_sentence_pronoun(self):
        sentence = [i, BasicVerb('do').negative().past_tense(), it]
        self.assertTrue(is_word_in_sentence(me, sentence))
        self.assertTrue(is_word_in_sentence(i, sentence))
        self.assertFalse(is_word_in_sentence(they, sentence))
        self.assertTrue(is_word_in_sentence(it, sentence))

    def test_is_word_in_sentence_other(self):
        sentence = [Word('tom'), BasicVerb('dick'), Noun('harry')]
        self.assertTrue(is_word_in_sentence(Word('tom'), sentence))
        self.assertTrue(is_word_in_sentence(BasicVerb('dick'), sentence))
        self.assertTrue(is_word_in_sentence(Noun('harry'), sentence))

        self.assertFalse(is_word_in_sentence(Noun('tom'), sentence))
        self.assertFalse(is_word_in_sentence(Word('dick'), sentence))
        self.assertFalse(is_word_in_sentence(BasicVerb('harry'), sentence))
