import random
import unittest

from sentences.alt_backend.new_error_maker import make_verb_error, make_noun_error, NewErrorMaker, get_be_verb
from sentences.tags.status_tag import StatusTag
from sentences.tags.tags import Tags
from sentences.tags.wordtag import WordTag
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.be_verb import BeVerb
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun, CapitalPronoun
from sentences.words.punctuation import Punctuation
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
            to_test = make_verb_error(verb)
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
            to_test = make_verb_error(verb)
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
            to_test = make_verb_error(verb)
            if index in plus_ed:
                self.assertEqual(Verb('played', '', 'play', tags=self.past), to_test)
            else:
                self.assertEqual(Verb('plays', '', 'play', tags=self.third_person), to_test)

    def test_make_verb_error_present_negative_not_third_person(self):
        random.seed(6)
        verb = Verb('play').negative()
        plus_ed = [1, 6]
        for index in range(10):
            to_test = make_verb_error(verb)
            if index in plus_ed:
                self.assertEqual(Verb("didn't play", '', 'play', tags=self.negative_past), to_test)
            else:
                self.assertEqual(Verb("doesn't play", '', 'play', tags=self.negative_third_person), to_test)

    def test_make_verb_error_past_tense(self):
        random.seed(6)
        verb = Verb('play').past_tense()
        plus_s = [1, 2, 6, 7, 8]
        for index in range(10):
            to_test = make_verb_error(verb)
            if index in plus_s:
                self.assertEqual(Verb('plays', '', 'play', tags=self.third_person), to_test)
            else:
                self.assertEqual(Verb('play'), to_test)

    def test_make_verb_error_negative_past_tense(self):
        random.seed(6)
        verb = Verb('play').negative().past_tense()
        plus_s = [1, 2, 6, 7, 8]
        for index in range(10):
            to_test = make_verb_error(verb)
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

    def test_get_be_verb_no_subject(self):
        sentence = Sentence([Verb('go')])
        self.assertEqual(get_be_verb(sentence), BeVerb.BE)

    def test_get_be_verb_no_verb(self):
        sentence = Sentence([Noun('cat')])
        self.assertEqual(get_be_verb(sentence), BeVerb.BE)

    def test_get_be_verb_verb_is_be_verb(self):
        sentence = Sentence([Pronoun.HE, BeVerb.AM, Verb('is')])
        self.assertEqual(get_be_verb(sentence), BeVerb.AM)

    def test_get_be_verb_present_tense_I(self):
        first_person = [Pronoun.I, Pronoun.ME, CapitalPronoun.I, CapitalPronoun.ME]
        for subj in first_person:
            sentence = Sentence([subj, Verb('go')])
            self.assertEqual(get_be_verb(sentence), BeVerb.AM)

            sentence = Sentence([subj, Verb('go').negative()])
            self.assertEqual(get_be_verb(sentence), BeVerb.AM_NOT)

    def test_get_be_verb_present_tense_singular_subject(self):
        singular_subj = [
            Noun('cat').definite(), Noun('cat').indefinite(), Noun.uncountable_noun('water'), Noun.proper_noun('Joe'),
            Pronoun.HE, Pronoun.HIM, Pronoun.SHE, Pronoun.HER, Pronoun.IT,
            CapitalPronoun.HE, CapitalPronoun.HIM, CapitalPronoun.SHE, CapitalPronoun.HER, CapitalPronoun.IT
        ]
        for subj in singular_subj:
            sentence = Sentence([subj, Verb('go')])
            self.assertEqual(get_be_verb(sentence), BeVerb.IS)

            sentence = Sentence([subj, Verb('go').negative()])
            self.assertEqual(get_be_verb(sentence), BeVerb.IS_NOT)

    def test_get_be_verb_present_tense_plural_subject(self):
        plural_subj = [
            Noun('cat').plural(), Noun.proper_noun('the Joes', plural=True), Pronoun.YOU, CapitalPronoun.YOU,
            Pronoun.WE, Pronoun.US, CapitalPronoun.WE, CapitalPronoun.US,
            Pronoun.THEY, Pronoun.THEM, CapitalPronoun.THEY, CapitalPronoun.THEM
        ]
        for subj in plural_subj:
            sentence = Sentence([subj, Verb('go')])
            self.assertEqual(get_be_verb(sentence), BeVerb.ARE)

            sentence = Sentence([subj, Verb('go').negative()])
            self.assertEqual(get_be_verb(sentence), BeVerb.ARE_NOT)

    def test_get_be_verb_past_tense_singular_subject(self):
        singular_subj = [
            Noun('cat').definite(), Noun('cat').indefinite(), Noun.uncountable_noun('water'), Noun.proper_noun('Joe'),
            Pronoun.HE, Pronoun.HIM, Pronoun.SHE, Pronoun.HER, Pronoun.IT,
            CapitalPronoun.HE, CapitalPronoun.HIM, CapitalPronoun.SHE, CapitalPronoun.HER, CapitalPronoun.IT,
            Pronoun.I, Pronoun.ME, CapitalPronoun.I, CapitalPronoun.ME
        ]
        for subj in singular_subj:
            sentence = Sentence([subj, Verb('go').past_tense()])
            self.assertEqual(get_be_verb(sentence), BeVerb.WAS)

            sentence = Sentence([subj, Verb('go').negative().past_tense()])
            self.assertEqual(get_be_verb(sentence), BeVerb.WAS_NOT)

    def test_get_be_verb_past_tense_plural_subject(self):
        plural_subj = [
            Noun('cat').plural(), Noun.proper_noun('the Joes', plural=True), Pronoun.YOU, CapitalPronoun.YOU,
            Pronoun.WE, Pronoun.US, CapitalPronoun.WE, CapitalPronoun.US,
            Pronoun.THEY, Pronoun.THEM, CapitalPronoun.THEY, CapitalPronoun.THEM
        ]
        for subj in plural_subj:
            sentence = Sentence([subj, Verb('go').past_tense()])
            self.assertEqual(get_be_verb(sentence), BeVerb.WERE)

            sentence = Sentence([subj, Verb('go').negative().past_tense()])
            self.assertEqual(get_be_verb(sentence), BeVerb.WERE_NOT)

    def test_error_maker_init(self):
        paragraph = Paragraph([Sentence([Noun('eskimo')])])
        error_maker = NewErrorMaker(paragraph)
        self.assertEqual(error_maker.get_paragraph(), paragraph)

    def test_error_maker_empty_paragraph(self):
        paragraph = Paragraph([])
        error_maker = NewErrorMaker(paragraph)

        self.assertEqual(error_maker.noun_errors(1.0).get_paragraph().sentence_list(), [])
        self.assertEqual(error_maker.pronoun_errors(1.0).get_paragraph().sentence_list(), [])
        self.assertEqual(error_maker.verb_errors(1.0).get_paragraph().sentence_list(), [])
        self.assertEqual(error_maker.is_do_errors(1.0).get_paragraph().sentence_list(), [])
        self.assertEqual(error_maker.preposition_errors(1.0).get_paragraph().sentence_list(), [])
        self.assertEqual(error_maker.punctuation_errors(1.0).get_paragraph().sentence_list(), [])

    def test_error_maker_noun_errors_changes_tags(self):
        paragraph = Paragraph([], Tags([StatusTag.GRAMMATICAL, StatusTag.PRONOUN_ERRORS]))
        new_error_maker = NewErrorMaker(paragraph).noun_errors(0.5)
        self.assertEqual(new_error_maker.get_paragraph().tags,
                         paragraph.tags.add(StatusTag.NOUN_ERRORS).remove(StatusTag.GRAMMATICAL))

    def test_error_maker_noun_errors_retains_capital_letters_in_first_word(self):
        sentences = [Sentence([Noun('A'), Noun('b')]),
                     Sentence([Noun('d'), Noun('e')]),
                     Sentence([Noun('F'), Noun('g')])]
        error_maker = NewErrorMaker(Paragraph(sentences))
        error_pargraph = error_maker.noun_errors(1.0).get_paragraph()
        capitals = [0, 2]
        for index, sentence in enumerate(error_pargraph):
            first_word = sentence.get(0)
            if index in capitals:
                self.assertEqual(first_word.capitalize(), first_word)
            else:
                self.assertNotEqual(first_word.capitalize(), first_word)

    def test_error_maker_noun_errors_p_error_lte_zero(self):
        sentences = [Sentence([Noun('a'), Noun('b').plural(), Noun.uncountable_noun('c'), Noun.proper_noun('e')])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.noun_errors(0.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

        error_paragraph = error_maker.noun_errors(-1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_noun_errors_p_error_gte_one(self):
        random.seed(4758)
        sentences = [Sentence([Noun('a').definite(), Noun.proper_noun('C')]),
                     Sentence([Noun('d').indefinite(), Noun('e').plural()]),
                     Sentence([Noun.uncountable_noun('f')])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.noun_errors(1.0).get_paragraph()
        expected = [Sentence([Noun('a').indefinite(), Noun.proper_noun('C').indefinite()]),
                    Sentence([Noun('d'), Noun('e').indefinite()]),
                    Sentence([Noun.uncountable_noun('f').indefinite()])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

        error_paragraph = error_maker.noun_errors(1.1).get_paragraph()
        expected = [Sentence([Noun('a'), Noun.proper_noun('C').definite()]),
                    Sentence([Noun('d'), Noun('e').indefinite()]),
                    Sentence([Noun.uncountable_noun('f').plural()])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_noun_error_p_error_middle(self):
        random.seed(475456)
        sentences = [Sentence([Noun('a').definite(), Noun.proper_noun('C')]),
                     Sentence([Noun('d').indefinite(), Noun('e').plural()])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.noun_errors(0.5).get_paragraph()
        expected = [sentences[0],
                    Sentence([Noun('d'), Noun('e').plural().indefinite()])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_noun_error_does_not_affect_others(self):
        sentences = [Sentence([BasicWord.preposition('a'), Verb('a'), Pronoun.HIM,
                               CapitalPronoun.ME, Punctuation.COMMA, BeVerb.AM])]
        error_maker = NewErrorMaker(Paragraph(sentences))

        error_paragraph = error_maker.noun_errors(1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_pronoun_errors_changes_tags(self):
        paragraph = Paragraph([], Tags([StatusTag.GRAMMATICAL, StatusTag.NOUN_ERRORS]))
        new_error_maker = NewErrorMaker(paragraph).pronoun_errors(0.5)
        self.assertEqual(new_error_maker.get_paragraph().tags,
                         paragraph.tags.add(StatusTag.PRONOUN_ERRORS).remove(StatusTag.GRAMMATICAL))

    def test_error_maker_pronoun_errors_retains_capital_letters_in_first_word(self):
        sentences = [Sentence([CapitalPronoun.I, Pronoun.ME]),
                     Sentence([Pronoun.HIM, Pronoun.HE]),
                     Sentence([CapitalPronoun.HER, Pronoun.THEY])]
        error_maker = NewErrorMaker(Paragraph(sentences))
        error_pargraph = error_maker.pronoun_errors(1.0).get_paragraph()
        capitals = [0, 2]
        for index, sentence in enumerate(error_pargraph):
            first_word = sentence.get(0)
            if index in capitals:
                self.assertEqual(first_word.capitalize(), first_word)
            else:
                self.assertNotEqual(first_word.capitalize(), first_word)

    def test_error_maker_pronoun_errors_p_error_lte_zero(self):
        sentences = [Sentence([Pronoun.HE, Pronoun.THEY, Pronoun.ME, Pronoun.YOU])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.pronoun_errors(0.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

        error_paragraph = error_maker.pronoun_errors(-1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_pronoun_errors_p_error_gte_one(self):
        sentences = [Sentence([Pronoun.I, Pronoun.ME,
                               Pronoun.YOU,
                               Pronoun.HE, Pronoun.HIM,
                               Pronoun.SHE, Pronoun.HER,
                               Pronoun.IT,
                               Pronoun.WE, Pronoun.US,
                               Pronoun.THEY, Pronoun.THEM]),
                     Sentence([CapitalPronoun.I, Pronoun.ME,
                               CapitalPronoun.YOU,
                               CapitalPronoun.HE, Pronoun.HIM,
                               CapitalPronoun.SHE, Pronoun.HER,
                               CapitalPronoun.IT,
                               CapitalPronoun.WE, Pronoun.US,
                               CapitalPronoun.THEY, Pronoun.THEM])]
        expected = [Sentence([Pronoun.ME, Pronoun.I,
                              Pronoun.YOU,
                              Pronoun.HIM, Pronoun.HE,
                              Pronoun.HER, Pronoun.SHE,
                              Pronoun.IT,
                              Pronoun.US, Pronoun.WE,
                              Pronoun.THEM, Pronoun.THEY]),
                    Sentence([CapitalPronoun.ME, Pronoun.I,
                              CapitalPronoun.YOU,
                              CapitalPronoun.HIM, Pronoun.HE,
                              CapitalPronoun.HER, Pronoun.SHE,
                              CapitalPronoun.IT,
                              CapitalPronoun.US, Pronoun.WE,
                              CapitalPronoun.THEM, Pronoun.THEY])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.pronoun_errors(1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), expected)

        error_paragraph = error_maker.pronoun_errors(1.1).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_pronoun_error_p_error_middle(self):
        random.seed(47534)
        sentences = [Sentence([Pronoun.I, Pronoun.HE]),
                     Sentence([Pronoun.US, Pronoun.THEM])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.pronoun_errors(0.5).get_paragraph()
        expected = [Sentence([Pronoun.ME, Pronoun.HE]),
                    Sentence([Pronoun.US, Pronoun.THEY])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_pronoun_error_does_not_affect_others(self):
        sentences = [Sentence([BasicWord.preposition('a'), Verb('a'), Noun('a'), Punctuation.COMMA, BeVerb.AM])]
        error_maker = NewErrorMaker(Paragraph(sentences))

        error_paragraph = error_maker.pronoun_errors(1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_verb_errors_changes_tags(self):
        paragraph = Paragraph([], Tags([StatusTag.GRAMMATICAL, StatusTag.PRONOUN_ERRORS]))
        new_error_maker = NewErrorMaker(paragraph).verb_errors(0.5)
        self.assertEqual(new_error_maker.get_paragraph().tags,
                         paragraph.tags.add(StatusTag.VERB_ERRORS).remove(StatusTag.GRAMMATICAL))

    def test_error_maker_verb_errors_retains_capital_letters_in_first_word(self):
        sentences = [Sentence([Verb('A'), Verb('b')]),
                     Sentence([Verb('d'), Verb('e')]),
                     Sentence([Verb('F'), Verb('g')])]
        error_maker = NewErrorMaker(Paragraph(sentences))
        error_pargraph = error_maker.pronoun_errors(1.0).get_paragraph()
        capitals = [0, 2]
        for index, sentence in enumerate(error_pargraph):
            first_word = sentence.get(0)
            if index in capitals:
                self.assertEqual(first_word.capitalize(), first_word)
            else:
                self.assertNotEqual(first_word.capitalize(), first_word)

    def test_error_maker_verb_errors_p_error_lte_zero(self):
        sentences = [Sentence([Verb('play'), Verb('like').third_person()]),
                     Sentence([Verb('cry').negative(), Verb('dry').negative().third_person()]),
                     Sentence([Verb('pry').past_tense(), Verb('fry').negative().past_tense()])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.verb_errors(0.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

        error_paragraph = error_maker.verb_errors(-1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_verb_errors_p_error_gte_one(self):
        random.seed(4758)
        sentences = [Sentence([Verb('play'), Verb('like').third_person()]),
                     Sentence([Verb('cry').negative(), Verb('dry').negative().third_person()]),
                     Sentence([Verb('pry').past_tense(), Verb('fry').negative().past_tense()])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.verb_errors(1.0).get_paragraph()
        expected = [Sentence([Verb('play').past_tense(), Verb('like')]),
                    Sentence([Verb('cry').negative().third_person(), Verb('dry').negative().past_tense()]),
                    Sentence([Verb('pry'), Verb('fry').negative()])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

        error_paragraph = error_maker.verb_errors(1.1).get_paragraph()
        expected = [Sentence([Verb('play').past_tense(), Verb('like')]),
                    Sentence([Verb('cry').negative().past_tense(), Verb('dry').negative()]),
                    Sentence([Verb('pry').third_person(), Verb('fry').negative()])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_verb_errors_p_error_middle_value(self):
        random.seed(4758)
        sentences = [Sentence([Verb('play'), Verb('like').third_person()]),
                     Sentence([Verb('cry').negative(), Verb('dry').negative().third_person()]),
                     Sentence([Verb('pry').past_tense(), Verb('fry').negative().past_tense()])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.verb_errors(0.5).get_paragraph()
        expected = [Sentence([Verb('play'), Verb('like').past_tense()]),
                    Sentence([Verb('cry').negative(), Verb('dry').negative().third_person()]),
                    Sentence([Verb('pry'), Verb('fry').negative()])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_verb_error_does_not_affect_others(self):
        sentences = [Sentence([BasicWord.preposition('a'), Noun('a'), BeVerb.AM,
                               Pronoun.HIM, CapitalPronoun.ME, Punctuation.COMMA])]
        error_maker = NewErrorMaker(Paragraph(sentences))

        error_paragraph = error_maker.verb_errors(1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_is_do_errors_changes_tags(self):
        paragraph = Paragraph([], Tags([StatusTag.GRAMMATICAL, StatusTag.PRONOUN_ERRORS]))
        new_error_maker = NewErrorMaker(paragraph).is_do_errors(0.5)
        self.assertEqual(new_error_maker.get_paragraph().tags,
                         paragraph.tags.add(StatusTag.IS_DO_ERRORS).remove(StatusTag.GRAMMATICAL))

    def test_error_maker_is_do_errors_retains_capital_letters_in_first_word(self):
        sentences = [Sentence([Verb('A'), Verb('b')]),
                     Sentence([Verb('d'), Verb('e')]),
                     Sentence([Verb('F'), Verb('g')]),
                     Sentence([CapitalPronoun.HE, Verb('go')])]
        error_maker = NewErrorMaker(Paragraph(sentences))
        error_pargraph = error_maker.pronoun_errors(1.0).get_paragraph()
        capitals = [0, 2, 3]
        for index, sentence in enumerate(error_pargraph):
            first_word = sentence.get(0)
            if index in capitals:
                self.assertEqual(first_word.capitalize(), first_word)
            else:
                self.assertNotEqual(first_word.capitalize(), first_word)

    def test_error_maker_is_do_errors_p_error_lte_zero(self):
        sentences = [Sentence([Pronoun.HE, Verb('play').third_person()]),
                     Sentence([Verb('stop')]),
                     Sentence([Pronoun.I, Verb('go').negative()]),
                     Sentence([Pronoun.THEY, Verb('go').past_tense()]),
                     Sentence([Pronoun.HIM, Verb('go').past_tense().negative()])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.is_do_errors(0.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

        error_paragraph = error_maker.is_do_errors(-1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_is_do_errors_p_error_gte_one(self):
        random.seed(4758)
        sentences = [Sentence([Pronoun.HE, Verb('play').third_person()]),
                     Sentence([Verb('stop')]),
                     Sentence([Pronoun.I, Verb('go').negative()]),
                     Sentence([Pronoun.THEY, Verb('go').past_tense()]),
                     Sentence([Pronoun.HIM, Verb('go').past_tense().negative()])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.is_do_errors(1.0).get_paragraph()
        expected = [Sentence([Pronoun.HE, BeVerb.IS, Verb('play')]),
                    Sentence([BeVerb.BE, Verb('stop')]),
                    Sentence([Pronoun.I, BeVerb.AM_NOT, Verb('go')]),
                    Sentence([Pronoun.THEY, BeVerb.WERE, Verb('go')]),
                    Sentence([Pronoun.HIM, BeVerb.WAS_NOT, Verb('go')])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_is_do_errors_p_error_middle_value(self):
        random.seed(5812)
        sentences = [Sentence([Pronoun.I, Verb('go')]),
                     Sentence([Pronoun.YOU, Verb('go')]),
                     Sentence([Pronoun.HE, Verb('go')]),
                     Sentence([Pronoun.WE, Verb('go')])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.is_do_errors(0.5).get_paragraph()
        expected = [Sentence([Pronoun.I, Verb('go')]),
                    Sentence([Pronoun.YOU, BeVerb.ARE, Verb('go')]),
                    Sentence([Pronoun.HE, BeVerb.IS, Verb('go')]),
                    Sentence([Pronoun.WE, Verb('go')])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_is_do_error_does_not_affect_others(self):
        sentences = [Sentence([BasicWord.preposition('a'), Noun('a'), BeVerb.AM,
                               Pronoun.HIM, CapitalPronoun.ME, Punctuation.COMMA])]
        error_maker = NewErrorMaker(Paragraph(sentences))

        error_paragraph = error_maker.is_do_errors(1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_preposition_errors_changes_tags(self):
        paragraph = Paragraph([], Tags([StatusTag.GRAMMATICAL, StatusTag.PRONOUN_ERRORS]))
        new_error_maker = NewErrorMaker(paragraph).preposition_errors(0.5)
        self.assertEqual(new_error_maker.get_paragraph().tags,
                         paragraph.tags.add(StatusTag.PREPOSITION_ERRORS).remove(StatusTag.GRAMMATICAL))

    def test_error_maker_preposition_errors_retains_capital_letters_in_first_word(self):
        sentences = [Sentence([Verb('Go'), BasicWord.preposition('with'), Pronoun.HIM]),
                     Sentence([Verb('go'), BasicWord.preposition('with'), Pronoun.HIM]),
                     Sentence([Verb('Eat'), BasicWord.preposition('at'), Noun("Joe's")])]
        error_maker = NewErrorMaker(Paragraph(sentences))
        error_pargraph = error_maker.pronoun_errors(1.0).get_paragraph()
        capitals = [0, 2, 3]
        for index, sentence in enumerate(error_pargraph):
            first_word = sentence.get(0)
            if index in capitals:
                self.assertEqual(first_word.capitalize(), first_word)
            else:
                self.assertNotEqual(first_word.capitalize(), first_word)

    def test_error_maker_preposition_errors_p_error_lte_zero(self):
        sentences = [Sentence([Pronoun.I, Verb('go'), BasicWord.preposition('with'), Pronoun.HIM]),
                     Sentence([Pronoun.HE, Verb('run'), BasicWord.preposition('over'), Pronoun.IT])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.preposition_errors(0.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

        error_paragraph = error_maker.preposition_errors(-1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_preposition_errors_p_error_gte_one(self):
        sentences = [Sentence([Pronoun.I, Verb('go'), BasicWord.preposition('with'), Pronoun.HIM, Punctuation.PERIOD]),
                     Sentence([Pronoun.HE, Verb('run'), BasicWord.preposition('over'), Pronoun.IT, Punctuation.PERIOD])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.preposition_errors(1.0).get_paragraph()
        expected = [Sentence([Pronoun.I, BasicWord.preposition('with'), Pronoun.HIM, Verb('go'), Punctuation.PERIOD]),
                    Sentence([Pronoun.HE, BasicWord.preposition('over'), Pronoun.IT, Verb('run'), Punctuation.PERIOD])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_preposition_errors_complex_case(self):
        sentence = Sentence([Pronoun.I, Verb('pick'), Pronoun.IT, BasicWord.particle('up'),
                             BasicWord.preposition('with'), Noun('toe').indefinite(), Punctuation.PERIOD])
        expected = Sentence([Pronoun.I, BasicWord.preposition('with'), Noun('toe').indefinite(),
                             Verb('pick'), Pronoun.IT, BasicWord.particle('up'), Punctuation.PERIOD])
        error_paragraph = NewErrorMaker(Paragraph([sentence])).preposition_errors(1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), [expected])

    def test_error_maker_preposition_errors_p_error_middle_value(self):
        random.seed(5812)
        sentences = [Sentence([Verb('go'), BasicWord.preposition('with'), Pronoun.ME]),
                     Sentence([Verb('go'), BasicWord.preposition('over'), BasicWord('there')]),
                     Sentence([Verb('go'), BasicWord.preposition('into'), Pronoun.IT]),
                     Sentence([Verb('go'), BasicWord.preposition('under'), BasicWord('that')])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.preposition_errors(0.5).get_paragraph()
        expected = [Sentence([Verb('go'), BasicWord.preposition('with'), Pronoun.ME]),
                    Sentence([BasicWord.preposition('over'), BasicWord('there'), Verb('go')]),
                    Sentence([BasicWord.preposition('into'), Pronoun.IT, Verb('go')]),
                    Sentence([Verb('go'), BasicWord.preposition('under'), BasicWord('that')])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_preposition_error_does_not_affect_others(self):
        sentences = [Sentence([Verb('a'), Noun('a'), BeVerb.AM,
                               Pronoun.HIM, CapitalPronoun.ME, Punctuation.COMMA])]
        error_maker = NewErrorMaker(Paragraph(sentences))

        error_paragraph = error_maker.preposition_errors(1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_punctuation_errors_changes_tags(self):
        paragraph = Paragraph([], Tags([StatusTag.GRAMMATICAL, StatusTag.PRONOUN_ERRORS]))
        new_error_maker = NewErrorMaker(paragraph).punctuation_errors(0.5)
        self.assertEqual(new_error_maker.get_paragraph().tags,
                         paragraph.tags.add(StatusTag.PUNCTUATION_ERRORS).remove(StatusTag.GRAMMATICAL))

    def test_error_maker_punctuation_errors_p_error_lte_zero(self):
        sentences = [Sentence([CapitalPronoun.I, Verb('go'), Pronoun.HIM, Punctuation.PERIOD]),
                     Sentence([CapitalPronoun.HE, Verb('run'), Pronoun.IT, Punctuation.EXCLAMATION])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.punctuation_errors(0.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

        error_paragraph = error_maker.punctuation_errors(-1.0).get_paragraph()
        self.assertEqual(error_paragraph.sentence_list(), sentences)

    def test_error_maker_punctuation_errors_p_error_gte_one(self):
        sentences = [Sentence([CapitalPronoun.I, Verb('go'), Pronoun.HIM, Punctuation.PERIOD]),
                     Sentence([CapitalPronoun.HE, Verb('run'), Pronoun.IT, Punctuation.EXCLAMATION])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.punctuation_errors(1.0).get_paragraph()
        expected = [Sentence([CapitalPronoun.I, Verb('go'), Pronoun.HIM, Punctuation.COMMA]),
                    Sentence([Pronoun.HE, Verb('run'), Pronoun.IT, Punctuation.COMMA])]
        self.assertEqual(error_paragraph.sentence_list(), expected)

    def test_error_maker_punctuation_errors_p_error_middle_value(self):
        random.seed(5812)
        sentences = [Sentence([CapitalPronoun.I, Verb('go'), Punctuation.PERIOD]),
                     Sentence([CapitalPronoun.HE, Verb('run'), Punctuation.EXCLAMATION]),
                     Sentence([Noun('dog').definite().capitalize(), Punctuation.PERIOD]),
                     Sentence([BasicWord('A'), Punctuation.PERIOD])]
        paragraph = Paragraph(sentences)
        error_maker = NewErrorMaker(paragraph)

        error_paragraph = error_maker.punctuation_errors(0.5).get_paragraph()

        expected = [Sentence([CapitalPronoun.I, Verb('go'), Punctuation.PERIOD]),
                    Sentence([CapitalPronoun.HE, Verb('run'), Punctuation.COMMA]),
                    Sentence([Noun('dog').definite(), Punctuation.COMMA]),
                    Sentence([BasicWord('a'), Punctuation.PERIOD])]
        self.assertEqual(error_paragraph.sentence_list(), expected)
