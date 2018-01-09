import random
import string
import unittest

from sentences.backend.grammarizer import normalize_probability, get_nouns, Grammarizer
from sentences.words.noun import (Noun, DefiniteNoun, UncountableNoun, PluralNoun, DefiniteUncountableNoun,
                                  DefinitePluralNoun, IndefiniteNoun)
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb, ThirdPersonVerb, PastVerb, NegativeVerb, NegativeThirdPersonVerb, NegativePastVerb


class TestGrammarizer(unittest.TestCase):

    def test_normalize_probability(self):
        self.assertEqual(normalize_probability(0.2), 0.2)
        self.assertEqual(normalize_probability(1), 1)
        self.assertEqual(normalize_probability(0), 0)
        self.assertEqual(normalize_probability(-1), 0)
        self.assertEqual(normalize_probability(1.2), 1.0)

    def test_get_nouns_no_nouns(self):
        raw_paragraph = [
            [Pronoun.I, Verb('grab'), Pronoun.YOU, Punctuation.EXCLAMATION],
            [Pronoun.WE, Verb('cut', 'cut'), Pronoun.IT, Punctuation.PERIOD],
            [Pronoun.IT, Verb('have', 'had'), Pronoun.THEM, Punctuation.PERIOD]
        ]
        self.assertEqual(get_nouns(raw_paragraph), [])

    def test_get_nouns_with_nouns(self):
        paragraph = [
            [Noun('money'), Verb('grab'), Noun('tea'), Punctuation.EXCLAMATION],
            [Noun('tea'), Verb('ride', 'rode'), Noun('apple'), Punctuation.PERIOD],
            [Noun('apple'), Verb('surprise'), Noun('gold'), Punctuation.PERIOD],
            [Noun('gold'), Verb('cut', 'cut'), Pronoun.IT, Punctuation.PERIOD],
            [Pronoun.IT, Verb('have', 'had'), Noun('watch'), Punctuation.PERIOD]
        ]

        self.assertEqual(get_nouns(paragraph),
                         [Noun('money'), Noun('tea'), Noun('apple'), Noun('gold'), Noun('watch')])

    def test_grammarizer_init_defaults_and_paragraph_is_copy(self):
        random.seed(5)

        paragraph = [
            [UncountableNoun('money'), Verb('grab'), UncountableNoun('tea'), Punctuation.EXCLAMATION],
            [Pronoun.IT, Verb('have', '', 'had'), Noun('watch'), Punctuation.PERIOD]
        ]
        grammarizer = Grammarizer(paragraph)
        self.assertEqual(grammarizer._raw, paragraph)
        self.assertIsNot(grammarizer._raw, paragraph)
        self.assertIsNot(grammarizer._raw[0], paragraph[0])

        self.assertEqual(grammarizer.plural, 0.3)
        self.assertEqual(grammarizer.negative, 0.3)
        self.assertEqual(grammarizer.present_tense, True)
        noun_info = {
            UncountableNoun('tea'): {'plural': False, 'definite': False, 'countable': False},
            Noun('watch'): {'plural': False, 'definite': False, 'countable': True},
            UncountableNoun('money'): {'plural': False, 'definite': False, 'countable': False},
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
            [Noun('money'), Verb('grab'), Noun('tea'), Punctuation.EXCLAMATION],
            [Pronoun.IT, Verb('have', 'had'), Noun('watch'), Punctuation.PERIOD]
        ]
        grammarizer = Grammarizer(paragraph)
        info_1 = grammarizer.noun_info
        info_2 = grammarizer.noun_info
        self.assertEqual(info_1, info_2)
        self.assertIsNot(info_1, info_2)
        self.assertIsNot(info_1[Noun('money')], info_2[Noun('money')])

    def test_grammarizer_reset_definite_nouns(self):
        paragraph = [
            [Noun('money'), Verb('grab'), Noun('tea'), Punctuation.EXCLAMATION],
            [Pronoun.IT, Verb('have', 'had'), Noun('watch'), Punctuation.PERIOD]
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
            [UncountableNoun('money'), Verb('grab'), Noun('witch'), Punctuation.EXCLAMATION],
            [Noun('witch'), Verb('play'), Noun('watch'), Punctuation.PERIOD]
        ]
        grammarizer = Grammarizer(paragraph, probability_plural_noun=0.5)

        random.seed(10)

        grammarizer.set_nouns()
        noun_info = {
            Noun('watch'): {'plural': True, 'definite': False, 'countable': True},
            Noun('witch'): {'plural': False, 'definite': False, 'countable': True},
            UncountableNoun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(grammarizer.noun_info, noun_info)

        grammarizer.set_nouns()
        noun_info = {
            Noun('watch'): {'plural': True, 'definite': False, 'countable': True},
            Noun('witch'): {'plural': False, 'definite': False, 'countable': True},
            UncountableNoun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(grammarizer.noun_info, noun_info)

        grammarizer.set_nouns()
        noun_info = {
            Noun('watch'): {'plural': False, 'definite': False, 'countable': True},
            Noun('witch'): {'plural': False, 'definite': False, 'countable': True},
            UncountableNoun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(grammarizer.noun_info, noun_info)

    def test_grammarizer_set_nouns_never_sets_uncountable_nouns_to_plural(self):
        paragraph = [
            [UncountableNoun('money'), Verb('grab'), UncountableNoun('tea'), Punctuation.EXCLAMATION],
            [Noun('witch'), Verb('have', 'had'), Noun('watch'), Punctuation.PERIOD]
        ]
        grammarizer = Grammarizer(paragraph, probability_plural_noun=1.0)
        grammarizer.set_nouns()
        noun_info = {
            UncountableNoun('tea'): {'plural': False, 'definite': False, 'countable': False},
            Noun('watch'): {'plural': True, 'definite': False, 'countable': True},
            Noun('witch'): {'plural': True, 'definite': False, 'countable': True},
            UncountableNoun('money'): {'plural': False, 'definite': False, 'countable': False},
        }

        self.assertEqual(grammarizer.noun_info, noun_info)

    def test_generate_paragraph_returns_sentences_with_capitals(self):
        paragraph = [
            [Noun('money'), Verb('grab'), Noun('tea'), Punctuation.EXCLAMATION],
            [Noun('tea'), Verb('ride', '', 'rode'), Noun('apple'), Punctuation.PERIOD],
            [Noun('apple'), Verb('surprise'), Noun('gold'), Punctuation.PERIOD],
            [Noun('gold'), Verb('cut', '', 'cut'), Pronoun.IT, Punctuation.PERIOD],
            [Pronoun.IT, Verb('have', '', 'had'), Noun('watch'), Punctuation.PERIOD]
        ]
        grammarizer = Grammarizer(paragraph)
        paragraph = grammarizer.generate_paragraph()
        for sentence in paragraph:
            self.assertIn(sentence[0].value[0], string.ascii_uppercase)

    def test_generate_paragraph_makes_nouns_indefinite_in_first_instance_and_definite_later(self):
        raw_paragraph = 5 * [
            [Noun('money'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
            [Noun('witch'), Verb('play'), Noun('dog'), Punctuation.PERIOD],
        ]
        grammarizer = Grammarizer(raw_paragraph)
        paragraph = grammarizer.generate_paragraph()
        self.assertEqual(len(paragraph), 10)
        indefinite_part = paragraph[:2]
        definite_part = paragraph[2:]
        for sentence in indefinite_part:
            for word in sentence:
                self.assertNotIsInstance(word, DefiniteNoun)

        for sentence in definite_part:
            for word in sentence:
                if isinstance(word, Noun):
                    self.assertIsInstance(word, DefiniteNoun)

    def test_generate_paragraph_singular_countable_noun(self):
        raw_paragraph = [[Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION]]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=0.0)
        paragraph = grammarizer.generate_paragraph()
        expected = [[IndefiniteNoun('A cat', '', 'cat'), ThirdPersonVerb('grabs', 'grab'),
                     DefiniteNoun('the cat', '', 'cat'), Punctuation.EXCLAMATION]]
        self.assertEqual(paragraph, expected)

    def test_generate_paragraph_plural_countable_noun(self):
        raw_paragraph = [[Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION]]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=1.0)
        paragraph = grammarizer.generate_paragraph()
        expected = [[PluralNoun('Cats', '', 'cat'), Verb('grab'),
                     DefinitePluralNoun('the cats', 'the catses', 'cat'), Punctuation.EXCLAMATION]]
        self.assertEqual(paragraph, expected)

    def test_generate_paragraph_uncountable_noun(self):
        raw_paragraph = [[UncountableNoun('water'), Verb('grab'), UncountableNoun('water'), Punctuation.PERIOD]]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=1.0)
        paragraph = grammarizer.generate_paragraph()
        expected = [[UncountableNoun('Water', '', 'water'), ThirdPersonVerb('grabs', 'grab'),
                     DefiniteUncountableNoun('the water', '', 'water'), Punctuation.PERIOD]]
        self.assertEqual(paragraph, expected)

    def test_generate_paragraph_present_tense_third_person_positive(self):
        raw_paragraph = [
            [UncountableNoun('water'), Verb('grab'), UncountableNoun('water'), Punctuation.EXCLAMATION],
            [Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION]]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=0.0)
        paragraph = grammarizer.generate_paragraph()
        target_verb = ThirdPersonVerb('grabs', 'grab')
        for sentence in paragraph:
            self.assertEqual(sentence[1], target_verb)

    def test_generate_paragraph_present_tense_third_person_negative(self):
        raw_paragraph = [
            [UncountableNoun('water'), Verb('grab'), UncountableNoun('water'), Punctuation.EXCLAMATION],
            [Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION]]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=1.0, probability_plural_noun=0.0)
        paragraph = grammarizer.generate_paragraph()
        target_verb = NegativeThirdPersonVerb("doesn't grab", 'grab')
        for sentence in paragraph:
            self.assertEqual(sentence[1], target_verb)

    def test_generate_paragraph_present_tense_not_third_person_positive(self):
        raw_paragraph = [[Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.I, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.YOU, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.WE, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.THEY, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=1.0)
        paragraph = grammarizer.generate_paragraph()
        target_verb = Verb('grab')
        for sentence in paragraph:
            self.assertEqual(sentence[1], target_verb)

    def test_generate_paragraph_present_tense_not_third_person_negative(self):
        raw_paragraph = [[Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.I, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.YOU, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.WE, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.THEY, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=1.0, probability_plural_noun=1.0)
        paragraph = grammarizer.generate_paragraph()
        target_verb = NegativeVerb("don't grab", 'grab')
        for sentence in paragraph:
            self.assertEqual(sentence[1], target_verb)

    def test_generate_paragraph_past_tense_positive(self):
        raw_paragraph = [[UncountableNoun('water'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Noun('cat'), Verb('eat', '', 'ate'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.I, Verb('sing', '', 'sang'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.YOU, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.WE, Verb('sing', '', 'sang'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.THEY, Verb('eat', '', 'ate'), Noun('cat'), Punctuation.EXCLAMATION],
                         ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0,
                                  probability_plural_noun=1.0, present_tense=False)
        paragraph = grammarizer.generate_paragraph()
        target_verbs = [PastVerb('grabbed', 'grab'), PastVerb('ate', 'eat', 'ate'), PastVerb('sang', 'sing', 'sang')]
        for sentence in paragraph:
            self.assertIn(sentence[1], target_verbs)

    def test_generate_paragraph_past_tense_negative(self):
        raw_paragraph = [[UncountableNoun('water'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Noun('cat'), Verb('eat', '', 'ate'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.I, Verb('sing', '', 'sang'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.YOU, Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.WE, Verb('sing', '', 'sang'), Noun('cat'), Punctuation.EXCLAMATION],
                         [Pronoun.THEY, Verb('eat', '', 'ate'), Noun('cat'), Punctuation.EXCLAMATION],
                         ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=1.0,
                                  probability_plural_noun=1.0, present_tense=False)
        paragraph = grammarizer.generate_paragraph()
        target_verbs = [NegativePastVerb("didn't grab", 'grab'),
                        NegativePastVerb("didn't eat", 'eat', 'ate'),
                        NegativePastVerb("didn't sing", 'sing', 'sang')]
        for sentence in paragraph:
            self.assertIn(sentence[1], target_verbs)

    def test_assign_negatives_all_negative(self):
        raw_paragraph = 5 * [
            [UncountableNoun('money'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
            [Noun('witch'), Verb('play'), Noun('dog'), Punctuation.PERIOD],

        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=1.0)
        paragraph = grammarizer.generate_paragraph()
        for sentence in paragraph:
            for word in sentence:
                if isinstance(word, Verb):
                    value = word.value
                    tests_true = value.startswith("don't ") or value.startswith("doesn't ")
                    self.assertTrue(tests_true)

    def test_assign_negatives_no_negative(self):
        raw_paragraph = 5 * [
            [UncountableNoun('money'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
            [Noun('witch'), Verb('play'), Noun('dog'), Punctuation.PERIOD],

        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0)
        paragraph = grammarizer.generate_paragraph()
        for sentence in paragraph:
            for word in sentence:
                if isinstance(word, Verb):
                    value = word.value
                    tests_false = value.startswith("don't ") or value.startswith("doesn't ")
                    self.assertFalse(tests_false)

    def test_assign_negatives_some_negative(self):
        random.seed(3)
        raw_paragraph = 10 * [
            [UncountableNoun('money'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.5)
        paragraph = grammarizer.generate_paragraph()
        negatives = [1, 4, 5, 7, 8]
        for index, sentence in enumerate(paragraph):
            for word in sentence:
                if isinstance(word, Verb):
                    value = word.value
                    is_negative = value.startswith("don't ") or value.startswith("doesn't ")
                    if index in negatives:
                        self.assertTrue(is_negative)
                    else:
                        self.assertFalse(is_negative)

    def test_generate_paragraph_multiple_times_resets_indefinte(self):
        raw_paragraph = [
            [UncountableNoun('money'), Verb('grab'), UncountableNoun('money'), Punctuation.EXCLAMATION],
            [Noun('cat'), Verb('grab'), Noun('cat'), Punctuation.EXCLAMATION],
        ]
        grammarizer = Grammarizer(raw_paragraph, probability_negative_verb=0.0, probability_plural_noun=0.0)
        paragraph_1 = grammarizer.generate_paragraph()
        paragraph_2 = grammarizer.generate_paragraph()
        answer = [
            [UncountableNoun('money').capitalize(), ThirdPersonVerb('grabs', 'grab'),
             DefiniteUncountableNoun('the money', base='money'), Punctuation.EXCLAMATION],
            [IndefiniteNoun('A cat', base='cat'), ThirdPersonVerb('grabs', 'grab'),
             DefiniteNoun('the cat', base='cat'), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(answer, paragraph_1)
        self.assertEqual(answer, paragraph_2)
