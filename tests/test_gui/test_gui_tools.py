import unittest

import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory

from sentences.gui.gui_tools import validate_int, IntSpinBox, PctSpinBox, FilenameVar, DirectoryVar, PopupSelectVar


class TestGuiTools(unittest.TestCase):

    def test_validate_int(self):
        self.assertTrue(validate_int(''))
        self.assertTrue(validate_int('123'))
        self.assertTrue(validate_int('001'))
        self.assertFalse(validate_int('-1'))
        self.assertFalse(validate_int('1a'))
        self.assertFalse(validate_int('1.2'))
        self.assertFalse(validate_int('2,000'))

    def test_IntSpinBox_init(self):
        box = IntSpinBox(range_=(2, 10))
        self.assertEqual(box.get(), '2')
        self.assertEqual(box.range, (2, 10))

    def test_IntSpinBox_validate_delete(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        self.assertEqual(box.get(), '')

    def test_IntSpinBox_validate_entry_false(self):
        box = IntSpinBox(range_=(2, 10))

        box.insert(0, 'a')
        self.assertEqual(box.get(), '2')

        box.insert(0, '0.2')
        self.assertEqual(box.get(), '2')

        box.insert(0, '2,000')
        self.assertEqual(box.get(), '2')

        box.insert(0, '-1')
        self.assertEqual(box.get(), '2')

    def test_IntSpinBox_validate_entry_true(self):
        box = IntSpinBox(range_=(2, 10))

        box.insert(0, '0')
        self.assertEqual(box.get(), '02')

        box.insert(tk.END, '0')
        self.assertEqual(box.get(), '020')

        box.insert(0, '2,000')
        self.assertEqual(box.get(), '020')

    def test_InitSpinBox_get_int_empty(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        answer = box.get_int()
        self.assertEqual(answer, 2)
        self.assertEqual(box.get(), '2')

    def test_InitSpinBox_get_int_below_min(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '1')
        answer = box.get_int()
        self.assertEqual(answer, 2)
        self.assertEqual(box.get(), '2')

    def test_InitSpinBox_get_int_above_max(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '100')
        answer = box.get_int()
        self.assertEqual(answer, 10)
        self.assertEqual(box.get(), '10')

    def test_InitSpinBox_get_int_at_max(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '10')
        answer = box.get_int()
        self.assertEqual(answer, 10)
        self.assertEqual(box.get(), '10')

    def test_InitSpinBox_get_int_at_min(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '2')
        answer = box.get_int()
        self.assertEqual(answer, 2)
        self.assertEqual(box.get(), '2')

    def test_InitSpinBox_get_int_mid_value(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '7')
        answer = box.get_int()
        self.assertEqual(answer, 7)
        self.assertEqual(box.get(), '7')

    def test_PctSpinBox(self):
        box = PctSpinBox()
        self.assertEqual(box.range, (0, 100))
        box.insert(0, '2')
        self.assertEqual(box.get_int(), 20)
        self.assertEqual(box.get_probability(), 0.2)

    def test_PopupSelectVar_empty_value(self):
        def mock_dialog(initialdir, title):
            return 'dir: {}, title: {}'.format(initialdir, title)

        new_var = PopupSelectVar(popup_title='omg')
        new_var.popup_func = mock_dialog

        new_var.set_with_popup()
        self.assertEqual(new_var.get(), 'dir: {}, title: omg'.format(os.path.expanduser('~')))

    def test_PopupSelectVar_bad_value(self):
        def mock_dialog(initialdir, title):
            return 'dir: {}, title: {}'.format(initialdir, title)

        new_var = PopupSelectVar(popup_title='omg')
        new_var.popup_func = mock_dialog
        new_var.set('this could not possibly be a directory.')

        new_var.set_with_popup()
        self.assertEqual(new_var.get(), 'dir: {}, title: omg'.format(os.path.expanduser('~')))

    def test_PopupSelectVar_correct_value(self):
        def mock_dialog(initialdir, title):
            return 'dir: {}, title: {}'.format(initialdir, title)

        new_var = PopupSelectVar(popup_title='omg')
        new_var.popup_func = mock_dialog
        new_var.set('.')

        new_var.set_with_popup()
        self.assertEqual(new_var.get(), 'dir: ., title: omg')

    def test_FilenameVar(self):
        new_var = FilenameVar()
        self.assertEqual(new_var.popup_func, askopenfilename)

    def test_DirectoryVar(self):
        new_var = DirectoryVar()
        self.assertEqual(new_var.popup_func, askdirectory)

