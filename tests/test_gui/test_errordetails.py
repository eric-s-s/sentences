import unittest
import tkinter as tk

from sentences.gui.errordetails import ErrorDetails
from sentences.gui.gui_tools import PctSpinBox


class TestParagraphType(unittest.TestCase):
    def setUp(self):
        self.frame = ErrorDetails()

    def test_init(self):
        answer = self.frame.get_values()
        self.assertEqual(answer, {
            'error_probability': 0.0,
            'noun_errors': False,
            'verb_errors': False,
            'punctuation_errors': False
        })

        self.assertIsInstance(self.frame.error_probability, PctSpinBox)

    def test_select_deselect_all(self):
        check_all = None
        for child in self.frame.winfo_children():
            if isinstance(child, tk.Checkbutton) and child.cget('text') == 'select/de-select all':
                check_all = child
                break
        check_all.invoke()
        self.assertEqual(self.frame.select_all.get(), 1)
        self.assertEqual(self.frame.get_values(), {
            'error_probability': 0.0,
            'noun_errors': True,
            'verb_errors': True,
            'punctuation_errors': True
        })
        check_all.invoke()
        self.assertEqual(self.frame.select_all.get(), 0)
        self.assertEqual(self.frame.get_values(), {
            'error_probability': 0.0,
            'noun_errors': False,
            'verb_errors': False,
            'punctuation_errors': False
        })

    def test_set_get_values(self):
        self.frame.error_probability.insert(0, '3')
        self.frame.noun_errors.set(1)
        self.frame.verb_errors.set(0)
        self.frame.punctuation_errors.set(1)
        self.assertEqual(self.frame.get_values(), {
            'error_probability': 0.3,
            'noun_errors': True,
            'verb_errors': False,
            'punctuation_errors': True
        })
