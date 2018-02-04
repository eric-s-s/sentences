import random
import string
import unittest

from sentences.backend.grammarizer import normalize_probability, get_non_proper_nouns, Grammarizer

from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.new_word import NewNoun
from sentences.words.new_verb import NewVerb
from sentences.words.wordtools.wordtag import WordTag
from sentences.words.wordtools.tags import Tags


PERIOD = Punctuation.PERIOD
EXCLAMATION = Punctuation.EXCLAMATION


class TestGrammarizer(unittest.TestCase):

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

    def test_normalize_probability(self):
        self.assertEqual(normalize_probability(0.2), 0.2)
        self.assertEqual(normalize_probability(1), 1)
        self.assertEqual(normalize_probability(0), 0)
        self.assertEqual(normalize_probability(-1), 0)
        self.assertEqual(normalize_probability(1.2), 1.0)

    def test_get_non_proper_nouns_no_nouns(self):
        raw_paragraph = [
            [Pronoun.I, NewVerb('grab'), Pronoun.YOU, EXCLAMATION],
            [Pronoun.WE, NewVerb('cut', 'cut'), Pronoun.IT, PERIOD],
            [Pronoun.IT, NewVerb('have', 'had'), Pronoun.THEM, PERIOD]
        ]
        self.assertEqual(get_non_proper_nouns(raw_paragraph), [])

    def test_get_non_proper_nouns_proper_nouns(self):
        raw_paragraph = [
            [NewNoun.proper_noun('NASA'), NewVerb('grab'), NewNoun.proper_noun('Joe'), EXCLAMATION],
            [NewNoun.proper_noun('the Things', plural=True), NewVerb('cut', 'cut'), NewNoun.proper_noun('Bob'), PERIOD],
            [Pronoun.IT, NewVerb('have', 'had'), Pronoun.THEM, PERIOD]
        ]
        self.assertEqual(get_non_proper_nouns(raw_paragraph), [])

    def test_get_non_proper_nouns_with_nouns(self):
        paragraph = [
            [NewNoun('money'), NewVerb('grab'), NewNoun('tea'), EXCLAMATION],
            [NewNoun('tea'), NewVerb('ride', 'rode'), NewNoun('apple'), PERIOD],
            [NewNoun('apple'), NewVerb('surprise'), NewNoun('gold'), PERIOD],
            [NewNoun('gold'), NewVerb('cut', 'cut'), NewNoun.proper_noun('Joe'), PERIOD],
            [Pronoun.IT, NewVerb('have', 'had'), NewNoun('watch'), PERIOD]
        ]

        self.assertEqual(get_non_proper_nouns(paragraph),
                         [NewNoun('money'), NewNoun('tea'), NewNoun('apple'), NewNoun('gold'), NewNoun('watch')])

    def test_grammarizer_init_defaults_and_paragraph_is_copy(self):
        random.seed(5)

        paragraph = [
            [NewNoun.uncountable_noun('money'), NewVerb('grab'), NewNoun.uncountable_noun('tea'), EXCLAMATION],
            [Pronoun.IT, NewVerb('have', 'had', ''), NewNoun('watch'), PERIOD],
            [NewNoun.proper_noun('Bob'), NewVerb('drive'), NewNoun.proper_noun('Benzes', plural=True)]
        ]
        grammarizer = Grammarizer(paragraph)
        self.assertEqual(grammarizer._raw, paragraph)
        self.assertIsNot(grammarizer._raw, paragraph)
        self.assertIsNot(grammarizer._raw[0], paragraph[0])

        self.assertEqual(grammarizer.plural, 0.3)
        self.assertEqual(grammarizer.negative, 0.3)
        self.assertEqual(grammarizer.present_tense, True)
        noun_info = {
            NewNoun.uncountable_noun('tea'): {'plural': False, 'definite': False, 'countable': False},
            NewNoun('watch'): {'plural': False, 'definite': False, 'countable': True},
            NewNoun.uncountable_noun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(noun_info, grammarizer.noun_info)

    def test_grammarizer_init_set(self):
        paragraph = [[]]
        grammarizer = Grammarizer(paragraph, False, 0.5, 0.1)

        self.assertEqual(grammarizer.plural, 0.5)
        self.assertEqual(grammarizer.negative, 0.1)
        self.assertEqual(grammarizer.present_tense, False)
        noun_info = {}
        self.assertEqual(noun_info, grammarizer.noun_info)

    def test_grammarizer_init_normalizes_probability(self):
        paragraph = [[]]
        grammarizer = Grammarizer(paragraph, False, 10.0, -0.1)

        self.assertEqual(grammarizer.plural, 1.0)
        self.assertEqual(grammarizer.negative, 0.0)

    def test_grammarizer_setters_normalize_probability(self):
        paragraph = [[]]
        grammarizer = Grammarizer(paragraph)
        grammarizer.plural = 10
        grammarizer.negative = -10
        self.assertEqual(grammarizer.plural, 1.0)
        self.assertEqual(grammarizer.negative, 0.0)

        grammarizer.plural = 0.1
        grammarizer.negative = 0.2
        self.assertEqual(grammarizer.plural, 0.1)
        self.assertEqual(grammarizer.negative, 0.2)

    def test_grammarizer_noun_info_property_is_copy(self):
        paragraph = [
            [NewNoun('money'), NewVerb('grab'), NewNoun('tea'), EXCLAMATION],
            [Pronoun.IT, NewVerb('have', 'had'), NewNoun('watch'), PERIOD]
        ]
        grammarizer = Grammarizer(paragraph)
        info_1 = grammarizer.noun_info
        info_2 = grammarizer.noun_info
        self.assertEqual(info_1, info_2)
        self.assertIsNot(info_1, info_2)
        self.assertIsNot(info_1[NewNoun('money')], info_2[NewNoun('money')])

    def test_grammarizer_reset_definite_nouns(self):
        paragraph = [
            [NewNoun('money'), NewVerb('grab'), NewNoun('tea'), EXCLAMATION],
            [Pronoun.IT, NewVerb('have', 'had'), NewNoun('watch'), PERIOD]
        ]
        grammarizer = Grammarizer(paragraph)
        grammarizer.generate_paragraph()
        for noun_dict in grammarizer.noun_info.values():
            self.assertTrue(noun_dict['definite'])
        grammarizer.reset_definite_nouns()
        for noun_dict in grammarizer.noun_info.values():
            self.assertFalse(noun_dict['definite'])

    def test_grammarizer_set_nouns(self):
        paragraph = [
            [NewNoun.uncountable_noun('money'), NewVerb('grab'), NewNoun('witch'), EXCLAMATION],
            [NewNoun('witch'), NewVerb('play'), NewNoun('watch'), PERIOD]
        ]
        grammarizer = Grammarizer(paragraph, probability_plural_noun=0.5)

        random.seed(10)

        grammarizer.set_nouns()
        noun_info = {
            NewNoun('watch'): {'plural': True, 'definite': False, 'countable': True},
            NewNoun('witch'): {'plural': False, 'definite': False, 'countable': True},
            NewNoun.uncountable_noun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(grammarizer.noun_info, noun_info)

        grammarizer.set_nouns()
        noun_info = {
            NewNoun('watch'): {'plural': True, 'definite': False, 'countable': True},
            NewNoun('witch'): {'plural': False, 'definite': False, 'countable': True},
            NewNoun.uncountable_noun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(grammarizer.noun_info, noun_info)

        grammarizer.set_nouns()
        noun_info = {
            NewNoun('watch'): {'plural': False, 'definite': False, 'countable': True},
            NewNoun('witch'): {'plural': False, 'definite': False, 'countable': True},
            NewNoun.uncountable_noun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(grammarizer.noun_info, noun_info)

    def test_grammarizer_set_nouns_never_sets_uncountable_nouns_to_plural(self):
        paragraph = [
            [NewNoun.uncountable_noun('money'), NewVerb('grab'), NewNoun.uncountable_noun('tea'), EXCLAMATION],
            [NewNoun('witch'), NewVerb('have', 'had'), NewNoun('watch'), PERIOD]
        ]
        grammarizer = Grammarizer(paragraph, probability_plural_noun=1.0)
        grammarizer.set_nouns()
        noun_info = {
            NewNoun.uncountable_noun('tea'): {'plural': False, 'definite': False, 'countable': False},
            NewNoun('watch'): {'plural': True, 'definite': False, 'countable': True},
            NewNoun('witch'): {'plural': True, 'definite': False, 'countable': True},
            NewNoun.uncountable_noun('money'): {'plural': False, 'definite': False, 'countable': False},
        }

        self.assertEqual(grammarizer.noun_info, noun_info)

    def test_generate_paragraph_returns_sentences_with_capitals(self):
        paragraph = [
            [NewNoun('money'), NewVerb('grab'), NewNoun('tea'), EXCLAMATION],
            [NewNoun('tea'), NewVerb('ride', 'rode', ''), NewNoun('apple'), PERIOD],
            [NewNoun('apple'), NewVerb('surprise'), NewNoun('gold'), PERIOD],
            [NewNoun.proper_noun('the Dude'), NewVerb('cut', 'cut', ''), Pronoun.IT, PERIOD],
            [Pronoun.IT, NewVerb('have', 'had', ''), NewNoun('watch'), PERIOD]
        ]
        grammarizer = Grammarizer(paragraph)
        paragraph = grammarizer.generate_paragraph()
        for sentence in paragraph:
            self.assertIn(sentence[0].value[0], string.ascii_uppercase)

    def test_generate_paragraph_makes_nouns_indefinite_in_first_instance_and_definite_later(self):
        raw_paragraph = 5 * [
            [NewNoun('money'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
            [NewNoun('witch'), NewVerb('play'), NewNoun('dog'), PERIOD],
        ]
        grammarizer = Grammarizer(raw_paragraph)
        paragraph = grammarizer.generate_paragraph()
        self.assertEqual(len(paragraph), 10)
        indefinite_part = paragraph[:2]
        definite_part = paragraph[2:]
        for sentence in indefinite_part:
            for word in sentence:
                self.assertFalse(word.has_tags(WordTag.DEFINITE))

        for sentence in definite_part:
            for word in sentence:
                if isinstance(word, NewNoun):
                    self.assertTrue(word.has_tags(WordTag.DEFINITE))

    def test_generate_paragraph_singular_countable_noun(self):
        raw_paragraph = [[NewNoun('cat'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION]]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=0.0)
        paragraph = grammarizer.generate_paragraph()
        expected = [[
            NewNoun('A cat', '', 'cat', tags=self.indefinite), NewVerb('grabs', '', 'grab', tags=self.third_person),
            NewNoun('the cat', '', 'cat', tags=self.definite), EXCLAMATION
        ]]
        self.assertEqual(paragraph, expected)

    def test_generate_paragraph_plural_countable_noun(self):
        raw_paragraph = [[NewNoun('cat'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION]]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=1.0)
        paragraph = grammarizer.generate_paragraph()
        expected = [[NewNoun('Cats', '', 'cat', tags=self.plural), NewVerb('grab'),
                     NewNoun('the cats', '', 'cat', tags=self.definite_plural), EXCLAMATION]]
        self.assertEqual(paragraph, expected)

    def test_generate_paragraph_uncountable_noun(self):
        raw_paragraph = [
            [NewNoun.uncountable_noun('water'), NewVerb('grab'), NewNoun.uncountable_noun('water'), PERIOD]
        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=1.0)
        paragraph = grammarizer.generate_paragraph()
        expected = [[
            NewNoun('Water', '', 'water', tags=self.uncountable), NewVerb('grabs', '', 'grab', tags=self.third_person),
            NewNoun('the water', '', 'water', tags=self.definite_uncountable), PERIOD
        ]]
        self.assertEqual(paragraph, expected)

    def test_generate_paragraph_present_tense_third_person_positive(self):
        raw_paragraph = [
            [NewNoun.uncountable_noun('water'), NewVerb('grab'), NewNoun.uncountable_noun('water'), EXCLAMATION],
            [NewNoun('cat'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
            [NewNoun.proper_noun('Joe'), NewVerb('grab'), NewNoun.proper_noun('Bob')]
        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=0.0)
        paragraph = grammarizer.generate_paragraph()
        target_verb = NewVerb('grabs', '', 'grab', tags=self.third_person)
        for sentence in paragraph:
            self.assertEqual(sentence[1], target_verb)

    def test_generate_paragraph_present_tense_third_person_negative(self):
        raw_paragraph = [
            [NewNoun.uncountable_noun('water'), NewVerb('grab'), NewNoun.uncountable_noun('water'), EXCLAMATION],
            [NewNoun('cat'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
            [NewNoun.proper_noun('Joe'), NewVerb('grab'), NewNoun('cat')]
        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=1.0, probability_plural_noun=0.0)
        paragraph = grammarizer.generate_paragraph()
        target_verb = NewVerb("doesn't grab", '', 'grab', tags=self.negative_third_person)
        for sentence in paragraph:
            self.assertEqual(sentence[1], target_verb)

    def test_generate_paragraph_present_tense_not_third_person_positive(self):
        raw_paragraph = [[NewNoun('cat'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.I, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.YOU, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.WE, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.THEY, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [NewNoun.proper_noun('Taiwanese', plural=True), NewVerb('grab'), NewNoun('cat'), EXCLAMATION]
                         ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=1.0)
        paragraph = grammarizer.generate_paragraph()
        target_verb = NewVerb('grab')
        for sentence in paragraph:
            self.assertEqual(sentence[1], target_verb)

    def test_generate_paragraph_present_tense_not_third_person_negative(self):
        raw_paragraph = [[NewNoun('cat'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.I, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.YOU, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.WE, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.THEY, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [NewNoun.proper_noun('Taiwanese', plural=True), NewVerb('grab'), NewNoun('cat'), EXCLAMATION]
                         ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=1.0, probability_plural_noun=1.0)
        paragraph = grammarizer.generate_paragraph()
        target_verb = NewVerb("don't grab", '', 'grab', tags=self.negative)
        for sentence in paragraph:
            self.assertEqual(sentence[1], target_verb)

    def test_generate_paragraph_past_tense_positive(self):
        raw_paragraph = [[NewNoun.uncountable_noun('water'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [NewNoun('cat'), NewVerb('eat', 'ate', ''), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.I, NewVerb('sing', 'sang', ''), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.YOU, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.WE, NewVerb('sing', 'sang', ''), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.THEY, NewVerb('eat', 'ate', ''), NewNoun('cat'), EXCLAMATION],
                         ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0,
                                  probability_plural_noun=1.0, present_tense=False)
        paragraph = grammarizer.generate_paragraph()
        target_verbs = [NewVerb('grabbed', '', 'grab', tags=self.past), NewVerb('ate', 'ate', 'eat', tags=self.past),
                        NewVerb('sang', 'sang', 'sing', tags=self.past)]
        for sentence in paragraph:
            self.assertIn(sentence[1], target_verbs)

    def test_generate_paragraph_past_tense_negative(self):
        raw_paragraph = [[NewNoun.uncountable_noun('water'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [NewNoun('cat'), NewVerb('eat', 'ate'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.I, NewVerb('sing', 'sang'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.YOU, NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.WE, NewVerb('sing', 'sang'), NewNoun('cat'), EXCLAMATION],
                         [Pronoun.THEY, NewVerb('eat', 'ate'), NewNoun('cat'), EXCLAMATION],
                         ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=1.0,
                                  probability_plural_noun=1.0, present_tense=False)
        paragraph = grammarizer.generate_paragraph()
        target_verbs = [NewVerb("didn't grab", '', 'grab', tags=self.negative_past),
                        NewVerb("didn't eat", 'ate', 'eat', tags=self.negative_past),
                        NewVerb("didn't sing", 'sang', 'sing', tags=self.negative_past)]
        for sentence in paragraph:
            self.assertIn(sentence[1], target_verbs)

    def test_assign_negatives_all_negative(self):
        raw_paragraph = 5 * [
            [NewNoun.uncountable_noun('money'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
            [NewNoun('witch'), NewVerb('play'), NewNoun('dog'), PERIOD],

        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=1.0)
        paragraph = grammarizer.generate_paragraph()
        for sentence in paragraph:
            for word in sentence:
                if isinstance(word, NewVerb):
                    value = word.value
                    tests_true = value.startswith("don't ") or value.startswith("doesn't ")
                    self.assertTrue(tests_true)

    def test_assign_negatives_no_negative(self):
        raw_paragraph = 5 * [
            [NewNoun.uncountable_noun('money'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
            [NewNoun('witch'), NewVerb('play'), NewNoun('dog'), PERIOD],

        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0)
        paragraph = grammarizer.generate_paragraph()
        for sentence in paragraph:
            for word in sentence:
                if isinstance(word, NewVerb):
                    value = word.value
                    tests_false = value.startswith("don't ") or value.startswith("doesn't ")
                    self.assertFalse(tests_false)

    def test_assign_negatives_some_negative(self):
        random.seed(3)
        raw_paragraph = 10 * [
            [NewNoun.uncountable_noun('money'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.5)
        paragraph = grammarizer.generate_paragraph()
        negatives = [1, 4, 5, 7, 8]
        for index, sentence in enumerate(paragraph):
            for word in sentence:
                if isinstance(word, NewVerb):
                    value = word.value
                    is_negative = value.startswith("don't ") or value.startswith("doesn't ")
                    if index in negatives:
                        self.assertTrue(is_negative)
                    else:
                        self.assertFalse(is_negative)

    def test_generate_paragraph_multiple_times_resets_indefinte(self):
        raw_paragraph = [
            [NewNoun.uncountable_noun('money'), NewVerb('grab'), NewNoun.uncountable_noun('money'), EXCLAMATION],
            [NewNoun('cat'), NewVerb('grab'), NewNoun('cat'), EXCLAMATION],
        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=0.0)
        paragraph_1 = grammarizer.generate_paragraph()
        paragraph_2 = grammarizer.generate_paragraph()
        answer = [
            [NewNoun.uncountable_noun('money').capitalize(), NewVerb('grabs', '', 'grab', tags=self.third_person),
             NewNoun('the money', base='money', tags=self.definite_uncountable), EXCLAMATION],
            [NewNoun('A cat', base='cat', tags=self.indefinite), NewVerb('grabs', '', 'grab', tags=self.third_person),
             NewNoun('the cat', base='cat', tags=self.definite), EXCLAMATION]
        ]
        self.assertEqual(answer, paragraph_1)
        self.assertEqual(answer, paragraph_2)

    def test_proper_noun_and_plural_proper_noun_do_not_change_except_capitalize(self):
        raw_paragraph = [
            [NewNoun.proper_noun('Joe'), NewVerb('grab'), NewNoun.proper_noun('the Guys', plural=True), PERIOD],
            [NewNoun.proper_noun('the Guys', plural=True), NewVerb('grab'), NewNoun.proper_noun('Joe'), PERIOD],
        ]

        expected = [
            [NewNoun.proper_noun('Joe'), NewVerb('grabs', '', 'grab', tags=self.third_person),
             NewNoun.proper_noun('the Guys', plural=True), PERIOD],

            [NewNoun('The Guys', '', 'the Guys', tags=self.plural_proper),
             NewVerb('grab'), NewNoun.proper_noun('Joe'), PERIOD],
        ]
        for probility_plural in (0.0, 0.2, 0.5, 1.0):
            grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0,
                                      probability_plural_noun=probility_plural)
            answer = grammarizer.generate_paragraph()
            self.assertEqual(answer, expected)
