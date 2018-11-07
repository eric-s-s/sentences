import random
import unittest
from typing import List, Any

from sentences.backend.errormaker import (copy_paragraph, make_verb_error, make_noun_error,
                                          make_is_do_error, find_subject_special_case, ErrorMaker)
from sentences.words.noun import Noun
from sentences.words.punctuation import Punctuation
from sentences.words.pronoun import Pronoun, CapitalPronoun
from sentences.words.verb import Verb
from sentences.words.basicword import BasicWord
from sentences.tags.wordtag import WordTag
from sentences.tags.tags import Tags


class TestErrorMaker(unittest.TestCase):

    def setUp(self):
        self.indefinite = Tags([WordTag.INDEFINITE])
        self.definite = Tags([WordTag.DEFINITE])
        self.plural = Tags([WordTag.PLURAL])
        self.uncountable = Tags([WordTag.UNCOUNTABLE])
        self.definite_plural = Tags([WordTag.DEFINITE, WordTag.PLURAL])
        self.definite_uncountable = Tags([WordTag.DEFINITE, WordTag.UNCOUNTABLE])
        self.proper = Tags([WordTag.PROPER])
        self.plural_proper = Tags([WordTag.PLURAL, WordTag.PROPER])

        self.past = Tags([WordTag.PAST])
        self.third_person = Tags([WordTag.THIRD_PERSON])
        self.negative = Tags([WordTag.NEGATIVE])
        self.negative_past = Tags([WordTag.NEGATIVE, WordTag.PAST])
        self.negative_third_person = Tags([WordTag.NEGATIVE, WordTag.THIRD_PERSON])

    def test_make_verb_error_present_third_person(self):
        random.seed(6)
        verb = Verb('play').third_person()
        plus_ed = [2, 8]
        plus_ed_plus_s = [0, 7]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=True)
            if index in plus_ed:
                self.assertEqual(Verb('played', '', 'play', tags=self.past), to_test)
            elif index in plus_ed_plus_s:
                self.assertEqual(Verb('playeds', '', 'play', tags=self.past), to_test)
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
                self.assertEqual(Verb("didn't play", '', 'play', tags=self.negative_past), to_test)
            elif index in plus_ed_plus_s:
                self.assertEqual(Verb("didn't plays", '', "play", tags=self.negative_past), to_test)
            else:
                self.assertEqual(Verb('play').negative(), to_test)

    def test_make_verb_error_present_not_third_person(self):
        random.seed(6)
        verb = Verb('play')
        plus_ed = [1, 6]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=False)
            if index in plus_ed:
                self.assertEqual(Verb('played', '', 'play', tags=self.past), to_test)
            else:
                self.assertEqual(Verb('plays', '', 'play', tags=self.third_person), to_test)

    def test_make_verb_error_present_negative_not_third_person(self):
        random.seed(6)
        verb = Verb('play').negative()
        plus_ed = [1, 6]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=False)
            if index in plus_ed:
                self.assertEqual(Verb("didn't play", '', 'play', tags=self.negative_past), to_test)
            else:
                self.assertEqual(Verb("doesn't play", '', 'play', tags=self.negative_third_person), to_test)

    def test_make_verb_error_past_tense(self):
        random.seed(6)
        verb = Verb('play').past_tense()
        plus_s = [0, 3, 5, 6, 9]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=random.choice([True, False]))
            if index in plus_s:
                self.assertEqual(Verb('plays', '', 'play', tags=self.third_person), to_test)
            else:
                self.assertEqual(Verb('play'), to_test)

    def test_make_verb_error_negative_past_tense(self):
        random.seed(6)
        verb = Verb('play').negative().past_tense()
        plus_s = [0, 3, 5, 6, 9]
        for index in range(10):
            to_test = make_verb_error(verb, is_third_person_noun=random.choice([True, False]))
            if index in plus_s:
                self.assertEqual(Verb("doesn't play", '', 'play', tags=self.negative_third_person), to_test)
            else:
                self.assertEqual(Verb("don't play", '', 'play', tags=self.negative), to_test)

    def test_make_noun_error_proper_no_article(self):
        random.seed(191)
        noun = Noun.proper_noun('Joe')
        definite = [1, 2, 6, 7, 8, 9]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in definite:
                self.assertEqual(Noun('the Joe', '', 'Joe', tags=self.definite), to_test)
            else:
                self.assertEqual(Noun('a Joe', '', 'Joe', tags=self.indefinite), to_test)

    def test_make_noun_error_proper_with_article(self):
        random.seed(6541)
        noun = Noun.proper_noun('the Dude').capitalize()
        definite = [0, 1, 2, 7, 8, 9]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in definite:
                self.assertEqual(Noun('the the Dude', '', 'the Dude', tags=self.definite), to_test)
            else:
                self.assertEqual(Noun('a the Dude', '', 'the Dude', tags=self.indefinite), to_test)

    def test_make_noun_error_plural_proper(self):
        random.seed(69167)
        noun = Noun.proper_noun('Eds', plural=True).capitalize()
        definite = [1, 5, 8, 9]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in definite:
                self.assertEqual(Noun('the Eds', '', 'Eds', tags=self.definite_plural), to_test)
            else:
                self.assertEqual(Noun('an Eds', '', 'Eds', tags=self.indefinite), to_test)

    def test_make_noun_error_plural_proper_with_article(self):
        random.seed(2559)
        noun = Noun.proper_noun('the Joneses', plural=True).capitalize()
        definite = [0, 1, 2, 8]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in definite:
                self.assertEqual(Noun('the the Joneses', '', 'the Joneses', tags=self.definite_plural), to_test)
            else:
                self.assertEqual(Noun('a the Joneses', '', 'the Joneses', tags=self.indefinite), to_test)

    def test_make_noun_error_uncountable_not_definite(self):
        random.seed(10)
        noun = Noun.uncountable_noun('water')
        plural = [1, 2, 5, 6, 7]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in plural:
                self.assertEqual(Noun('waters', base='water', tags=self.plural), to_test)
            else:
                self.assertEqual(Noun('a water', base='water', tags=self.indefinite), to_test)

    def test_make_noun_error_uncountable_definite(self):
        random.seed(10)
        noun = Noun.uncountable_noun('water').definite()
        plural = [1, 2, 5, 6, 7]
        for index in range(10):
            to_test = make_noun_error(noun)
            if index in plural:
                self.assertEqual(Noun('waters', base='water', tags=self.plural), to_test)
            else:
                self.assertEqual(Noun('a water', base='water', tags=self.indefinite), to_test)

    def test_make_noun_error_plural_not_definite(self):
        random.seed(8)
        noun = Noun('toys', base='toy', tags=self.plural)
        indefinite = [2, 12]
        definite = [10]
        indefinite_plural = [5, 13]
        for index in range(15):
            to_test = make_noun_error(noun)
            if index in indefinite:
                self.assertEqual(Noun('a toy', base='toy', tags=self.indefinite), to_test)
            elif index in definite:
                self.assertEqual(Noun('the toy', base='toy', tags=self.definite), to_test)
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
                self.assertEqual(Noun('a toy', base='toy', tags=self.indefinite), to_test)
            elif index in definite:
                self.assertEqual(Noun('the toy', base='toy', tags=self.definite), to_test)
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
                self.assertEqual(Noun('toys', base='toy', tags=self.plural), to_test)
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
                self.assertEqual(Noun('a toy', base='toy', tags=self.indefinite), to_test)
            elif index in plural:
                self.assertEqual(Noun('toys', base='toy', tags=self.plural), to_test)
            elif index in indefinite_plural:
                self.assertEqual('a toys', to_test.value)
            else:
                self.assertEqual(Noun('toy'), to_test)

    def test_is_do_error_present_not_negative(self):
        verb = Verb('go')
        self.assertEqual(make_is_do_error(verb, BasicWord('am')), BasicWord('am go'))
        self.assertEqual(make_is_do_error(verb, BasicWord('are')), BasicWord('are go'))
        self.assertEqual(make_is_do_error(verb.third_person(), BasicWord('is')), BasicWord('is go'))

    def test_is_do_error_present_negative(self):
        verb = Verb('go').negative()
        self.assertEqual(make_is_do_error(verb, BasicWord('am')), BasicWord('am not go'))
        self.assertEqual(make_is_do_error(verb, BasicWord('are')), BasicWord('are not go'))
        self.assertEqual(make_is_do_error(verb.third_person(), BasicWord('is')), BasicWord('is not go'))

    def test_is_do_error_past_not_negative(self):
        verb = Verb('go', 'went', '').past_tense()
        self.assertEqual(make_is_do_error(verb, BasicWord('am')), BasicWord('was go'))
        self.assertEqual(make_is_do_error(verb, BasicWord('are')), BasicWord('were go'))
        self.assertEqual(make_is_do_error(verb, BasicWord('is')), BasicWord('was go'))

    def test_is_do_error_past_negative(self):
        verb = Verb('go', 'went', '').negative().past_tense()
        self.assertEqual(make_is_do_error(verb, BasicWord('am')), BasicWord('was not go'))
        self.assertEqual(make_is_do_error(verb, BasicWord('are')), BasicWord('were not go'))
        self.assertEqual(make_is_do_error(verb, BasicWord('is')), BasicWord('was not go'))

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
            [Noun('A cats', '', 'cat', tags=self.indefinite), grab, Noun('dog'), Punctuation.EXCLAMATION]
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
        joe = Noun.proper_noun('Joe')
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
            [dog.indefinite(), BasicWord('is grab'), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), BasicWord('are grab'), dog.definite(), Punctuation.EXCLAMATION]
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
            [dog.indefinite(), BasicWord('is grab'), cat.plural(), Punctuation.EXCLAMATION],
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
            [dog.indefinite(), BasicWord('was grab'), cat.plural(), Punctuation.EXCLAMATION],
            [cat.plural().definite(), BasicWord('were grab'), dog.definite(), Punctuation.EXCLAMATION]
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
            [dog.indefinite(), BasicWord('was grab'), cat.plural(), Punctuation.EXCLAMATION],
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
            (Pronoun.I, CapitalPronoun.I): BasicWord('am go'),
            (Pronoun.HE, Pronoun.SHE, Pronoun.IT,
             CapitalPronoun.HE, CapitalPronoun.SHE, CapitalPronoun.IT): BasicWord('is go'),
            (Pronoun.YOU, Pronoun.WE, Pronoun.THEY,
             CapitalPronoun.YOU, CapitalPronoun.WE, CapitalPronoun.THEY): BasicWord('are go')
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
            [Noun('the cats', '', 'cat', tags=self.definite_plural), grab, dog.definite(), Punctuation.COMMA]
        ]
        answer_paragraph = [
            [dog.indefinite().capitalize(), grab.third_person(), cat.plural(), Punctuation.EXCLAMATION.bold()],
            [cat.plural().definite().capitalize().bold(), grab, dog.definite(), Punctuation.EXCLAMATION.bold()]
        ]
        self.assertEqual(error_maker.error_paragraph, error_paragraph)
        self.assertEqual(error_maker.answer_paragraph, answer_paragraph)
        self.assertEqual(error_maker.error_count, 2)

    def test_error_maker_create_period_errors_does_not_bold_when_noun_is_unchanged(self):
        sox = Noun('the Sox')
        joe = Noun('Joe')
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
            [Noun('the cats', '', 'cat', tags=self.definite_plural), grab, dog.definite(), Punctuation.EXCLAMATION]
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
        on = BasicWord.preposition('on')
        hit = Verb('hit')
        with_ = BasicWord.preposition('with')

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
        on = BasicWord.preposition('on')
        hit = Verb('hit')
        with_ = BasicWord.preposition('with')
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
        with_ = BasicWord.preposition('with')
        paragraph = [
            [dog.indefinite().capitalize(), hit.third_person(), Pronoun.ME, with_, cat.plural(),
             Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        random.seed(1)
        error_maker.create_all_errors()
        error_paragraph = [
            [dog.capitalize(), BasicWord.preposition('with'), cat.indefinite(), BasicWord('was hit'), Pronoun.I,
             Punctuation.COMMA]
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

            e_maker = ErrorMaker([[BasicWord('Every day'), Punctuation.COMMA, subj, go.third_person()] + after_verb],
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

            e_maker = ErrorMaker([[BasicWord('Every day'), Punctuation.COMMA, subj, go] + after_verb],
                                 p_error=1.0)
            e_maker.create_is_do_errors()
            self.assertEqual(find_subject_special_case(e_maker.error_paragraph[0]), 2)

    def test_find_subject_special_case_non_special_case(self):
        sentence = [BasicWord('Yesterday'), Punctuation.COMMA, Noun('dog').definite(), Verb('play').past_tense()]
        self.assertEqual(find_subject_special_case(sentence), 2)

    def test_error_maker_create_all_errors_with_preposition_positive_and_negative_verbs(self):
        dog = Noun('dog')
        cat = Noun('cat')
        jump = Verb('jump')
        on = BasicWord.preposition('on')
        paragraph = [
            [dog.indefinite().capitalize(), jump.third_person(), on, cat.plural(), Punctuation.EXCLAMATION],
            [dog.indefinite().capitalize(), jump.third_person().negative(), on, cat.plural(), Punctuation.EXCLAMATION]
        ]
        error_maker = ErrorMaker(paragraph, p_error=1.0)
        random.seed(456)
        error_maker.create_all_errors()
        error_paragraph = [
            [dog.plural().indefinite().capitalize(), on, cat.plural().indefinite(), BasicWord('is jump'),
             Punctuation.COMMA],
            [dog.plural(), on, cat, BasicWord('were not jump'), Punctuation.COMMA],
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
        self.assertEqual(error_maker.error_paragraph[0][1], BasicWord('was grab'))
        self.assertEqual(error_maker.error_count, 1)

    def test_regression_test_make_verb_error_make_is_do_error(self):
        random.seed(10)
        verb = Verb('go', 'went').negative().third_person()
        error = make_verb_error(verb, True)
        self.assertEqual(error, Verb("didn't goes", 'went', 'go', tags=self.negative_past))
        new_error = make_is_do_error(error, BasicWord('is'))
        self.assertEqual(new_error, BasicWord('was not go'))
