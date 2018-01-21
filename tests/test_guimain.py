import unittest
from unittest.mock import patch

import filecmp
import os
import shutil
import tkinter as tk

from sentences import DATA_PATH, APP_NAME
from tests import TESTS_FILES
from sentences.configloader import (CONFIG_FILE, DEFAULT_CONFIG, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV,
                                    VERBS_CSV, DEFAULT_SAVE_DIR, ConfigLoader, get_documents_folder)
from sentences.gui.filemanagement import FileManagement

from sentences.guimain import MainFrame
from sentences.words.verb import Verb
from sentences.words.noun import Noun


SAVE_CONFIG = os.path.join(TESTS_FILES, 'save.cfg')
SAVE_APP_FOLDER = os.path.join(TESTS_FILES, 'saved_app')

APP_FOLDER = os.path.join(get_documents_folder(), APP_NAME)


def rm_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)


def rm_app_folder():
    if os.path.exists(APP_FOLDER):
        shutil.rmtree(APP_FOLDER)


def mv_app_folder():
    src_target = APP_FOLDER
    if os.path.exists(src_target):
        shutil.copytree(src_target, SAVE_APP_FOLDER)


def restore_app_folder():
    if os.path.exists(SAVE_APP_FOLDER):
        shutil.copytree(SAVE_APP_FOLDER, APP_FOLDER)
        shutil.rmtree(SAVE_APP_FOLDER)


def mv_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as read_file:
            with open(SAVE_CONFIG, 'w') as write_file:
                write_file.write(read_file.read())


def restore_config():
    if os.path.exists(SAVE_CONFIG):
        with open(SAVE_CONFIG, 'r') as read_file:
            with open(CONFIG_FILE, 'w') as write_file:
                write_file.write(read_file.read())
        os.remove(SAVE_CONFIG)
    else:
        rm_config()


class TestGuiMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mv_app_folder()
        mv_config()

    @classmethod
    def tearDownClass(cls):
        restore_app_folder()
        restore_config()

    def setUp(self):
        rm_config()
        rm_app_folder()

    def tearDown(self):
        rm_config()
        rm_app_folder()

    def test_init_no_config(self):
        main = MainFrame()
        loader = ConfigLoader()
        self.assertEqual(main.get_state(), loader.state)

        self.assertEqual(main.paragraph_generator._options, loader.state)

    def test_reload_files(self):
        loader = ConfigLoader()
        loader.save_and_reload({'probability_plural_noun': 0,
                                'probability_negative_verb': 0,
                                'probability_pronoun': 0})
        new_verb = Verb('boogahboogah').third_person()
        new_noun = Noun('wackawacka').definite()
        main = MainFrame()

        with open(os.path.join(APP_FOLDER, COUNTABLE_NOUNS_CSV), 'w') as f:
            f.write('wackawacka')
        with open(os.path.join(APP_FOLDER, UNCOUNTABLE_NOUNS_CSV), 'w') as f:
            f.write('')
        with open(os.path.join(APP_FOLDER, VERBS_CSV), 'w') as f:
            f.write('boogahboogah')

        paragraph = main.paragraph_generator.create_paragraph()
        for sentence in paragraph:
            self.assertNotIn(new_noun, sentence)
            self.assertNotIn(new_verb, sentence)

        main.reload_files()

        paragraph = main.paragraph_generator.create_paragraph()
        for sentence in paragraph:
            self.assertIn(new_noun, sentence)
            self.assertIn(new_verb, sentence)

    def test_default_word_file(self):
        main = MainFrame()
        new_text = 'hi there'
        all_files = (UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV, VERBS_CSV)
        for file in all_files:
            with open(os.path.join(APP_FOLDER, file), 'w') as f:
                f.write(new_text)

        main.default_word_files()
        for file in all_files:
            with open(os.path.join(APP_FOLDER, file), 'r') as app_file:
                with open(os.path.join(DATA_PATH, file), 'r') as default:
                    self.assertEqual(app_file.read(), default.read())

            with open(os.path.join(APP_FOLDER, file.replace('.csv', '_old_01.csv')), 'r') as f:
                self.assertEqual(f.read(), new_text)

    def test_load_config(self):
        main = MainFrame()
        loader = ConfigLoader()

        loader.save_and_reload({'probability_plural_noun': 0})

        self.assertNotEqual(loader.state, main.get_state())
        main.load_config()
        self.assertEqual(loader.state, main.get_state())

    def test_set_config(self):
        main = MainFrame()

        with open(os.path.join(DATA_PATH, CONFIG_FILE), 'w') as f:
            f.write('')
        self.assertRaises(KeyError, ConfigLoader)

        main.set_config()
        self.assertEqual(main.get_state(), ConfigLoader().state)

    def test_read_me(self):
        main = MainFrame()
        main.read_me()
        top_levels = 0
        for child in main.winfo_children():
            if isinstance(child, tk.Toplevel):
                top_levels += 1
        self.assertEqual(top_levels, 1)

    def test_revert_to_original(self):
        loader = ConfigLoader()
        loader.save_and_reload({'probability_pronoun': 0})
        verb_file = os.path.join(APP_FOLDER, VERBS_CSV)
        with open(verb_file, 'w') as f:
            f.write('go')
        main = MainFrame()
        main.revert_to_original()
        with open(DEFAULT_CONFIG, 'r') as default:
            with open(CONFIG_FILE, 'r') as current:
                self.assertEqual(default.read(), current.read())
        with open(os.path.join(DATA_PATH, VERBS_CSV), 'r') as default:
            with open(verb_file, 'r') as current:
                self.assertEqual(default.read(), current.read())

    @patch("sentences.guimain.showerror")
    def test_create_text_error_no_verbs(self, mock_error):
        main = MainFrame()
        with open(os.path.join(APP_FOLDER, VERBS_CSV), 'w') as f:
            f.write('')
        main.reload_files()
        main.create_texts()
        mock_error.assert_called_with('Uh-oh!', 'ValueError: There are no verbs in the verb list.')

    @patch("sentences.guimain.showerror")
    def test_create_text_error_no_nouns(self, mock_error):
        main = MainFrame()
        for file_name in (UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV):
            with open(os.path.join(APP_FOLDER, file_name), 'w') as f:
                f.write('')
        main.reload_files()
        main.create_texts()
        mock_error.assert_called_with('Uh-oh!', 'ValueError: There are no countable nouns AND no uncountable nouns.')

    @patch("sentences.guimain.showerror")
    def test_create_text_error_pool_not_large_enough(self, mock_error):
        loader = ConfigLoader()
        loader.save_and_reload({'paragraph_type': 'pool', 'probability_pronoun': 0})
        for file_name in (UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV):
            with open(os.path.join(APP_FOLDER, file_name), 'w') as f:
                f.write('dog')
        main = MainFrame()

        main.create_texts()
        mock_error.assert_called_with('Uh-oh!',
                                      'ValueError: pool size is too large for available nouns loaded from file')

    @patch("sentences.guimain.showerror")
    def test_reload_files_bad_verbs(self, mock_error):
        main = MainFrame()
        with open(os.path.join(APP_FOLDER, VERBS_CSV), 'w') as f:
            f.write('oh, no, this, is, very, very, bad')
        main.reload_files()
        mock_error.assert_called_with('Bad file',
                                      'LoaderError: Bad values in columns for CSV for verbs. See default for example.')

    @patch("sentences.guimain.showerror")
    def test_init_bad_files(self, mock_error):
        ConfigLoader()
        with open(os.path.join(APP_FOLDER, VERBS_CSV), 'w') as f:
            f.write('oh, no, this, is, very, very, bad')
        MainFrame()
        message = ('On loading, caught the following error:\n' +
                   'LoaderError: Bad values in columns for CSV for verbs. See default for example.\n\n' +
                   'The original word files were moved to <name>_old_(number).csv and replaced with new files.')
        mock_error.assert_called_with('Bad start file', message)
        with open(os.path.join(APP_FOLDER, VERBS_CSV), 'r') as new_file:
            with open(os.path.join(DATA_PATH, VERBS_CSV), 'r') as default_file:
                self.assertEqual(new_file.read(), default_file.read())
        for file_name in (COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV):
            expected = os.path.join(APP_FOLDER, file_name.replace('.csv', '_old_01.csv'))
            self.assertTrue(os.path.exists(expected))

    @patch("sentences.guimain.showerror")
    def test_init_bad_files_unreadable(self, mock_error):
        ConfigLoader()
        src = os.path.join(DATA_PATH, 'go_time.ico')
        dst = os.path.join(APP_FOLDER, COUNTABLE_NOUNS_CSV)
        shutil.copy(src, dst)
        MainFrame()
        message = ('On loading, caught the following error:\n' +
                   'LoaderError: Could not read CSV file. ' +
                   'If you edited it in MSWord or something similar, it got formatted. Use "notepad"\n\n' +
                   'The original word files were moved to <name>_old_(number).csv and replaced with new files.')
        mock_error.assert_called_with('Bad start file', message)
        filecmp.cmp(src, dst.replace('.csv', '_old_01.csv'), shallow=False)

    @patch("sentences.guimain.showerror")
    def test_change_file_bad_file_by_config(self, mock_error):
        bad_file = os.path.join(DATA_PATH, 'go_time.ico')
        main = MainFrame()
        for count, key in enumerate(('countable_nouns', 'uncountable_nouns', 'verbs')):
            self.assertEqual(mock_error.call_count, count)
            main.revert_to_original()
            loader = ConfigLoader()
            loader.save_and_reload({key: bad_file})

            main.load_config()
            message = ('LoaderError: Could not read CSV file. ' +
                       'If you edited it in MSWord or something similar, it got formatted. Use "notepad"')
            mock_error.assert_called_with('Bad file', message)
            self.assertEqual(mock_error.call_count, count + 1)

    @patch("sentences.guimain.showerror")
    def test_change_file_bad_file_showerror_called_on_value_change(self, mock_error):

        bad_file = os.path.join(DATA_PATH, 'go_time.ico')
        main = MainFrame()
        files_frame = None
        for child in main.winfo_children():
            if isinstance(child, FileManagement):
                files_frame = child
        for count, key in enumerate(('countable_nouns', 'uncountable_nouns', 'verbs')):
            self.assertEqual(mock_error.call_count, count)
            main.revert_to_original()
            files_frame.set_variable(key, bad_file)

            message = ('LoaderError: Could not read CSV file. ' +
                       'If you edited it in MSWord or something similar, it got formatted. Use "notepad"')
            mock_error.assert_called_with('Bad file', message)
            self.assertEqual(mock_error.call_count, count + 1)

    @patch("sentences.guimain.showerror")
    def test_create_texts_missing_words(self, mock_error):
        ConfigLoader()
        with open(os.path.join(APP_FOLDER, VERBS_CSV), 'w') as f:
            f.write('')
        MainFrame().create_texts()
        mock_error.assert_called_with('Uh-oh!', 'ValueError: There are no verbs in the verb list.')

    @patch("sentences.guimain.showerror")
    def test_create_texts_reloads_words(self, mock_error):
        ConfigLoader()
        main = MainFrame()
        with open(os.path.join(APP_FOLDER, VERBS_CSV), 'w') as f:
            f.write('')
        main.create_texts()
        mock_error.assert_called_with('Uh-oh!', 'ValueError: There are no verbs in the verb list.')
        self.assertFalse(os.path.exists(os.path.join(APP_FOLDER, DEFAULT_SAVE_DIR, '01_answer.pdf')))
        self.assertFalse(os.path.exists(os.path.join(APP_FOLDER, DEFAULT_SAVE_DIR, '01_error.pdf')))

    @patch("sentences.guimain.CancelableMessagePopup")
    def test_message_popup_create_texts(self, mock_popup):
        main = MainFrame()
        main.create_texts()
        message = 'Your files are located at:\n{}'.format(main.get_state()['save_directory'])
        mock_popup.assert_called_with('success', message, main.do_not_show_popup)

        main.do_not_show_popup.set(1)
        main.create_texts()
        self.assertEqual(mock_popup.call_count, 1)

    def test_create_texts_creates_files(self):
        prefix = 'adjjk409dvc'
        main = MainFrame()
        main.do_not_show_popup.set(1)
        main.file_prefix.set(prefix)
        main.create_texts()
        self.assertTrue(os.path.exists(os.path.join(APP_FOLDER, DEFAULT_SAVE_DIR, prefix + '01_answer.pdf')))
        self.assertTrue(os.path.exists(os.path.join(APP_FOLDER, DEFAULT_SAVE_DIR, prefix + '01_error.pdf')))
