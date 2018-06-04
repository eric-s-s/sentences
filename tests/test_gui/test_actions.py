import unittest
from unittest.mock import patch

import string

import tkinter as tk

from sentences.gui.actions import Actions, validate_file_prefix
from sentences.gui.gui_tools import IntSpinBox


class TestGrammarDetails(unittest.TestCase):
    def setUp(self):
        self.frame = Actions()

    def test_validate_file_prefix_true(self):
        reserved = '"<>:\\/?*|'
        all_chars = string.ascii_letters + string.punctuation
        for char in all_chars:
            if char not in reserved:
                self.assertTrue(validate_file_prefix(char))
                self.assertTrue(validate_file_prefix('a' + char))
        self.assertTrue(validate_file_prefix(''))

    @patch('sentences.gui.actions.showwarning')
    def test_validate_file_prefix_false(self, mock_warning):
        reserved = '"<>:\\/?*|'
        with_spaces = '" < > : \\ / ? * |'
        for char in reserved:
            self.assertFalse(validate_file_prefix(char))
            self.assertFalse(validate_file_prefix('a' + char))
        self.assertEqual(mock_warning.call_count, 2 * len(reserved))
        mock_warning.assert_called_with('illegal character',
                                        'The following characters are not allowed: {}'.format(with_spaces))

    def test_init(self):
        answer = self.frame.get_values()
        self.assertEqual(answer, {
            'file_prefix': '',
            'font_size': 2
        })

        self.assertIsInstance(self.frame.font_size, IntSpinBox)

        btn_txt = [
            (self.frame.save_settings, 'Save current settings'),
            (self.frame.export_settings, 'Export\nsettings'),
            (self.frame.reload_config, 'Reset to saved settings'),
            (self.frame.load_config_file, 'Load\nconfig file'),
            (self.frame.default_word_files, 'New default word files'),
            (self.frame.factory_reset, 'Factory Reset'),
            (self.frame.make_pdfs, 'Make me some PDFs'),
            (self.frame.read_me, 'Help'),
        ]
        for btn, txt in btn_txt:
            self.assertEqual(btn.cget('text'), txt)

    def test_set_get_values(self):
        self.frame.set_variable('file_prefix', 'thingy')
        self.frame.set_variable('font_size', 5)
        self.assertEqual(self.frame.get_values(), {
            'file_prefix': 'thingy',
            'font_size': 5
        })

    @patch('sentences.gui.actions.showwarning')
    def test_entry_validates_file_prefix(self, mock_warning):
        reserved = '"<>:\\/?*|'

        entry = None  # type: tk.Entry
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Entry):
                entry = widget
                break

        entry.insert(0, 'a')
        for char in reserved:
            entry.insert(tk.END, char)

        self.assertEqual(entry.get(), 'a')
        entry.insert(tk.END, 'b')
        self.assertEqual(entry.get(), 'ab')
        entry.delete(0, 1)
        self.assertEqual(entry.get(), 'b')
        entry.delete(0, tk.END)
        self.assertEqual(entry.get(), '')

        self.assertEqual(mock_warning.call_count, len(reserved))
