import unittest

import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory

from sentences.gui.gui_tools import (validate_int, IntSpinBox, PctSpinBox, FilenameVar, DirectoryVar, PopupSelectVar,
                                     SetVariablesFrame, all_children, CancelableMessagePopup)


class TestGuiTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Variables need a widget floating around in the aether or they raise an error.
        tk.Tk()

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

    def test_IntSpinBox_get_int_empty(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        answer = box.get_int()
        self.assertEqual(answer, 2)
        self.assertEqual(box.get(), '2')

    def test_IntSpinBox_get_int_below_min(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '1')
        answer = box.get_int()
        self.assertEqual(answer, 2)
        self.assertEqual(box.get(), '2')

    def test_IntSpinBox_get_int_above_max(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '100')
        answer = box.get_int()
        self.assertEqual(answer, 10)
        self.assertEqual(box.get(), '10')

    def test_IntSpinBox_get_int_at_max(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '10')
        answer = box.get_int()
        self.assertEqual(answer, 10)
        self.assertEqual(box.get(), '10')

    def test_IntSpinBox_get_int_at_min(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '2')
        answer = box.get_int()
        self.assertEqual(answer, 2)
        self.assertEqual(box.get(), '2')

    def test_IntSpinBox_get_int_mid_value(self):
        box = IntSpinBox(range_=(2, 10))
        box.delete(0, tk.END)
        box.insert(0, '7')
        answer = box.get_int()
        self.assertEqual(answer, 7)
        self.assertEqual(box.get(), '7')

    def test_IntSpinBox_set_int(self):
        box = IntSpinBox(range_=(3, 5))
        box.set_int(-2)
        self.assertEqual(box.get_int(), 3)

        box.set_int(100)
        self.assertEqual(box.get_int(), 5)

        box.set_int(3)
        self.assertEqual(box.get_int(), 3)

        box.set_int(4)
        self.assertEqual(box.get_int(), 4)

        box.set_int(5)
        self.assertEqual(box.get_int(), 5)

    def test_PctSpinBox(self):
        box = PctSpinBox()
        self.assertEqual(box.range, (0, 100))
        box.insert(0, '2')
        self.assertEqual(box.get_int(), 20)
        self.assertEqual(box.get_probability(), 0.2)

    def test_PctSpinBox_get_probability_sets_to_max_or_min(self):
        box = PctSpinBox()
        box.insert(0, '500')
        self.assertEqual(box.get_probability(), 1.0)
        self.assertEqual(box.get(), '100')

        box.delete(0, tk.END)
        self.assertEqual(box.get_probability(), 0.0)
        self.assertEqual(box.get(), '0')

    def test_PctSpinBox_set_probability(self):
        box = PctSpinBox()
        box.set_probability(0.22)
        self.assertEqual(box.get_probability(), 0.22)
        self.assertEqual(box.get(), '22')

        box.set_probability(1.1)
        self.assertEqual(box.get_probability(), 1.0)

        box.set_probability(-0.2)
        self.assertEqual(box.get_probability(), 0.0)

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

    def test_SetVariableFrame_non_existent_value_raise_attribute_error(self):
        frame = SetVariablesFrame()
        self.assertRaises(AttributeError, frame.set_variable, 'not_there', 2)

    def test_SetVariableFrame_PctSpinBox_and_float(self):
        frame = SetVariablesFrame()
        frame.pct = PctSpinBox()
        frame.set_variable('pct', 0.3)
        self.assertEqual(frame.pct.get_probability(), 0.3)

    def test_SetVariableFrame_IntBox_and_int(self):
        frame = SetVariablesFrame()
        frame.int = IntSpinBox(range_=(2, 10))
        frame.set_variable('int', 11)
        self.assertEqual(frame.int.get_int(), 10)

    def test_SetVariableFrame_IntVar_and_bool(self):
        frame = SetVariablesFrame()
        frame.boolean = tk.IntVar()
        frame.set_variable('boolean', True)
        self.assertEqual(frame.boolean.get(), 1)
        frame.set_variable('boolean', False)
        self.assertEqual(frame.boolean.get(), 0)

    def test_SetVariableFrame_PopupSelectVar_str(self):
        frame = SetVariablesFrame()
        frame.selector = PopupSelectVar()
        frame.set_variable('selector', 'new_value')
        self.assertEqual(frame.selector.get(), 'new_value')

    def test_SetVariableFrame_unanticipated_value_defaults_to_set(self):
        frame = SetVariablesFrame()
        frame.fail = PctSpinBox()
        frame.succeed = tk.IntVar()
        frame.set_variable('succeed', -2)
        self.assertEqual(frame.succeed.get(), -2)
        self.assertRaises(AttributeError, frame.set_variable, 'fail', '1')

    def test_all_children_no_children(self):
        widget = tk.Label(text='hi')
        self.assertEqual(all_children(widget), [])

    def test_all_children_multi_level(self):
        top_widget = tk.Frame()
        down_1 = tk.Frame(master=top_widget)
        down_2 = tk.Frame(master=down_1)
        down_3 = tk.Frame(master=down_2)
        self.assertEqual(all_children(top_widget), [down_1, down_2, down_3])
        self.assertEqual(all_children(down_1), [down_2, down_3])

    def test_SetVariableFrame_set_bg(self):
        top_widget = SetVariablesFrame()
        down_1 = tk.Frame(master=top_widget)
        down_2 = tk.Frame(master=down_1)
        down_3 = tk.Label(master=down_2)
        top_widget.set_bg('blue')
        for widget in [top_widget, down_1, down_2, down_3]:
            self.assertEqual(widget.cget('bg'), 'blue')

    def test_CancelableMessagePopup(self):
        int_var = tk.IntVar()
        to_test = CancelableMessagePopup('title', 'text', int_var)

        self.assertEqual(to_test.title(), 'title')
        self.assertTrue(to_test.winfo_exists())
        self.assertEqual(int_var.get(), 0)

        for child in to_test.winfo_children():
            if isinstance(child, tk.Label):
                self.assertEqual(child.cget('text'), 'text')

        for child in to_test.winfo_children():
            if isinstance(child, tk.Checkbutton):
                child.invoke()
        self.assertEqual(int_var.get(), 1)

        for child in to_test.winfo_children():
            if type(child) == tk.Button:
                child.invoke()
        self.assertFalse(to_test.winfo_exists())


