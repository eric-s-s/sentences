import random
import unittest
from typing import List, Any

from sentences.backend.errormaker import (de_capitalize, copy_paragraph, make_verb_error, make_noun_error,
                                          make_is_do_error, find_subject_special_case, ErrorMaker)
from sentences.words.noun import (Noun, PluralNoun, UncountableNoun, IndefiniteNoun, DefinitePluralNoun,
                                  DefiniteNoun, ProperNoun, PluralProperNoun)
from sentences.words.punctuation import Punctuation
from sentences.words.verb import (Verb, ThirdPersonVerb, PastVerb,
                                  NegativeVerb, NegativeThirdPersonVerb, NegativePastVerb)
from sentences.words.word import Word, Preposition
from sentences.words.pronoun import Pronoun, CapitalPronoun


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

    def test_de_capitalize_with_proper_noun(self):
        self.assertEqual(de_capitalize(ProperNoun('Joe')), ProperNoun('Joe'))
        self.assertEqual(de_capitalize(ProperNoun('the Dude').capitalize()), ProperNoun('the Dude'))
        self.assertEqual(de_capitalize(PluralProperNoun('Joes')), PluralProperNoun('Joes'))

    def test_de_capitalize_with_pronoun(self):
        expected = Pronoun.I
        capital = expected.capitalize()
        for p_noun in (expected, capital):
            self.assertEqual(de_capitalize(p_noun), expected)

    def test_de_capitalize_other(self):
        word = Word('He')
        verb = Verb('He')
        for test_word in [word, verb]:
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
                self.assertEqual(PastVerb('played', '', 'play'), to_test)
            elif index in plus_ed_plus_s:
                self.assertEqual(PastVerb('playeds', '', 'play'), to_test)
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
                self.assertEqual(NegativePastVerb("didn't play", '', 'play'), to_test)
            elif index in plus_ed_plus_s:
                self.assertEqual(NegativePastVerb("didn't plays", '', "play"), to_test)
            else:
                self.assertEqual(Verb('play').negative(), to_test)

    def test_make_verb_error_present_not_third_person(self):
        random.seed(6)
        verb = Verb('play')
        plus_ed = [1, 6]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=False)
            if index in plus_ed:
                self.assertEqual(PastVerb('played', '', 'play'), to_test)
            else:
                self.assertEqual(ThirdPersonVerb('plays', '', 'play'), to_test)

    def test_make_verb_error_present_negative_not_third_person(self):
        random.seed(6)
        verb = Verb('play').negative()
        plus_ed = [1, 6]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=False)
            if index in plus_ed:
                self.assertEqual(NegativePastVerb("didn't play", '', 'play'), to_test)
            else:
                self.assertEqual(NegativeThirdPersonVerb("doesn't play", '', 'play'), to_test)

    def test_make_verb_error_past_tense(self):
        random.seed(6)
        verb = Verb('play').past_tense()
        plus_s = [0, 3, 5, 6, 9]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=random.choice([True, False]))
            if index in plus_s:
                self.assertEqual(ThirdPersonVerb('plays', '', 'play'), to_test)
            else:
                self.assertEqual(Verb('play'), to_test)

    def test_make_verb_error_negative_past_tense(self):
        random.seed(6)
        verb = Verb('play').negative().past_tense()
        plus_s = [0, 3, 5, 6, 9]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=random.choice([True, False]))
            if index in plus_s:
                self.assertEqual(NegativeThirdPersonVerb("doesn't play", '', 'play'), to_test)
            else:
                self.assertEqual(NegativeVerb("don't play", '', 'play'), to_test)

    def test_make_noun_error_proper_no_article(self):
        random.seed(191)
        noun = ProperNoun('Joe')
        definite = [1, 2, 6, 7, 8, 9]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in definite:
                self.assertEqual(DefiniteNoun('the Joe', '', 'Joe'), to_test)
            else:
                self.assertEqual(IndefiniteNoun('a Joe', '', 'Joe'), to_test)

    def test_make_noun_error_proper_with_article(self):
        random.seed(6541)
        noun = ProperNoun('the Dude').capitalize()
        definite = [0, 1, 2, 7, 8, 9]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in definite:
                self.assertEqual(DefiniteNoun('the the Dude', '', 'the Dude'), to_test)
            else:
                self.assertEqual(IndefiniteNoun('a the Dude', '', 'the Dude'), to_test)

    def test_make_noun_error_plural_proper(self):
        random.seed(69167)
        noun = PluralProperNoun('Eds').capitalize()
        definite = [1, 5, 8, 9]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in definite:
                self.assertEqual(DefinitePluralNoun('the Eds', '', 'Eds'), to_test)
            else:
                self.assertEqual(IndefiniteNoun('an Eds', '', 'Eds'), to_test)

    def test_make_noun_error_plural_proper_with_article(self):
        random.seed(2559)
        noun = PluralProperNoun('the Joneses').capitalize()
        definite = [0, 1, 2, 8]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in definite:
                self.assertEqual(DefinitePluralNoun('the the Joneses', '', 'the Joneses'), to_test)
            else:
                self.assertEqual(IndefiniteNoun('a the Joneses', '', 'the Joneses'), to_test)

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

    def test_is_do_error_present_not_negative(self):
        verb = Verb('go')
        self.assertEqual(make_is_do_error(verb, Word('am')), Word('am go'))
        self.assertEqual(make_is_do_error(verb, Word('are')), Word('are go'))
        self.assertEqual(make_is_do_error(verb.third_person(), Word('is')), Word('is go'))

    def test_is_do_error_present_negative(self):
        verb = Verb('go').negative()
        self.assertEqual(make_is_do_error(verb, Word('am')), Word('am not go'))
        self.assertEqual(make_is_do_error(verb, Word('are')), Word('are not go'))
        self.assertEqual(make_is_do_error(verb.third_person(), Word('is')), Word('is not go'))

    def test_is_do_error_past_not_negative(self):
        verb = Verb('go', 'went', '').past_tense()
        self.assertEqual(make_is_do_error(verb, Word('am')), Word('was go'))
        self.assertEqual(make_is_do_error(verb, Word('are')), Word('were go'))
        self.assertEqual(make_is_do_error(verb, Word('is')), Word('was go'))

    def test_is_do_error_past_negative(self):
        verb = Verb('go', 'went', '').negative().past_tense()
        self.assertEqual(make_is_do_error(verb, Word('am')), Word('was not go'))
        self.assertEqual(make_is_do_error(verb, Word('are')), Word('were not go'))
        self.assertEqual(make_is_do_error(verb, Word('is')), Word('was not go'))

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
        self.assertEqual(error_maker.answer_paragraph, paragraph)
        self.assertEqual(error_maker.error_paragraph, paragraph)
        self.assertEqual(error_maker.p_error, 0.5)

        self.assertIsNot(error_maker.paragraph, paragraph)
        self.assertIsNot(error_maker.answer_paragraph, paragraph)
        self.assertIsNot(error_maker.error_paragraph, paragraph)

        expected = [
            error_maker.create_noun_errors, error_maker.create_pronoun_errors, error_maker.create_verb_errors,
            error_maker.create_is_do_errors, error_maker.create_preposition_transpose_errors,
            error_maker.create_period_errors
        ]
        self.assertEqual(error_maker.method_order, expected)

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
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_noun_errors()
        error_paragraph = [
            [Noun('Dog', '', 'dog'), grab.third_person(), Noun('cat'), Punctuation.EXCLAMATION],
            [IndefiniteNoun('A cats', '', 'cat'), grab, Noun('dog'), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite().bold(), grab.third_person(), cat.plural().bold(), Punctuation.EXCLAMATION],
            [cat.plural().definite().bold(), grab, dog.definite().bold(), Punctuation.EXCLAMATION]
        ]

        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)
        self.assertEqual(error_maker.error_count, 4)

    def test_error_maker_create_noun_errors_some_errors(self):
        dog = Noun('dog')
        joe = ProperNoun('Joe')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), joe, Punctuation.EXCLAMATION],
            [joe, grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(2)
        error_maker = ErrorMaker(paragraph, p_error=0.5)
        error_maker.create_noun_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), joe, Punctuation.EXCLAMATION],
            [joe.indefinite().capitalize(), grab, dog, Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), joe, Punctuation.EXCLAMATION],
            [joe.bold(), grab, dog.definite().bold(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_pronoun_errors_it_and_you(self):
        grab = Verb('grab')
        paragraph = [
            [CapitalPronoun.IT, grab, Pronoun.IT, Punctuation.EXCLAMATION],
            [CapitalPronoun.YOU, grab, Pronoun.YOU, Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_pronoun_errors()
        error_paragraph = [
            [CapitalPronoun.IT, grab, Pronoun.IT, Punctuation.EXCLAMATION],
            [CapitalPronoun.YOU, grab, Pronoun.YOU, Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [CapitalPronoun.IT, grab, Pronoun.IT, Punctuation.EXCLAMATION],
            [CapitalPronoun.YOU, grab, Pronoun.YOU, Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_pronoun_errors_all_errors(self):
        grab = Verb('grab')
        paragraph = [
            [CapitalPronoun.I, grab, Pronoun.THEM, Punctuation.EXCLAMATION],
            [CapitalPronoun.SHE, grab, Pronoun.US, Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_pronoun_errors()
        error_paragraph = [
            [CapitalPronoun.ME, grab, Pronoun.THEY, Punctuation.EXCLAMATION],
            [CapitalPronoun.HER, grab, Pronoun.WE, Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [CapitalPronoun.I.bold(), grab, Pronoun.THEM.bold(), Punctuation.EXCLAMATION],
            [CapitalPronoun.SHE.bold(), grab, Pronoun.US.bold(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)
        self.assertEqual(error_maker.error_count, 4)

    def test_error_maker_create_pronoun_errors_some_errors(self):
        grab = Verb('grab')
        paragraph = [
            [CapitalPronoun.I, grab, Pronoun.THEM, Punctuation.EXCLAMATION],
            [CapitalPronoun.SHE, grab, Pronoun.US, Punctuation.EXCLAMATION]
        ]
        random.seed(45615)
        error_maker = ErrorMaker(paragraph, p_error=0.5)
        error_maker.create_pronoun_errors()
        error_paragraph = [
            [CapitalPronoun.I, grab, Pronoun.THEY, Punctuation.EXCLAMATION],
            [CapitalPronoun.HER, grab, Pronoun.WE, Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [CapitalPronoun.I, grab, Pronoun.THEM.bold(), Punctuation.EXCLAMATION],
            [CapitalPronoun.SHE.bold(), grab, Pronoun.US.bold(), Punctuation.EXCLAMATION]
        ]

        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_verb_errors_all_errors_present_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(2)
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_verb_errors()
        error_paragraph = [
            [dog.indefinite(), grab, cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.third_person(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.third_person().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.bold(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)
        self.assertEqual(error_maker.error_count, 2)

    def test_error_maker_create_verb_errors_some_errors_present_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(4)
        error_maker = ErrorMaker(paragraph, p_error=0.5)
        error_maker.create_verb_errors()
        error_paragraph = [
            [dog.indefinite(), grab, cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.third_person().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_verb_errors_all_errors_past_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite(), grab.past_tense(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(2)
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_verb_errors()
        error_paragraph = [
            [dog.indefinite(), grab, cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.third_person(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.past_tense().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense().bold(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_verb_errors_some_errors_past_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite(), grab.past_tense(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(4)
        error_maker = ErrorMaker(paragraph, p_error=0.5)
        error_maker.create_verb_errors()
        error_paragraph = [
            [dog.indefinite(), grab, cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.past_tense().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_is_do_errors_all_errors_present_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_is_do_errors()
        error_paragraph = [
            [dog.indefinite(), Word('is grab'), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), Word('are grab'), dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.third_person().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.bold(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)
        self.assertEqual(error_maker.error_count, 2)

    def test_error_maker_create_is_do_errors_some_errors_present_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(8)
        error_maker = ErrorMaker(paragraph, p_error=0.5)
        error_maker.create_is_do_errors()
        error_paragraph = [
            [dog.indefinite(), Word('is grab'), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.third_person().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_is_do_errors_all_errors_past_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite(), grab.past_tense(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(2)
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_is_do_errors()
        error_paragraph = [
            [dog.indefinite(), Word('was grab'), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), Word('were grab'), dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.past_tense().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense().bold(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_is_do_errors_some_errors_past_tense(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite(), grab.past_tense(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        random.seed(8)
        error_maker = ErrorMaker(paragraph, p_error=0.5)
        error_maker.create_is_do_errors()
        error_paragraph = [
            [dog.indefinite(), Word('was grab'), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite(), grab.past_tense().bold(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), grab.past_tense(), dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_is_do_errors_all_pronouns(self):
        predicate = [Verb('go'), Noun('home'), Punctuation.PERIOD]  # type: List[Any]
        expected = {
            (Pronoun.I, CapitalPronoun.I): Word('am go'),
            (Pronoun.HE, Pronoun.SHE, Pronoun.IT,
             CapitalPronoun.HE, CapitalPronoun.SHE, CapitalPronoun.IT): Word('is go'),
            (Pronoun.YOU, Pronoun.WE, Pronoun.THEY,
             CapitalPronoun.YOU, CapitalPronoun.WE, CapitalPronoun.THEY): Word('are go')
        }
        for subj_list, is_do in expected.items():
            for subj in subj_list:
                paragraph = [[subj] + predicate]  # type: List[Any]
                error_maker = ErrorMaker(paragraph, p_error=1.0)
                error_maker.create_is_do_errors()
                self.assertEqual(error_maker.error_paragraph[0][1], is_do)

    def test_error_maker_create_period_errors_all_errors_and_decapitalizes(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().capitalize(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_period_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.COMMA],
            [DefinitePluralNoun('the cats', '', 'cat'), grab, dog.definite(), Punctuation.COMMA]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION.bold()],
            [cat.plural().definite().capitalize().bold(), grab, dog.definite(), Punctuation.EXCLAMATION.bold()]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)
        self.assertEqual(error_maker.error_count, 2)

    def test_error_maker_create_period_errors_does_not_bold_when_proper_noun_is_unchanged(self):
        sox = PluralProperNoun('the Sox')
        joe = ProperNoun('Joe')
        grab = Verb('grab')
        paragraph = [
            [joe, grab.third_person(), sox, Punctuation.EXCLAMATION],
            [sox.capitalize(), grab, joe, Punctuation.EXCLAMATION],
            [joe, grab.third_person(), sox, Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_period_errors()
        error_paragraph = [
            [joe, grab.third_person(), sox, Punctuation.COMMA],
            [sox, grab, joe, Punctuation.COMMA],
            [joe, grab.third_person(), sox, Punctuation.COMMA]
        ]
        answer_paragraph = [
            [joe, grab.third_person(), sox, Punctuation.EXCLAMATION.bold()],
            [sox.capitalize().bold(), grab, joe, Punctuation.EXCLAMATION.bold()],
            [joe, grab.third_person(), sox, Punctuation.EXCLAMATION.bold()]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)
        self.assertEqual(error_maker.error_count, 3)

    def test_error_maker_create_period_errors_some_errors(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().capitalize(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=0.5)
        random.seed(1)
        error_maker.create_period_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.COMMA],
            [DefinitePluralNoun('the cats', '', 'cat'), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION.bold()],
            [cat.plural().definite().capitalize().bold(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_preposition_transpose_errors_no_prepositions(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().capitalize(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        random.seed(1)
        error_maker.create_preposition_transpose_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().capitalize(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite().capitalize(), grab, dog.definite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_preposition_transpose_errors_all_errors(self):
        dog = Noun('dog')
        cat = Noun('cat')
        pig = Noun('pig')
        jump = Verb('jump')
        on = Preposition('on')
        hit = Verb('hit')
        with_ = Preposition('with')

        paragraph = [
            [dog.indefinite().capitalize(), jump.third_person(), on, cat.plural(), Punctuation.EXCLAMATION],
            [cat.definite().capitalize(), hit, dog.definite(), with_, pig.indefinite(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_preposition_transpose_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), on, cat.plural(), jump.third_person(), Punctuation.EXCLAMATION],
            [cat.definite().capitalize(), with_, pig.indefinite(), hit, dog.definite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize(), jump.third_person(), on.bold(), cat.plural().bold(),
             Punctuation.EXCLAMATION],
            [cat.definite().capitalize(), hit, dog.definite(), with_.bold(), pig.indefinite().bold(),
             Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)
        self.assertEqual(error_maker.error_count, 2)

    def test_error_maker_create_preposition_transpose_errors_some_errors(self):
        dog = Noun('dog')
        cat = Noun('cat')
        pig = Noun('pig')
        jump = Verb('jump')
        on = Preposition('on')
        hit = Verb('hit')
        with_ = Preposition('with')
        random.seed(8)
        paragraph = [
            [dog.indefinite().capitalize(), jump.third_person(), on, cat.plural(), Punctuation.EXCLAMATION],
            [cat.definite().capitalize(), hit, dog.definite(), with_, pig.indefinite(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=0.5)
        error_maker.create_preposition_transpose_errors()
        error_paragraph = [
            [dog.indefinite().capitalize(), on, cat.plural(), jump.third_person(), Punctuation.EXCLAMATION],
            [cat.definite().capitalize(), hit, dog.definite(), with_, pig.indefinite(), Punctuation.EXCLAMATION]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize(), jump.third_person(), on.bold(), cat.plural().bold(),
             Punctuation.EXCLAMATION],
            [cat.definite().capitalize(), hit, dog.definite(), with_, pig.indefinite(), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_maker_create_all_errors(self):
        dog = Noun('dog')
        cat = Noun('cat')
        hit = Verb('hit')
        with_ = Preposition('with')
        paragraph = [
            [dog.indefinite().capitalize(), hit.third_person(), Pronoun.ME, with_, cat.plural(),
             Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        random.seed(1)
        error_maker.create_all_errors()
        error_paragraph = [
            [dog.capitalize(), Preposition('with'), cat.indefinite(), Word('was hit'), Pronoun.I, Punctuation.COMMA]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize().bold(), hit.third_person().bold(), Pronoun.ME.bold(), with_.bold(),
             cat.plural().bold(), Punctuation.EXCLAMATION.bold()]]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_find_subject_special_case_special_cases(self):
        go = Verb('go')
        after_verb = [Noun('home'), Punctuation.PERIOD]

        third_person = [Pronoun.HE, Pronoun.SHE, Pronoun.IT, Noun('dog').definite()]
        not_third_person = [Pronoun.I, Pronoun.THEY, Pronoun.YOU, Pronoun.WE, Noun('dog').plural()]

        for subj in third_person:
            e_maker = ErrorMaker([[subj, go.third_person()] + after_verb], p_error=1.0)
            e_maker.create_is_do_errors()
            self.assertEqual(find_subject_special_case(e_maker.error_paragraph[0]), 0)

            e_maker = ErrorMaker([[subj, go.past_tense()] + after_verb], p_error=1.0)
            e_maker.create_is_do_errors()
            self.assertEqual(find_subject_special_case(e_maker.error_paragraph[0]), 0)

            e_maker = ErrorMaker([[Word('Every day'), Punctuation.COMMA, subj, go.third_person()] + after_verb],
                                 p_error=1.0)
            e_maker.create_is_do_errors()
            self.assertEqual(find_subject_special_case(e_maker.error_paragraph[0]), 2)

        for subj in not_third_person:
            e_maker = ErrorMaker([[subj, go] + after_verb], p_error=1.0)
            e_maker.create_is_do_errors()
            self.assertEqual(find_subject_special_case(e_maker.error_paragraph[0]), 0)

            e_maker = ErrorMaker([[subj, go.past_tense()] + after_verb], p_error=1.0)
            e_maker.create_is_do_errors()
            self.assertEqual(find_subject_special_case(e_maker.error_paragraph[0]), 0)

            e_maker = ErrorMaker([[Word('Every day'), Punctuation.COMMA, subj, go] + after_verb],
                                 p_error=1.0)
            e_maker.create_is_do_errors()
            self.assertEqual(find_subject_special_case(e_maker.error_paragraph[0]), 2)

    def test_find_subject_special_case_non_special_case(self):
        sentence = [Word('Yesterday'), Punctuation.COMMA, Noun('dog').definite(), Verb('play').past_tense()]
        self.assertEqual(find_subject_special_case(sentence), 2)

    def test_error_maker_create_all_errors_with_preposition_positive_and_negative_verbs(self):
        dog = Noun('dog')
        cat = Noun('cat')
        jump = Verb('jump')
        on = Preposition('on')
        paragraph = [
            [dog.indefinite().capitalize(), jump.third_person(), on, cat.plural(), Punctuation.EXCLAMATION],
            [dog.indefinite().capitalize(), jump.third_person().negative(), on, cat.plural(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        random.seed(456)
        error_maker.create_all_errors()
        error_paragraph = [
            [dog.plural().indefinite().capitalize(), on, cat.plural().indefinite(), Word('is jump'), Punctuation.COMMA],
            [dog.plural(), on, cat, Word('were not jump'), Punctuation.COMMA],
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize().bold(), jump.third_person().bold(), on.bold(),
             cat.plural().bold(), Punctuation.EXCLAMATION.bold()],
            [dog.indefinite().capitalize().bold(), jump.third_person().negative().bold(), on.bold(),
             cat.plural().bold(), Punctuation.EXCLAMATION.bold()]
        ]

        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)

    def test_error_count_and_reset(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        self.assertEqual(error_maker.error_count, 0)
        error_maker.create_all_errors()
        self.assertEqual(error_maker.error_count, 4)
        error_maker.reset()
        self.assertEqual(error_maker.error_count, 0)
        self.assertEqual(error_maker.error_paragraph, paragraph)

        error_maker.create_noun_errors()
        self.assertEqual(error_maker.error_count, 2)

    def test_already_has_error(self):
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_noun_errors()
        self.assertTrue(error_maker.already_has_error(0, 0))
        self.assertTrue(error_maker.already_has_error(0, 2))
        self.assertFalse(error_maker.already_has_error(0, 1))
        self.assertFalse(error_maker.already_has_error(0, 3))

    def test_error_count_does_not_count_same_verb_twice(self):
        random.seed(100)
        dog = Noun('dog')
        cat = Noun('cat')
        grab = Verb('grab')
        paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        error_maker.create_verb_errors()
        error_maker.create_is_do_errors()
        self.assertEqual(error_maker.error_paragraph[0][1], Word('was grab'))
        self.assertEqual(error_maker.error_count, 1)

    def test_regression_test_make_verb_error_make_is_do_error(self):
        random.seed(10)
        verb = Verb('go', 'went').negative().third_person()
        error = make_verb_error(verb, True)
        self.assertEqual(error, NegativePastVerb("didn't goes", 'went', 'go'))
        new_error = make_is_do_error(error, Word('is'))
        self.assertEqual(new_error, Word('was not go'))
