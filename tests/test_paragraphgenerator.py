import unittest
from random import seed
import os

from sentences.paragraphsgenerator import ParagraphsGenerator

from sentences import APP_NAME, DATA_PATH, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV
from sentences.backend.random_paragraph import RandomParagraph
from sentences.backend.loader import verbs, uncountable_nouns, countable_nouns


TEST_FILES = os.path.join(os.path.dirname(__file__), 'test_files')
delete_me = 'delete_me_{}'

DELETE_ME_VERBS = delete_me.format(VERBS_CSV)
DELETE_ME_COUNTABLE = delete_me.format(COUNTABLE_NOUNS_CSV)
DELETE_ME_UNCOUNTABLE = delete_me.format(UNCOUNTABLE_NOUNS_CSV)


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


def create_test_csvs(dummy_word):
    noun_text = dummy_word
    verb_text = '{}, null, null'.format(dummy_word)
    for filename, text in [(DELETE_ME_VERBS, verb_text),
                           (DELETE_ME_COUNTABLE, noun_text),
                           (DELETE_ME_UNCOUNTABLE, 'uncountable {}'.format(noun_text))]:
        with open(filename, 'w') as f:
            f.write(text)


def delete_test_csvs():
    for path in (DELETE_ME_VERBS, DELETE_ME_COUNTABLE, DELETE_ME_UNCOUNTABLE):
        if os.path.exists(path):
            os.remove(path)


class TestParagraphGenerator(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        delete_test_csvs()

    def setUp(self):
        delete_test_csvs()

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

    def test_init_loads_in_csv_paths(self):
        pg = ParagraphsGenerator(self.config_state)
        self.assertEqual(pg._verbs_list, verbs(os.path.join(DATA_PATH, VERBS_CSV)))
        self.assertEqual(pg._countable_nouns_list, countable_nouns(os.path.join(DATA_PATH, COUNTABLE_NOUNS_CSV)))
        self.assertEqual(pg._uncountable_nouns_list, uncountable_nouns(os.path.join(DATA_PATH, UNCOUNTABLE_NOUNS_CSV)))

    def test_load_csv_reloads(self):
        create_test_csvs('cat')
        self.config_state['verbs'] = DELETE_ME_VERBS
        self.config_state['countable_nouns'] = DELETE_ME_COUNTABLE
        self.config_state['uncountable_nouns'] = DELETE_ME_UNCOUNTABLE
        pg = ParagraphsGenerator(self.config_state)
        self.assertEqual(pg._verbs_list[0]['verb'].value, 'cat')
        self.assertEqual(pg._countable_nouns_list[0].value, 'cat')
        self.assertEqual(pg._uncountable_nouns_list[0].value, 'uncountable cat')

        create_test_csvs('dog')
        pg.load_lists_from_file()
        self.assertEqual(pg._verbs_list[0]['verb'].value, 'dog')
        self.assertEqual(pg._countable_nouns_list[0].value, 'dog')
        self.assertEqual(pg._uncountable_nouns_list[0].value, 'uncountable dog')

    def test_update_updates_dict(self):
        pg = ParagraphsGenerator(self.config_state)
        self.assertEqual(pg._options, self.config_state)

        pg.update_options({'paragraph_size': 10})
        self.config_state['paragraph_size'] = 10
        self.assertEqual(pg._options, self.config_state)

    def test_update_reloads_lists_if_any_are_empty(self):
        create_test_csvs('cat')
        self.config_state['verbs'] = DELETE_ME_VERBS
        self.config_state['countable_nouns'] = DELETE_ME_COUNTABLE
        self.config_state['uncountable_nouns'] = DELETE_ME_UNCOUNTABLE
        pg = ParagraphsGenerator(self.config_state)
        pg._verbs_list = []

        create_test_csvs('dog')
        pg.update_options({'dummy': 10})
        self.assertEqual(pg._verbs_list[0]['verb'].value, 'dog')
        self.assertEqual(pg._countable_nouns_list[0].value, 'dog')
        self.assertEqual(pg._uncountable_nouns_list[0].value, 'uncountable dog')


    # def test_create_paragraph_generator(self):
    #     test = ParagraphsGenerator(self.config_state)
    #     answer = test.create_paragraphs()
    #     for text in answer:
    #         for ot in text:
    #             line_print(ot, 100)


