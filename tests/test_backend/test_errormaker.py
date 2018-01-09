import random
import unittest

from sentences.backend.errormaker import (de_capitalize, copy_paragraph, make_verb_error, make_noun_error,
                                          ErrorMaker)
from sentences.words.noun import (Noun, PluralNoun, UncountableNoun, IndefiniteNoun, DefinitePluralNoun,
                                  DefiniteNoun)
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb, ThirdPersonVerb, PastVerb, NegativeVerb, NegativeThirdPersonVerb, NegativePastVerb
from sentences.words.word import Word
from sentences.words.pronoun import Pronoun


class TestErrorMaker(unittest.TestCase):
    def test_de_capitalize_with_noun(self):
        test = Noun('dog')
        definite = test.definite()
        indefinite = test.indefinite()
        plural = test.plural()
        definite_plural = definite.plural()
        test_list = [test, definite, indefinite, plural, definite_plural]
        for noun in test_list:
            to_test = de_capitalize(noun.capitalize())
            self.assertEqual(noun, to_test)
            self.assertEqual(type(noun), type(to_test))

    def test_de_capitalize_other(self):
        pronoun = Pronoun.HE
        word = Word('He')
        verb = Verb('He')
        for test_word in [pronoun, word, verb]:
            to_test = de_capitalize(test_word.capitalize())
            self.assertEqual(to_test.value, 'he')
            self.assertEqual(type(to_test), Word)

    def test_make_verb_error_present_third_person(self):
        random.seed(6)
        verb = Verb('play').third_person()
        plus_ed = [2, 8]
        plus_ed_plus_s = [0, 7]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=True)
            if index in plus_ed:
                self.assertEqual(PastVerb('played', 'play'), to_test)
            elif index in plus_ed_plus_s:
                self.assertEqual(PastVerb('playeds', 'playeds'), to_test)
            else:
                self.assertEqual(Verb('play'), to_test)

    def test_make_verb_error_present_negative_third_person(self):
        random.seed(6)
        verb = Verb('play').negative().third_person()
        plus_ed = [2, 8]
        plus_ed_plus_s = [0, 7]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=True)
            if index in plus_ed:
                self.assertEqual(NegativePastVerb("didn't play", 'play'), to_test)
            elif index in plus_ed_plus_s:
                self.assertEqual(NegativePastVerb("didn't plays", "didn't plays"), to_test)
            else:
                self.assertEqual(Verb('play').negative(), to_test)

    def test_make_verb_error_present_not_third_person(self):
        random.seed(6)
        verb = Verb('play')
        plus_ed = [1, 6]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=False)
            if index in plus_ed:
                self.assertEqual(PastVerb('played', 'play'), to_test)
            else:
                self.assertEqual(ThirdPersonVerb('plays', 'play'), to_test)

    def test_make_verb_error_present_negative_not_third_person(self):
        random.seed(6)
        verb = Verb('play').negative()
        plus_ed = [1, 6]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=False)
            if index in plus_ed:
                self.assertEqual(NegativePastVerb("didn't play", 'play'), to_test)
            else:
                self.assertEqual(NegativeThirdPersonVerb("doesn't play", 'play'), to_test)

    def test_make_verb_error_past_tense(self):
        random.seed(6)
        verb = Verb('play').past_tense()
        plus_s = [0, 3, 5, 6, 9]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=random.choice([True, False]))
            if index in plus_s:
                self.assertEqual(ThirdPersonVerb('plays', 'play'), to_test)
            else:
                self.assertEqual(Verb('play'), to_test)

    def test_make_verb_error_negative_past_tense(self):
        random.seed(6)
        verb = Verb('play').negative().past_tense()
        plus_s = [0, 3, 5, 6, 9]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=random.choice([True, False]))
            if index in plus_s:
                self.assertEqual(NegativeThirdPersonVerb("doesn't play", 'play'), to_test)
            else:
                self.assertEqual(NegativeVerb("don't play", 'play'), to_test)

    def test_make_noun_error_uncountable_not_definite(self):
        random.seed(10)
        noun = UncountableNoun('water')
        plural = [1, 2, 5, 6, 7]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in plural:
                self.assertEqual(PluralNoun('waters', base='water'), to_test)
            else:
                self.assertEqual(IndefiniteNoun('a water', base='water'), to_test)

    def test_make_noun_error_uncountable_definite(self):
        random.seed(10)
        noun = UncountableNoun('water').definite()
        plural = [1, 2, 5, 6, 7]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in plural:
                self.assertEqual(PluralNoun('waters', base='water'), to_test)
            else:
                self.assertEqual(IndefiniteNoun('a water', base='water'), to_test)

    def test_make_noun_error_plural_not_definite(self):
        random.seed(8)
        noun = PluralNoun('toys', base='toy')
        indefinite = [2, 12]
        definite = [10]
        indefinite_plural = [5, 13]
        for index in range(15):
            to_test = make_noun_error(noun)
            if index in indefinite:
                self.assertEqual(IndefiniteNoun('a toy', base='toy'), to_test)
            elif index in definite:
                self.assertEqual(DefiniteNoun('the toy', base='toy'), to_test)
            elif index in indefinite_plural:
                self.assertEqual('a toys', to_test.value)
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
                self.assertEqual(IndefiniteNoun('a toy', base='toy'), to_test)
            elif index in definite:
                self.assertEqual(DefiniteNoun('the toy', base='toy'), to_test)
            elif index in indefinite_plural:
                self.assertEqual('a toys', to_test.value)
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
                self.assertEqual(PluralNoun('toys', base='toy'), to_test)
            elif index in indefinite_plural:
                self.assertEqual('a toys', to_test.value)
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
                self.assertEqual(IndefiniteNoun('a toy', base='toy'), to_test)
            elif index in plural:
                self.assertEqual(PluralNoun('toys', base='toy'), to_test)
            elif index in indefinite_plural:
                self.assertEqual('a toys', to_test.value)
            else:
                self.assertEqual(Noun('toy'), to_test)

    def test_copy_paragraph_empty(self):
        empty = []
        self.assertIsNot(copy_paragraph(empty), empty)
        self.assertEqual(copy_paragraph(empty), empty)

    def test_copy_paragraph_single_sentence(self):
        single_sentence = [[Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION]]
        self.assertIsNot(copy_paragraph(single_sentence), single_sentence)
        self.assertIsNot(copy_paragraph(single_sentence)[0], single_sentence[0])
        self.assertEqual(copy_paragraph(single_sentence), single_sentence)

    def test_copy_paragraph_multiple_sentences(self):
        multiple_sentences = [[Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                              [Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION]]
        self.assertIsNot(copy_paragraph(multiple_sentences), multiple_sentences)
        self.assertIsNot(copy_paragraph(multiple_sentences)[0], multiple_sentences[0])
        self.assertEqual(copy_paragraph(multiple_sentences), multiple_sentences)

    def test_error_maker_init(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
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
        grab = Verb('grab')
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
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(2)
        all_error_maker = ErrorMaker(paragraph, p_error=1.0)
        all_error_maker.create_noun_errors()
        error_paragraph = [
            [Noun('Dog', '', 'dog'), grab.third_person(), Noun('cat'), Punctuation.EXCLAMATION],
            [IndefiniteNoun('A cats', 'a catses', 'cat'), grab, Noun('dog'), Punctuation.EXCLAMATION]
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
        grab = Verb('grab')
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
        grab = Verb('grab')
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
        grab = Verb('grab')
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
        grab = Verb('grab')
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
        grab = Verb('grab')
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
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().capitalize(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        all_error_maker = ErrorMaker(paragraph, p_error=1.0)
        all_error_maker.create_period_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.COMMA],
            [DefinitePluralNoun('the cats', '', 'cat'), grab, dog.definite(), Punctuation.COMMA]
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
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().capitalize(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        all_error_maker = ErrorMaker(paragraph, p_error=0.5)
        random.seed(1)
        all_error_maker.create_period_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.COMMA],
            [DefinitePluralNoun('the cats', '', 'cat'), grab, dog.definite(), Punctuation.EXCLAMATION]
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
        grab = Verb('grab')
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
        grab = Verb('grab')
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
