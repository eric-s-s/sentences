import random
import unittest

from sentences.alt_backend.new_grammarizer import NewGrammarizer
from sentences.tags.status_tag import StatusTag
from sentences.words.basicword import BasicWord
from sentences.words.punctuation import Punctuation

from sentences.alt_backend.new_error_maker import make_verb_error, make_noun_error, make_is_do_error, NewErrorMaker
from sentences.tags.tags import Tags
from sentences.tags.wordtag import WordTag
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.be_verb import BeVerb
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun
from sentences.words.verb import Verb


class TestNewErrorMaker(unittest.TestCase):

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
        self.assertEqual(make_is_do_error(verb, BeVerb.AM), [BeVerb.AM, Verb('go')])
        self.assertEqual(make_is_do_error(verb, BeVerb.ARE), [BeVerb.ARE, Verb('go')])
        self.assertEqual(make_is_do_error(verb.third_person(), BeVerb.IS), [BeVerb.IS, Verb('go')])

    def test_is_do_error_present_negative(self):
        verb = Verb('go').negative()
        self.assertEqual(make_is_do_error(verb, BeVerb.AM), [BeVerb.AM_NOT, Verb('go')])
        self.assertEqual(make_is_do_error(verb, BeVerb.ARE), [BeVerb.ARE_NOT, Verb('go')])
        self.assertEqual(make_is_do_error(verb.third_person(), BeVerb.IS), [BeVerb.IS_NOT, Verb('go')])

    def test_is_do_error_past_not_negative(self):
        verb = Verb('go', 'went', '').past_tense()
        self.assertEqual(make_is_do_error(verb, BeVerb.AM), [BeVerb.WAS, Verb('go', 'went', '')])
        self.assertEqual(make_is_do_error(verb, BeVerb.ARE), [BeVerb.WERE, Verb('go', 'went', '')])
        self.assertEqual(make_is_do_error(verb, BeVerb.IS), [BeVerb.WAS, Verb('go', 'went', '')])

    def test_is_do_error_past_negative(self):
        verb = Verb('go', 'went', '').negative().past_tense()
        self.assertEqual(make_is_do_error(verb, BeVerb.AM), [BeVerb.WAS_NOT, Verb('go', 'went', '')])
        self.assertEqual(make_is_do_error(verb, BeVerb.ARE), [BeVerb.WERE_NOT, Verb('go', 'went', '')])
        self.assertEqual(make_is_do_error(verb, BeVerb.IS), [BeVerb.WAS_NOT, Verb('go', 'went', '')])

    def test_error_maker_init(self):
        paragraph = Paragraph([Sentence([Noun('eskimo')])])
        error_maker = NewErrorMaker(paragraph, 1.0)
        self.assertEqual(error_maker.paragraph, paragraph)
        self.assertEqual(error_maker.p_error, 1.0)
        self.assertEqual(error_maker.error_paragraph, paragraph)

    def test_error_maker_method_order(self):
        error_maker = NewErrorMaker(Paragraph([]), 1.0)
        expected = [error_maker.create_noun_errors, error_maker.create_pronoun_errors,
                    error_maker.create_verb_errors, error_maker.create_is_do_errors,
                    error_maker.create_preposition_transpose_errors,
                    error_maker.create_period_errors]
        self.assertEqual(error_maker.method_order, expected)

    def test_error_maker_reset(self):
        sentences = [Sentence([Noun('roman').plural().capitalize(), Verb('go').third_person(),
                               Noun('house').definite()])]
        tags = Tags([StatusTag.GRAMMATICAL])
        paragraph = Paragraph(sentences, tags)
        error_maker = NewErrorMaker(paragraph, 1.0)
        for method in error_maker.method_order:
            method()
            error_maker.reset()
            self.assertEqual(error_maker.error_paragraph, paragraph)

    def test_error_maker_changes_tags(self):
        tags = Tags([StatusTag.GRAMMATICAL, StatusTag.HAS_PLURALS])
        paragraph = Paragraph([], tags)
        error_maker = NewErrorMaker(paragraph, 1.0)

        expected_tags = Tags([StatusTag.HAS_ERRORS, StatusTag.HAS_PLURALS])
        for method in error_maker.method_order:
            error_maker.reset()
            method()
            self.assertEqual(error_maker.paragraph.tags, tags)
            self.assertEqual(error_maker.error_paragraph.tags, expected_tags)

    def test_error_maker_make_noun_errors_p_error_zero(self):
        sentences = [Sentence([Noun('roman').plural().capitalize(), Verb('go'), BasicWord.preposition('to'),
                               Noun('house').definite(), Punctuation.EXCLAMATION])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph, 0.0)
        error_maker.create_noun_errors()
        error_tags = Tags([StatusTag.HAS_ERRORS])
        self.assertEqual(error_maker.paragraph, paragraph)
        self.assertEqual(error_maker.error_paragraph, Paragraph(sentences, error_tags))

    def test_error_maker_make_noun_errors_p_error_one(self):
        random.seed(34758)
        sentences = [Sentence([Noun('roman').plural().capitalize(), Verb('go'), BasicWord.preposition('to'),
                               Noun('house').definite(), Punctuation.EXCLAMATION])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph, 1.0)
        error_maker.create_noun_errors()

        expected_sentences = [Sentence([Noun('roman').definite().capitalize(), Verb('go'), BasicWord.preposition('to'),
                                        Noun('house'), Punctuation.EXCLAMATION])]
        error_tags = Tags([StatusTag.HAS_ERRORS])
        self.assertEqual(error_maker.paragraph, paragraph)
        self.assertEqual(error_maker.error_paragraph, Paragraph(expected_sentences, error_tags))

    def test_error_maker_make_noun_errors_p_error_between_one_and_zero(self):
        random.seed(48335)
        sentences = [Sentence([Noun('roman').plural().capitalize(), Verb('go'), BasicWord.preposition('to'),
                               Noun('house').definite(), Punctuation.EXCLAMATION])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph, 1.0)
        error_maker.create_noun_errors()

        expected_sentences = [Sentence([Noun('roman').definite().capitalize(), Verb('go'), BasicWord.preposition('to'),
                                        Noun('house'), Punctuation.EXCLAMATION])]
        error_tags = Tags([StatusTag.HAS_ERRORS])
        self.assertEqual(error_maker.paragraph, paragraph)
        print(error_maker.error_paragraph)
