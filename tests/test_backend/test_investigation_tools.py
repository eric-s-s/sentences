import unittest

from sentences.backend.investigation_tools import (requires_third_person, is_third_person, find_subject,
                                                   is_word_in_sentence, get_present_be_verb)
from sentences.words.noun import Noun, UncountableNoun
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb
from sentences.words.word import Word, Preposition

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun
period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION


class TestInvestigationTools(unittest.TestCase):
    def test_find_subject_on_standard_sentence(self):
        sentence = [Noun('cow'), Verb('give'), Noun('frog'), Preposition('to'), Noun('pig'), period]

        self.assertEqual(find_subject(sentence), 0)

        words = [Noun('orangutan'), Noun('bunny')]
        self.assertEqual(find_subject(words + sentence), 2)

    def test_find_subject_on_standard_predicate(self):

        predicate = [Verb('give'), Noun('frog'), Preposition('to'), Noun('pig'), period]

        self.assertEqual(find_subject(predicate), -1)

    def test_find_subject_limitations(self):
        sentence = [Word('to'), Word('boldly'), Verb('save_paragraphs_to_pdf')]
        self.assertEqual(find_subject(sentence), 1)

        sentence = [Word('to'), Word('boldly'), Word('save_paragraphs_to_pdf')]
        self.assertEqual(find_subject(sentence), -1)

    def test_is_third_person_fails_on_word(self):
        self.assertFalse(is_third_person(Word('dog')))

    def test_is_third_person_pronouns_true(self):
        for third_person in [he, she, it, him, her]:
            self.assertTrue(is_third_person(third_person))

    def test_is_third_person_pronouns_false(self):
        for not_it in [i, me, you, we, us, they, them]:
            self.assertFalse(is_third_person(not_it))

    def test_is_third_person_capitalized_pronouns_as_words(self):
        for word in [Word('He'), Word('She'), Word('It')]:
            self.assertTrue(is_third_person(word))

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
        answer = [it, Verb('steal', 'stole'), her, exclamation]
        self.assertTrue(requires_third_person(answer))

        answer = [Noun('teacher', ''), Verb('take', 'took'), me, period]
        self.assertTrue(requires_third_person(answer))

        answer[0] = answer[0].plural()
        self.assertFalse(requires_third_person(answer))

        answer[0] = you
        self.assertFalse(requires_third_person(answer))

    def test_requires_third_person_no_subject(self):
        answer = [Verb('STOP'), Word('in'), Noun('name').definite(), Word('of'), Noun('love'),
                  period, period, period]
        self.assertFalse(requires_third_person(answer))

    def test_is_word_in_sentence_pronoun(self):
        sentence = [i, Verb('do').negative().past_tense(), it]
        self.assertTrue(is_word_in_sentence(me, sentence))
        self.assertTrue(is_word_in_sentence(i, sentence))
        self.assertFalse(is_word_in_sentence(they, sentence))
        self.assertTrue(is_word_in_sentence(it, sentence))

    def test_is_word_in_sentence_other(self):
        sentence = [Word('tom'), Verb('dick'), Noun('harry')]
        self.assertTrue(is_word_in_sentence(Word('tom'), sentence))
        self.assertTrue(is_word_in_sentence(Verb('dick'), sentence))
        self.assertTrue(is_word_in_sentence(Noun('harry'), sentence))

        self.assertFalse(is_word_in_sentence(Noun('tom'), sentence))
        self.assertFalse(is_word_in_sentence(Word('dick'), sentence))
        self.assertFalse(is_word_in_sentence(Verb('harry'), sentence))

    def test_get_present_be_verb_no_subj(self):
        sentence = [Verb('Give'), Pronoun.ME, Noun('break').indefinite(), period]
        self.assertEqual(get_present_be_verb(sentence), Word('be'))

    def test_get_present_be_verb_are(self):
        predicate = [Verb('play'), period]
        subjs = [you, them, they, we, us, Word('You'), Word('They'), Word('We'),
                 Noun('dog').plural(), Noun('dog').definite().plural(), Noun('dog').plural().capitalize()]
        for subj in subjs:
            self.assertEqual(get_present_be_verb([subj] + predicate), Word('are'))

    def test_get_present_be_verb_is(self):
        predicate = [Verb('play').third_person(), period]
        subjs = [he, him, she, her, it, Word('He'), Word('She'), Word('It'),
                 UncountableNoun('water'), Noun('dog').definite(), Noun('dog').capitalize(), Noun('dog').indefinite()]
        for subj in subjs:
            self.assertEqual(get_present_be_verb([subj] + predicate), Word('is'))

    def test_get_present_be_verb_am(self):
        predicate = [Verb('play'), period]
        subjs = [i, me, i.capitalize()]
        for subj in subjs:
            self.assertEqual(get_present_be_verb([subj] + predicate), Word('am'))

