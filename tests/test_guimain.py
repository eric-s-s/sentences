import unittest
from unittest.mock import patch

import filecmp
import os
import shutil
import tkinter as tk

from sentences import DATA_PATH, APP_NAME, ConfigFileError, LoaderError
from tests import TESTS_FILES
from sentences.configloader import (CONFIG_FILE, DEFAULT_CONFIG, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV,
                                    VERBS_CSV, DEFAULT_SAVE_DIR, ConfigLoader, get_documents_folder, save_config,
                                    save_config_to_filename)

from sentences.gui.filemanagement import FileManagement

from sentences.guimain import MainFrame, catch_errors
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

    @patch("sentences.guimain.showerror")
    def test_catch_errors_decorator(self, mock_error):
        def error_func(num):
            if num == 1:
                raise ValueError('bad value')
            elif num == 2:
                raise ConfigFileError('bad file')
            elif num == 3:
                raise LoaderError('bad load')
            else:
                raise AttributeError('bad attr')

        without_msg = catch_errors('title')(error_func)

        without_msg(1)
        mock_error.assert_called_with('title', 'ValueError: bad value')

        without_msg(2)
        mock_error.assert_called_with('title', 'ConfigFileError: bad file')

        without_msg(3)
        mock_error.assert_called_with('title', 'LoaderError: bad load')

        self.assertRaises(AttributeError, without_msg, 4)

        with_msg = catch_errors('title', 'msg')(error_func)

        with_msg(1)
        mock_error.assert_called_with('title', 'msgValueError: bad value')

        with_msg(2)
        mock_error.assert_called_with('title', 'msgConfigFileError: bad file')

        with_msg(3)
        mock_error.assert_called_with('title', 'msgLoaderError: bad load')

        self.assertRaises(AttributeError, with_msg, 4)

    def test_init_no_config(self):
        main = MainFrame()
        loader = ConfigLoader()
        self.assertEqual(main.get_state(), loader.state)

        self.assertEqual(main.paragraph_generator._options, loader.state)

    def test_reload_files(self):
        ConfigLoader()
        save_config({'probability_plural_noun': 0,
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

        save_config({'probability_plural_noun': 0})
        loader = ConfigLoader()

        self.assertNotEqual(loader.state, main.get_state())
        main.load_config()
        self.assertEqual(loader.state, main.get_state())

    @patch("sentences.guimain.showerror")
    def test_load_config_error_reverts(self, mock_error):
        main = MainFrame()
        default_state = main.get_state()

        save_config({'probability_plural_noun': 0.0})
        main.load_config()

        self.assertNotEqual(main.get_state(), default_state)

        save_config({'probability_plural_noun': 'oops'})

        main.load_config()
        mock_error.assert_called_with(
            'bad config',
            "ConfigFileError: Tried to set key: 'probability_plural_noun' to incompatible value: 'oops'."
        )

        self.assertEqual(main.get_state(), default_state)

    @patch("sentences.guimain.showerror")
    def test_load_config_white_box_test_font_size_error(self, mock_error):
        main = MainFrame()
        default_state = main.get_state()

        save_config({'probability_plural_noun': 0.0})
        main.load_config()

        save_config({'font_size': 'oops'})
        main.load_config()
        self.assertEqual(main.get_state(), default_state)
        self.assertEqual(mock_error.call_args[0][0], 'bad config')
        self.assertIn('ConfigFileError: Tried to set key to incompatible value', mock_error.call_args[0][1])

    @patch("sentences.guimain.showerror")
    def test_load_config_white_box_test_file_prefix_error(self, mock_error):
        main = MainFrame()
        default_state = main.get_state()

        save_config({'probability_plural_noun': 0.0})
        main.load_config()

        save_config({'file_prefix': 10})
        main.load_config()
        self.assertEqual(main.get_state(), default_state)
        self.assertEqual(mock_error.call_args[0][0], 'bad config')
        self.assertIn('ConfigFileError: Tried to set key to incompatible value', mock_error.call_args[0][1])

    @patch("sentences.guimain.askopenfilename")
    def test_load_config_from_file_empty_string_does_nothing(self, mock_filename):
        main = MainFrame()
        save_config({'probability_plural_noun': 0.0})
        main.load_config()

        current_state = main.get_state()

        mock_filename.return_value = ''
        main.load_config_from_file()
        self.assertEqual(current_state, main.get_state())

    @patch("sentences.guimain.askopenfilename")
    def test_load_config_from_file_loads_from_file(self, mock_filename):
        filename = os.path.join(TESTS_FILES, 'tst.cfg')

        mock_filename.return_value = filename

        save_config_to_filename({'probability_plural_noun': 0.0}, filename)

        main = MainFrame()
        default_state = main.get_state()

        main.load_config_from_file()

        self.assertNotEqual(main.get_state(), default_state)

        loader = ConfigLoader()
        loader.set_state_from_file(filename)
        self.assertEqual(loader.state, main.get_state())

        os.remove(filename)

    @patch("sentences.guimain.showerror")
    @patch("sentences.guimain.askopenfilename")
    def test_load_config_from_file_bad_file_with_reset(self, mock_filename, mock_error):
        filename = os.path.join(TESTS_FILES, 'tst.cfg')

        mock_filename.return_value = filename

        save_config_to_filename({'probability_plural_noun': 'oops'}, filename)

        main = MainFrame()
        default_state = main.get_state()
        save_config({'probability_plural_noun': 0.0})
        main.load_config()

        main.load_config_from_file()

        self.assertEqual(main.get_state(), default_state)
        mock_error.assert_called_with(
            'bad config file',
            "ConfigFileError: Tried to set key: 'probability_plural_noun' to incompatible value: 'oops'."
        )

        os.remove(filename)

    @patch("sentences.guimain.showerror")
    @patch("sentences.guimain.askopenfilename")
    def test_load_config_from_file_bad_file_without_reset(self, mock_filename, mock_error):
        filename = os.path.join(TESTS_FILES, 'tst.cfg')
        bad_path = os.path.join(TESTS_FILES, 'nope', 'really_nope')

        mock_filename.return_value = filename

        save_config_to_filename({'save_directory': bad_path}, filename)

        main = MainFrame()
        save_config({'probability_plural_noun': 0.0})
        main.load_config()
        current_state = main.get_state()

        main.load_config_from_file()

        self.assertEqual(main.get_state(), current_state)
        self.assertEqual(mock_error.call_args[0][0], 'bad config file')
        msg = "ConfigFileError: Config Loader failed to create the following directory:\n"
        self.assertIn(msg, mock_error.call_args[0][1])

        os.remove(filename)

    @patch("sentences.guimain.asksaveasfilename")
    def test_export_config_file_saves_correctly(self, mock_filename):
        filename = os.path.join(TESTS_FILES, 'tst.cfg')

        if os.path.exists(filename):
            os.remove(filename)

        main = MainFrame()
        default_state = main.get_state()
        main.font_size.set_int(15)
        current_state = main.get_state()

        config_state = ConfigLoader().state
        expected_state = config_state.copy()
        expected_state['font_size'] = 15

        # test current state
        self.assertEqual(default_state, config_state)
        self.assertEqual(current_state, expected_state)
        self.assertNotEqual(default_state, current_state)

        mock_filename.return_value = filename
        main.export_config_file()

        saved_config = ConfigLoader()
        saved_config.set_state_from_file(filename)
        config_file_state = ConfigLoader().state

        self.assertEqual(saved_config.state, current_state)
        self.assertEqual(main.get_state(), current_state)
        self.assertEqual(config_file_state, default_state)

        mock_filename.assert_called_with(
            initialdir=current_state['home_directory'], title='select .cfg file',
            initialfile='exported_config.cfg', defaultextension='.cfg'
        )
        os.remove(filename)

    @patch("sentences.guimain.save_config_to_filename")
    @patch("sentences.guimain.asksaveasfilename")
    def test_export_config_file_no_save(self, mock_filename, mock_save_config):
        filename = os.path.join(TESTS_FILES, 'tst.cfg')

        mock_filename.return_value = filename

        main = MainFrame()
        main.export_config_file()
        self.assertEqual(mock_save_config.call_count, 1)

        mock_filename.return_value = ''

        main.export_config_file()
        self.assertEqual(mock_save_config.call_count, 1)

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
        ConfigLoader()  # set up directories

        save_config({'probability_pronoun': 0})
        with open(DEFAULT_CONFIG, 'r') as default:
            with open(CONFIG_FILE, 'r') as current:
                self.assertNotEqual(default.read(), current.read())

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
        mock_error.assert_called_with('Uh-oh!', 'ValueError: There are no nouns in any of the nouns lists.')

    @patch("sentences.guimain.showerror")
    def test_create_text_error_pool_not_large_enough(self, mock_error):
        ConfigLoader()  # set up directories
        save_config({'paragraph_type': 'pool', 'probability_pronoun': 0})
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
            save_config({key: bad_file})

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
