import unittest

import random

from sentences.errormaker import copy_paragraph, make_verb_error, make_noun_error, is_negative_verb, ErrorMaker

from sentences.words.word import Word
from sentences.words.noun import Noun, PluralNoun, UncountableNoun
from sentences.words.verb import BasicVerb, ConjugatedVerb
from sentences.words.punctuation import Punctuation


class TestErrorMaker(unittest.TestCase):
    def test_is_negative_verb_true(self):
        self.assertTrue(is_negative_verb(BasicVerb('play').negative()))
        self.assertTrue(is_negative_verb(BasicVerb('play').negative().past_tense()))
        self.assertTrue(is_negative_verb(BasicVerb('play').negative().third_person()))
        self.assertTrue(is_negative_verb(ConjugatedVerb('did not play', 'play')))
        self.assertTrue(is_negative_verb(ConjugatedVerb("didn't play", 'play')))
        self.assertTrue(is_negative_verb(ConjugatedVerb("do not play", 'play')))
        self.assertTrue(is_negative_verb(ConjugatedVerb("don't play", 'play')))
        self.assertTrue(is_negative_verb(ConjugatedVerb("doesn't play", 'play')))
        self.assertTrue(is_negative_verb(ConjugatedVerb("does not play", 'play')))

    def test_is_negative_verb_False(self):
        self.assertFalse(is_negative_verb(BasicVerb('play')))
        self.assertFalse(is_negative_verb(BasicVerb('play').past_tense()))
        self.assertFalse(is_negative_verb(BasicVerb('play').third_person()))

    def test_is_negative_cannot_use_bold(self):
        self.assertFalse(is_negative_verb(BasicVerb('play').negative().bold()))

    def test_make_verb_error_present_third_person(self):
        random.seed(6)
        verb = BasicVerb('play').third_person()
        plus_ed = [2, 8]
        plus_ed_plus_s = [0, 7]
        for index in range(10):
            to_test = make_verb_error(verb, present_tense=True, third_person=True)
            if index in plus_ed:
                self.assertEqual(ConjugatedVerb('played', 'play'), to_test)
            elif index in plus_ed_plus_s:
                self.assertEqual(ConjugatedVerb('playeds', 'playeds'), to_test)
            else:
                self.assertEqual(BasicVerb('play'), to_test)

    def test_make_verb_error_present_negative_third_person(self):
        random.seed(6)
        verb = BasicVerb('play').negative().third_person()
        plus_ed = [2, 8]
        plus_ed_plus_s = [0, 7]
        for index in range(10):
            to_test = make_verb_error(verb, present_tense=True, third_person=True)
            if index in plus_ed:
                self.assertEqual(ConjugatedVerb("didn't play", 'play'), to_test)
            elif index in plus_ed_plus_s:
                self.assertEqual(ConjugatedVerb("didn't plays", "didn't plays"), to_test)
            else:
                self.assertEqual(BasicVerb('play').negative(), to_test)

    def test_make_verb_error_present_not_third_person(self):
        random.seed(6)
        verb = BasicVerb('play')
        plus_ed = [1, 6]
        for index in range(10):
            to_test = make_verb_error(verb, present_tense=True, third_person=False)
            if index in plus_ed:
                self.assertEqual(ConjugatedVerb('played', 'play'), to_test)
            else:
                self.assertEqual(ConjugatedVerb('plays', 'play'), to_test)

    def test_make_verb_error_present_negative_not_third_person(self):
        random.seed(6)
        verb = BasicVerb('play').negative()
        plus_ed = [1, 6]
        for index in range(10):
            to_test = make_verb_error(verb, present_tense=True, third_person=False)
            if index in plus_ed:
                self.assertEqual(ConjugatedVerb("didn't play", 'play'), to_test)
            else:
                self.assertEqual(ConjugatedVerb("doesn't play", 'play'), to_test)

    def test_make_verb_error_past_tense(self):
        random.seed(6)
        verb = BasicVerb('play').past_tense()
        plus_s = [0, 3, 5, 6, 9]
        for index in range(10):
            to_test = make_verb_error(verb, present_tense=False, third_person=random.choice([True, False]))
            if index in plus_s:
                self.assertEqual(ConjugatedVerb('plays', 'play'), to_test)
            else:
                self.assertEqual(BasicVerb('play'), to_test)

    def test_make_verb_error_negative_past_tense(self):
        random.seed(6)
        verb = BasicVerb('play').negative().past_tense()
        plus_s = [0, 3, 5, 6, 9]
        for index in range(10):
            to_test = make_verb_error(verb, present_tense=False, third_person=random.choice([True, False]))
            if index in plus_s:
                self.assertEqual(ConjugatedVerb("doesn't play", 'play'), to_test)
            else:
                self.assertEqual(ConjugatedVerb("don't play", 'play'), to_test)

    def test_make_noun_error_uncountable_not_definite(self):
        random.seed(10)
        noun = UncountableNoun('water')
        plural = [1, 2, 5, 6, 7]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in plural:
                self.assertEqual(Noun('waters', base='water'), to_test)
            else:
                self.assertEqual(Noun('a water', base='water'), to_test)

    def test_make_noun_error_uncountable_definite(self):
        random.seed(10)
        noun = UncountableNoun('water').definite()
        plural = [1, 2, 5, 6, 7]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in plural:
                self.assertEqual(Noun('waters', base='water'), to_test)
            else:
                self.assertEqual(Noun('a water', base='water'), to_test)

    def test_make_noun_error_plural_not_definite(self):
        random.seed(8)
        noun = PluralNoun('toys', base='toy')
        indefinite = [2, 12]
        definite = [10]
        indefinite_plural = [5, 13]
        for index in range(15):
            to_test = make_noun_error(noun)
            if index in indefinite:
                self.assertEqual(Noun('a toy', base='toy'), to_test)
            elif index in definite:
                self.assertEqual(Noun('the toy', base='toy'), to_test)
            elif index in indefinite_plural:
                self.assertEqual(Noun('a toys', base='toy'), to_test)
            else:
                self.assertEqual(Noun('toy'), to_test)

    def test_make_noun_error_plural_definite(self):
        random.seed(8)
        noun = Noun('toy').plural().definite()
        indefinite = [2, 12]
        definite = [10]
        indefinite_plural = [5, 13]
        for index in range(15):
            to_test = make_noun_error(noun)
            if index in indefinite:
                self.assertEqual(Noun('a toy', base='toy'), to_test)
            elif index in definite:
                self.assertEqual(Noun('the toy', base='toy'), to_test)
            elif index in indefinite_plural:
                self.assertEqual(Noun('a toys', base='toy'), to_test)
            else:
                self.assertEqual(Noun('toy'), to_test)

    def test_make_noun_error_indefinite(self):
        random.seed(2)
        noun = Noun('toy').indefinite()
        plural = [7, 9, 11]
        indefinite_plural = [13, 14]
        for index in range(15):
            to_test = make_noun_error(noun)
            if index in plural:
                self.assertEqual(Noun('toys', base='toy'), to_test)
            elif index in indefinite_plural:
                self.assertEqual(Noun('a toys', base='toy'), to_test)
            else:
                self.assertEqual(Noun('toy'), to_test)

    def test_make_noun_error_definite(self):
        random.seed(4)
        noun = Noun('toy').definite()
        indefinite = [4, 5, 10]
        plural = [11]
        indefinite_plural = [3]
        for index in range(15):
            to_test = make_noun_error(noun)
            if index in indefinite:
                self.assertEqual(Noun('a toy', base='toy'), to_test)
            elif index in plural:
                self.assertEqual(Noun('toys', base='toy'), to_test)
            elif index in indefinite_plural:
                self.assertEqual(Noun('a toys', base='toy'), to_test)
            else:
                self.assertEqual(Noun('toy'), to_test)

    def test_copy_paragraph_empty(self):
        empty = []
        self.assertIsNot(copy_paragraph(empty), empty)
        self.assertEqual(copy_paragraph(empty), empty)

    def test_copy_paragraph_single_sentence(self):
        single_sentence = [[Noun('cat'), BasicVerb('grab'), Noun('cat'), Punctuation.EXCLAMATION]]
        self.assertIsNot(copy_paragraph(single_sentence), single_sentence)
        self.assertIsNot(copy_paragraph(single_sentence)[0], single_sentence[0])
        self.assertEqual(copy_paragraph(single_sentence), single_sentence)

    def test_copy_paragraph_multiple_sentences(self):
        multiple_sentences = [[Noun('cat'), BasicVerb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                              [Noun('cat'), BasicVerb('grab'), Noun('cat'), Punctuation.EXCLAMATION]]
        self.assertIsNot(copy_paragraph(multiple_sentences), multiple_sentences)
        self.assertIsNot(copy_paragraph(multiple_sentences)[0], multiple_sentences[0])
        self.assertEqual(copy_paragraph(multiple_sentences), multiple_sentences)

    def test_error_maker_init(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=0.5)
        self.assertEqual(error_maker.paragraph, paragraph)
        self.assertEqual(error_maker.present_tense, True)
        self.assertEqual(error_maker.answer_paragraph, paragraph)
        self.assertEqual(error_maker.error_paragraph, paragraph)
        self.assertEqual(error_maker.p_error, 0.5)

        self.assertIsNot(error_maker.paragraph, paragraph)
        self.assertIsNot(error_maker.answer_paragraph, paragraph)
        self.assertIsNot(error_maker.error_paragraph, paragraph)

    def test_error_maker_create_errors_no_errors(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]

        no_error_maker = ErrorMaker(paragraph, p_error=0.0)
        no_error_maker.create_noun_errors()
        self.assertEqual(no_error_maker.error_paragraph, paragraph)

        no_error_maker.create_verb_errors()
        self.assertEqual(no_error_maker.error_paragraph, paragraph)

        no_error_maker.create_period_errors()
        self.assertEqual(no_error_maker.error_paragraph, paragraph)

        no_error_maker.create_all_errors()
        self.assertEqual(no_error_maker.error_paragraph, paragraph)

    def test_error_maker_create_noun_errors_all_errors_also_capitalizes_errors_at_start_of_sentence(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(2)
        all_error_maker = ErrorMaker(paragraph, p_error=1.0)
        all_error_maker.create_noun_errors()
        error_paragraph = [
            [Noun('Dog', '', 'dog'), grab.third_person(), Noun('cat'), Punctuation.EXCLAMATION],
            [Noun('A cats', 'a catses', 'cat'), grab, Noun('dog'), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite().bold(), grab.third_person(), cat.plural().bold(), Punctuation.EXCLAMATION],
            [cat.plural().definite().bold(), grab, dog.definite().bold(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(all_error_maker.error_paragraph, error_paragraph)
        self.assertEqual(all_error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_noun_errors_some_errors(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(2)
        all_error_maker = ErrorMaker(paragraph, p_error=0.5)
        all_error_maker.create_noun_errors()
        error_paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.capitalize(), grab, dog, Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().bold(), grab, dog.definite().bold(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(all_error_maker.error_paragraph, error_paragraph)
        self.assertEqual(all_error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_verb_errors_all_errors_present_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(2)
        all_error_maker = ErrorMaker(paragraph, p_error=1.0)
        all_error_maker.create_verb_errors()
        error_paragraph = [
            [dog.indefinite(), grab, cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.third_person(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.third_person().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.bold(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(all_error_maker.error_paragraph, error_paragraph)
        self.assertEqual(all_error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_verb_errors_some_errors_present_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(4)
        all_error_maker = ErrorMaker(paragraph, p_error=0.5)
        all_error_maker.create_verb_errors()
        error_paragraph = [
            [dog.indefinite(), grab, cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.third_person().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(all_error_maker.error_paragraph, error_paragraph)
        self.assertEqual(all_error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_verb_errors_all_errors_past_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite(), grab.past_tense(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(2)
        all_error_maker = ErrorMaker(paragraph, p_error=1.0, present_tense=False)
        all_error_maker.create_verb_errors()
        error_paragraph = [
            [dog.indefinite(), grab, cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.third_person(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.past_tense().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense().bold(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(all_error_maker.error_paragraph, error_paragraph)
        self.assertEqual(all_error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_verb_errors_some_errors_past_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite(), grab.past_tense(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(4)
        all_error_maker = ErrorMaker(paragraph, p_error=0.5, present_tense=False)
        all_error_maker.create_verb_errors()
        error_paragraph = [
            [dog.indefinite(), grab, cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.past_tense().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(all_error_maker.error_paragraph, error_paragraph)
        self.assertEqual(all_error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_period_errors_all_errors_and_decapitalizes(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().capitalize(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        all_error_maker = ErrorMaker(paragraph, p_error=1.0)
        all_error_maker.create_period_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.COMMA],
            [Word('the cats'), grab, dog.definite(), Punctuation.COMMA]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION.bold()],
            [cat.plural().definite().capitalize().bold(), grab, dog.definite(), Punctuation.EXCLAMATION.bold()]
        ]
        self.assertEqual(all_error_maker.error_paragraph, error_paragraph)
        self.assertEqual(all_error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_period_errors_some_errors(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().capitalize(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        all_error_maker = ErrorMaker(paragraph, p_error=0.5)
        random.seed(1)
        all_error_maker.create_period_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.COMMA],
            [Word('the cats'), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION.bold()],
            [cat.plural().definite().capitalize().bold(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(all_error_maker.error_paragraph, error_paragraph)
        self.assertEqual(all_error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_all_errors(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION]
        ]
        all_error_maker = ErrorMaker(paragraph, p_error=1.0)
        random.seed(1)
        all_error_maker.create_all_errors()
        error_paragraph = [
            [dog.capitalize(), grab.past_tense(), cat.indefinite(), Punctuation.COMMA],
        ]
        answer_paragraph = [[dog.indefinite().capitalize().bold(), grab.third_person().bold(), cat.plural().bold(),
                             Punctuation.EXCLAMATION.bold()]]

        self.assertEqual(all_error_maker.error_paragraph, error_paragraph)
        self.assertEqual(all_error_maker.answer_paragraph, answer_paragraph)

    def test_error_count_and_reset(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = BasicVerb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION]
        ]
        all_error_maker = ErrorMaker(paragraph, p_error=1.0)
        self.assertEqual(all_error_maker.error_count, 0)
        all_error_maker.create_all_errors()
        self.assertEqual(all_error_maker.error_count, 4)
        all_error_maker.reset()
        self.assertEqual(all_error_maker.error_count, 0)
        self.assertEqual(all_error_maker.error_paragraph, paragraph)

        all_error_maker.create_noun_errors()
        self.assertEqual(all_error_maker.error_count, 2)
