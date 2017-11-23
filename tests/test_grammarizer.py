import random
import unittest

from sentences.grammarizer import normalize_probability, get_nouns, Grammarizer
from sentences.random_paragraph import RandomParagraph
from sentences.words.punctuation import Punctuation
from sentences.words.pronoun import Pronoun
from sentences.words.word import Word
from sentences.words.verb import BasicVerb, ConjugatedVerb
from sentences.words.noun import Noun


class TestGrammarizer(unittest.TestCase):

    def test_normalize_probability(self):
        self.assertEqual(normalize_probability(0.2), 0.2)
        self.assertEqual(normalize_probability(1), 1)
        self.assertEqual(normalize_probability(0), 0)
        self.assertEqual(normalize_probability(-1), 0)
        self.assertEqual(normalize_probability(1.2), 1.0)

    def test_get_nouns_no_nouns(self):
        random.seed(5)
        rp = RandomParagraph(p_pronoun=1.0)
        raw_paragraph = rp.create_chain_paragraph(3)
        self.assertEqual(get_nouns(raw_paragraph), [])

    def test_get_nouns_with_nouns(self):
        paragraph = [
            [Noun('money'), BasicVerb('grab'), Noun('tea'), Punctuation.EXCLAMATION],
            [Noun('tea'), BasicVerb('ride', 'rode'), Noun('apple'), Punctuation.PERIOD],
            [Noun('apple'), BasicVerb('surprise'), Noun('gold'), Punctuation.PERIOD],
            [Noun('gold'), BasicVerb('cut', 'cut'), Pronoun.IT, Punctuation.PERIOD],
            [Pronoun.IT, BasicVerb('have', 'had'), Noun('watch'), Punctuation.PERIOD]
        ]

        self.assertEqual(get_nouns(paragraph),
                         [Noun('money'), Noun('tea'), Noun('apple'), Noun('gold'), Noun('watch')])

    def test_grammarizer_init_defaults_and_paragraph_is_copy(self):
        random.seed(5)

        paragraph = [
            [Noun('money'), BasicVerb('grab'), Noun('tea'), Punctuation.EXCLAMATION],
            [Pronoun.IT, BasicVerb('have', 'had'), Noun('watch'), Punctuation.PERIOD]
        ]
        grammarizer = Grammarizer(paragraph)
        self.assertEqual(grammarizer._raw, paragraph)
        self.assertIsNot(grammarizer._raw, paragraph)
        self.assertIsNot(grammarizer._raw[0], paragraph[0])

        self.assertEqual(grammarizer.plural, 0.3)
        self.assertEqual(grammarizer.negative, 0.3)
        self.assertEqual(grammarizer.present_tense, True)
        noun_info = {
            Noun('tea'): {'plural': False, 'definite': False, 'countable': False},
            Noun('watch'): {'plural': False, 'definite': False, 'countable': True},
            Noun('money'): {'plural': False, 'definite': False, 'countable': False},
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
            [Noun('money'), BasicVerb('grab'), Noun('tea'), Punctuation.EXCLAMATION],
            [Pronoun.IT, BasicVerb('have', 'had'), Noun('watch'), Punctuation.PERIOD]
        ]
        grammarizer = Grammarizer(paragraph)
        info_1 = grammarizer.noun_info
        info_2 = grammarizer.noun_info
        self.assertEqual(info_1, info_2)
        self.assertIsNot(info_1, info_2)
        self.assertIsNot(info_1[Noun('money')], info_2[Noun('money')])

    def test_grammarizer_reset_definite_nouns(self):
        paragraph = [
            [Noun('money'), BasicVerb('grab'), Noun('tea'), Punctuation.EXCLAMATION],
            [Pronoun.IT, BasicVerb('have', 'had'), Noun('watch'), Punctuation.PERIOD]
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
            [Noun('money'), BasicVerb('grab'), Noun('witch'), Punctuation.EXCLAMATION],
            [Noun('witch'), BasicVerb('play'), Noun('watch'), Punctuation.PERIOD]
        ]
        grammarizer = Grammarizer(paragraph, p_plural=0.5)

        random.seed(10)

        grammarizer.set_nouns()
        noun_info = {
            Noun('watch'): {'plural': True, 'definite': False, 'countable': True},
            Noun('witch'): {'plural': False, 'definite': False, 'countable': True},
            Noun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(grammarizer.noun_info, noun_info)

        grammarizer.set_nouns()
        noun_info = {
            Noun('watch'): {'plural': True, 'definite': False, 'countable': True},
            Noun('witch'): {'plural': False, 'definite': False, 'countable': True},
            Noun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(grammarizer.noun_info, noun_info)

        grammarizer.set_nouns()
        noun_info = {
            Noun('watch'): {'plural': False, 'definite': False, 'countable': True},
            Noun('witch'): {'plural': False, 'definite': False, 'countable': True},
            Noun('money'): {'plural': False, 'definite': False, 'countable': False},
        }
        self.assertEqual(grammarizer.noun_info, noun_info)

    def test_grammarizer_set_nouns_never_sets_uncountable_nouns_to_plural(self):
        paragraph = [
            [Noun('money'), BasicVerb('grab'), Noun('tea'), Punctuation.EXCLAMATION],
            [Noun('witch'), BasicVerb('have', 'had'), Noun('watch'), Punctuation.PERIOD]
        ]
        grammarizer = Grammarizer(paragraph, p_plural=1.0)
        grammarizer.set_nouns()
        noun_info = {
            Noun('tea'): {'plural': False, 'definite': False, 'countable': False},
            Noun('watch'): {'plural': True, 'definite': False, 'countable': True},
            Noun('witch'): {'plural': True, 'definite': False, 'countable': True},
            Noun('money'): {'plural': False, 'definite': False, 'countable': False},
        }

        self.assertEqual(grammarizer.noun_info, noun_info)

