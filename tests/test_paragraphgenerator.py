import unittest
from random import seed
import os

from sentences.paragraphsgenerator import ParagraphsGenerator

from sentences import APP_NAME, DATA_PATH, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV
from sentences.backend.random_paragraph import RandomParagraph


def line_print(long_text, lin_len):
    new = '("' + long_text[:lin_len] + '" +\n'
    long_text = long_text[lin_len:]
    while long_text:
        new += ' "' + long_text[:lin_len] + '" +\n'
        long_text = long_text[lin_len:]
    new = new[:-3] + '),'
    print(new)


def short_line_print(short_text):
    print('"{}",'.format(short_text))


class TestParagraphGenerator(unittest.TestCase):
    def setUp(self):
        self.config_state = {
            'home_directory': '',
            'save_directory': '',
            'countable_nouns': os.path.join(DATA_PATH, COUNTABLE_NOUNS_CSV),
            'uncountable_nouns': os.path.join(DATA_PATH, UNCOUNTABLE_NOUNS_CSV),
            'verbs': os.path.join(DATA_PATH, VERBS_CSV),

            'error_probability': 0.2,
            'noun_errors': True,
            'verb_errors': True,
            'punctuation_errors': True,

            'tense': 'simple_present',
            'probability_plural_noun': 0.3,
            'probability_negative_verb': 0.3,
            'probability_pronoun': 0.2,

            'paragraph_type': 'chain',
            'subject_pool': 5,
            'num_paragraphs': 4,
            'paragraph_size': 15,
        }

    def test_create_paragraph_generator(self):
        test = ParagraphsGenerator(self.config_state)
        answer = test.create_paragraphs()
        for text in answer:
            for ot in text:
                line_print(ot, 100)


