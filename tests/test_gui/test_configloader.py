import os
from shutil import rmtree
import unittest

from sentences.gui.configloader import (CONFIG_FILE, DEFAULT_CONFIG, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV,
                                        VERBS_CSV, DEFAULT_SAVE_DIR,
                                        create_default_config, save_config, load_config, ConfigLoader,
                                        get_documents_folder, get_key_value, get_key_value_list,
                                        create_line)

from sentences import DATA_PATH, APP_NAME


def rm_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)


def rm_app_folder():
    target = os.path.join(get_documents_folder(), APP_NAME)
    if os.path.exists(target):
        rmtree(target)


class TestConfigLoader(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        rm_config()

    def test_CONFIG_FILE(self):
        self.assertEqual(CONFIG_FILE, os.path.join(DATA_PATH, 'config.cfg'))

    def test_DEFAULT_CONFIG(self):
        self.assertEqual(DEFAULT_CONFIG, os.path.join(DATA_PATH, 'default.cfg'))

    def test_csv_constants(self):
        self.assertEqual(COUNTABLE_NOUNS_CSV, 'nouns.csv')
        self.assertEqual(UNCOUNTABLE_NOUNS_CSV, 'uncountable.csv')
        self.assertEqual(VERBS_CSV, 'verbs.csv')

    def test_DEFAULT_SAVE_DIR(self):
        self.assertEqual(DEFAULT_SAVE_DIR, 'pdfs')

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
        with open(DEFAULT_CONFIG, 'r') as f:
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
        self.assertEqual(get_key_value(' '), ('', None))

    def test_get_key_value_list_bad_file(self):
        bad_text = 'no comment and no equal'
        to_delete = os.path.join(DATA_PATH, 'to_delete.cfg')
        with open(to_delete, 'w') as f:
            f.write(bad_text)

        self.assertRaises(ValueError, get_key_value_list, to_delete)
        os.remove(to_delete)

    def test_get_key_value_list_default_config(self):
        answer = [
            ('# all values are case-insensitive and convert to lower case', None),
            ('', None),
            ('# FILE DETAILS', None),
            ('# home_directory = none defaults to system home. ex: C:/Users/<username>/My Documents/sentence_mangler',
             None),
            ('# save_directory = none defaults to home_directory/pdfs', None),
            ('home_directory', None),
            ('save_directory', None),
            ('', None),
            ('# word lists', None),
            ('# If none, defaults to home_directory/<filename>/[nouns.csv|uncountable.csv|verbs.csv]', None),
            ('countable_nouns', None),
            ('uncountable_nouns', None),
            ('verbs', None),
            ('', None),
            ('# ERROR DETAILS', None),
            ('error_probability', 0.2),
            ('', None),
            ('noun_errors', True),
            ('verb_errors', True),
            ('punctuation_errors', True),
            ('', None),
            ('# GRAMMAR DETAILS', None),
            ('# tense option: simple_present, simple_past', None),
            ('tense', 'simple_present'),
            ('probability_plural_noun', 0.3),
            ('probability_negative_verb', 0.3),
            ('probability_pronoun', 0.2),
            ('', None),
            ('# PARAGRAPH TYPE AND SIZE', None),
            ('# paragraph_type option: chain, pool', None),
            ('# subject_pool determines the number of subjects for pool type', None),
            ('paragraph_type', 'chain'),
            ('subject_pool', 5),
            ('num_paragraphs', 4),
            ('paragraph_size', 15),
            ('', None),
        ]
        self.assertEqual(get_key_value_list(DEFAULT_CONFIG), answer)

    def test_create_line(self):
        self.assertEqual(create_line('thing', 'string'), 'thing = string')
        self.assertEqual(create_line('file', 'E:/data/thing.csv'), 'file = E:/data/thing.csv')
        self.assertEqual(create_line('file', 'E:\\data\\thing.csv'), 'file = E:\\data\\thing.csv')
        self.assertEqual(create_line('int', 10), 'int = 10')
        self.assertEqual(create_line('float', 3.5), 'float = 3.5')
        self.assertEqual(create_line('TRUE', True), 'TRUE = true')
        self.assertEqual(create_line('FALSE', False), 'FALSE = false')
        self.assertEqual(create_line('NONE', None), 'NONE = none')

    def test_save_config(self):
        with open(DEFAULT_CONFIG, 'r') as f:
            default_text = f.read()
        save_config({'paragraph_type': 'bobo', 'paragraph_size': 10})
        with open(CONFIG_FILE, 'r') as f:
            config_text = f.read()

        answer = default_text.replace('paragraph_size = 15', 'paragraph_size = 10')
        answer = answer.replace('paragraph_type = chain', 'paragraph_type = bobo')
        self.assertEqual(answer, config_text)

    def test_load_config_default_config(self):
        answer = load_config(DEFAULT_CONFIG)
        self.assertEqual(answer, {
            'home_directory': None,
            'save_directory': None,
            'countable_nouns': None,
            'uncountable_nouns': None,
            'verbs': None,

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
        })

    def test_load_config_bad_file_ValueError(self):
        bad_text = 'no comment and no equal'
        to_delete = os.path.join(DATA_PATH, 'to_delete.cfg')
        with open(to_delete, 'w') as f:
            f.write(bad_text)

        self.assertRaises(ValueError, load_config, to_delete)
        os.remove(to_delete)

    def test_load_config_missing_file_OSError(self):
        self.assertRaises(OSError, load_config, 'not_there.cfg')

    def test_ConfigLoader_init_no_config_file_no_home_dir(self):
        rm_app_folder()
        rm_config()
        new = ConfigLoader()
        with open(DEFAULT_CONFIG, 'r') as default:
            with open(CONFIG_FILE, 'r') as target:
                self.assertEqual(default.read(), target.read())

        app_folder = os.path.join(get_documents_folder(), APP_NAME)
        for filename in [UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV, VERBS_CSV]:
            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                with open(os.path.join(app_folder, filename), 'r') as target:
                    self.assertEqual(default.read(), target.read())

        self.assertEqual(new._dictionary['home_directory'], app_folder)
        self.assertEqual(new._dictionary['save_directory'], os.path.join(app_folder, DEFAULT_SAVE_DIR))
        self.assertEqual(new._dictionary['countable_nouns'], os.path.join(app_folder, COUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['uncountable_nouns'], os.path.join(app_folder, UNCOUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['verbs'], os.path.join(app_folder, VERBS_CSV))

    def test_ConfigLoader_init_corrupted_config_file(self):
        rm_app_folder()
        with open(CONFIG_FILE, 'w') as f:
            f.write('ooooops')

        new = ConfigLoader()
        with open(DEFAULT_CONFIG, 'r') as default:
            with open(CONFIG_FILE, 'r') as target:
                self.assertEqual(default.read(), target.read())

        app_folder = os.path.join(get_documents_folder(), APP_NAME)
        for filename in [UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV, VERBS_CSV]:
            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                with open(os.path.join(app_folder, filename), 'r') as target:
                    self.assertEqual(default.read(), target.read())

        self.assertEqual(new._dictionary['home_directory'], app_folder)
        self.assertEqual(new._dictionary['save_directory'], os.path.join(app_folder, DEFAULT_SAVE_DIR))
        self.assertEqual(new._dictionary['countable_nouns'], os.path.join(app_folder, COUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['uncountable_nouns'], os.path.join(app_folder, UNCOUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['verbs'], os.path.join(app_folder, VERBS_CSV))

    def test_ConfigLoader_init_no_config_file_has_home_dir_and_some_files(self):
        rm_app_folder()
        rm_config()
        app_folder = os.path.join(get_documents_folder(), APP_NAME)
        os.mkdir(app_folder)
        with open(os.path.join(app_folder, VERBS_CSV), 'w') as f:
            f.write('hi there')

        new = ConfigLoader()
        with open(DEFAULT_CONFIG, 'r') as default:
            with open(CONFIG_FILE, 'r') as target:
                self.assertEqual(default.read(), target.read())

        for filename in [UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV]:
            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                with open(os.path.join(app_folder, filename), 'r') as target:
                    self.assertEqual(default.read(), target.read())
        with open(os.path.join(app_folder, VERBS_CSV), 'r') as f:
            self.assertEqual(f.read(), 'hi there')

        self.assertEqual(new._dictionary['home_directory'], app_folder)
        self.assertEqual(new._dictionary['save_directory'], os.path.join(app_folder, DEFAULT_SAVE_DIR))
        self.assertEqual(new._dictionary['countable_nouns'], os.path.join(app_folder, COUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['uncountable_nouns'], os.path.join(app_folder, UNCOUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['verbs'], os.path.join(app_folder, VERBS_CSV))

    def test_ConfigLoader_init_existing_config_file_existing_files(self):
        home = os.path.abspath('to_delete')
        save = os.path.abspath('bogus_save')
        existing_verbs = os.path.join(home, 'my_verb.csv')

        os.mkdir(home)
        os.mkdir(save)
        with open(existing_verbs, 'w') as f:
            f.write('exists')

        save_config({'home_directory': home, 'save_directory': save, 'verbs': existing_verbs})

        new = ConfigLoader()

        for filename in [UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV]:
            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                with open(os.path.join(home, filename), 'r') as target:
                    self.assertEqual(default.read(), target.read())
        with open(existing_verbs, 'r') as f:
            self.assertEqual(f.read(), 'exists')

        self.assertEqual(new._dictionary['home_directory'], home)
        self.assertEqual(new._dictionary['save_directory'], save)
        self.assertEqual(new._dictionary['countable_nouns'], os.path.join(home, COUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['uncountable_nouns'], os.path.join(home, UNCOUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['verbs'], existing_verbs)

        rmtree(home)
        rmtree(save)

    def test_ConfigLoader_init_existing_config_file_non_existent_files(self):
        home = os.path.abspath('to_delete')
        save = os.path.abspath('bogus_save')
        existing_verbs = os.path.join(home, 'not_really_there.csv')

        os.mkdir(home)
        os.mkdir(save)

        save_config({'home_directory': home, 'save_directory': save, 'verbs': existing_verbs})

        new = ConfigLoader()

        for filename in [UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV, VERBS_CSV]:
            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                with open(os.path.join(home, filename), 'r') as target:
                    self.assertEqual(default.read(), target.read())

        self.assertEqual(new._dictionary['home_directory'], home)
        self.assertEqual(new._dictionary['save_directory'], save)
        self.assertEqual(new._dictionary['countable_nouns'], os.path.join(home, COUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['uncountable_nouns'], os.path.join(home, UNCOUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['verbs'], os.path.join(home, VERBS_CSV))

        rmtree(home)
        rmtree(save)

    def test_ConfigLoader_init_existing_config_file_non_existent_directories_only_if_parent_path_exists(self):
        home = os.path.abspath('to_delete')
        save = os.path.join(home, 'bogus_save')

        save_config({'home_directory': home, 'save_directory': save})

        new = ConfigLoader()

        for filename in [UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV, VERBS_CSV]:
            with open(os.path.join(DATA_PATH, filename), 'r') as default:
                with open(os.path.join(home, filename), 'r') as target:
                    self.assertEqual(default.read(), target.read())

        self.assertEqual(new._dictionary['home_directory'], home)
        self.assertEqual(new._dictionary['save_directory'], save)
        self.assertEqual(new._dictionary['countable_nouns'], os.path.join(home, COUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['uncountable_nouns'], os.path.join(home, UNCOUNTABLE_NOUNS_CSV))
        self.assertEqual(new._dictionary['verbs'], os.path.join(home, VERBS_CSV))

        rmtree(home)

    def test_ConfigLoader_init_existing_config_fails_when_directory_parent_not_there(self):
        home = 'not_there/really_not_there'
        save_config({'home_directory': home})
        self.assertRaises(OSError, ConfigLoader)



