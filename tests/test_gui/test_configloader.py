import os
import unittest

from sentences.gui.configloader import (create_default_config, has_config_file, get_documents_folder, CONFIG_FILE,
                                        get_key_value, get_key_value_list)

from sentences import DATA_PATH


class TestConfigLoader(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)

    def test_CONFIG_FILE(self):
        self.assertEqual(CONFIG_FILE, os.path.join(DATA_PATH, 'config.cfg'))

    def test_has_config_file(self):
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        self.assertFalse(has_config_file())

        with open(CONFIG_FILE, 'w') as f:
            f.write('hi')
        self.assertTrue(has_config_file())

    def test_get_documents_folder(self):
        user_dir = os.path.expanduser('~')
        docs = os.path.join(user_dir, 'Documents')
        my_docs = os.path.join(user_dir, 'My Documents')

        answer = get_documents_folder()
        self.assertIn(answer, [user_dir, docs, my_docs])
        self.assertTrue(os.path.exists(answer))

    def test_create_default_config(self):
        with open(CONFIG_FILE, 'w') as f:
            f.write('hi')

        with open(CONFIG_FILE, 'r') as f:
            before = f.read()
        self.assertEqual(before, 'hi')

        create_default_config()
        with open(os.path.join(DATA_PATH, 'default.cfg'), 'r') as f:
            default = f.read()

        with open(CONFIG_FILE, 'r') as f:
            current = f.read()

        self.assertNotEqual(current, before)
        self.assertEqual(current, default)

    def test_get_key_value_positive_int(self):
        self.assertEqual(get_key_value('my_int = 123'), ('my_int', 123))
        self.assertEqual(get_key_value(' my_int =  0 '), ('my_int', 0))

    def test_get_key_value_float(self):
        self.assertEqual(get_key_value('my_float = 123.44'), ('my_float', 123.44))
        self.assertEqual(get_key_value('my_float = -0.01'), ('my_float', -0.01))

    def test_get_key_value_special(self):
        self.assertEqual(get_key_value('special = true'), ('special', True))
        self.assertEqual(get_key_value('special = false'), ('special', False))
        self.assertEqual(get_key_value('special = none'), ('special', None))

        self.assertEqual(get_key_value('special = TRUE'), ('special', True))
        self.assertEqual(get_key_value('special = FALSE'), ('special', False))
        self.assertEqual(get_key_value('special = NONE'), ('special', None))

    def test_get_key_value_others(self):
        self.assertEqual(get_key_value('thing = this is my thing. '), ('thing', 'this is my thing.'))

    def test_get_key_value_empty(self):
        self.assertEqual(get_key_value(' '), (None, None))

    def test_get_key_value_list(self):
        answer = [
            ('# all values are case-insensitive and convert to lower case', None),
            (None, None),
            ('# FILE DETAILS', None),
            ('# home_directory = none defaults to system home. ex: C:/Users/<username>/My Documents/sentence_mangler',
             None),
            ('# save_directory = none defaults to home_directory/pdfs', None),
            ('home_directory', None),
            ('save_directory', None),
            (None, None),
            ('# word lists', None),
            ('# If no directory, defaults to home_directory/<filename>', None),
            ('countable_nouns', 'nouns.csv'),
            ('uncountable_nouns', 'uncountable.csv'),
            ('verbs', 'verbs.csv'),
            (None, None),
            ('# ERROR DETAILS', None),
            ('error_probability', 0.2),
            (None, None),
            ('noun_errors', True),
            ('verb_errors', True),
            ('punctuation_errors', True),
            (None, None),
            ('# GRAMMAR DETAILS', None),
            ('# tense option: simple_present, simple_past', None),
            ('tense', 'simple_present'),
            ('probability_plural_noun', 0.3),
            ('probability_negative_verb', 0.3),
            ('probability_pronoun', 0.2),
            (None, None),
            ('# PARAGRAPH TYPE AND SIZE', None),
            ('# paragraph_type option: chain, pool', None),
            ('# subject_pool determines the number of subjects for pool type', None),
            ('paragraph_type', 'chain'),
            ('subject_pool', 5),
            ('num_paragraphs', 4),
            ('paragraph_size', 15),
            (None, None),
        ]
        self.assertEqual(get_key_value_list(os.path.join(DATA_PATH, 'default.cfg')), answer)