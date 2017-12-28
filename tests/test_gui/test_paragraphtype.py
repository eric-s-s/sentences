import unittest
import tkinter as tk

from sentences.gui.paragraphtype import ParagraphType
from sentences.gui.gui_tools import IntSpinBox


class TestParagraphType(unittest.TestCase):
    def setUp(self):
        self.frame = ParagraphType()

    def test_init(self):
        answer = self.frame.get_values()
        self.assertEqual(answer, {
            'num_paragraphs': 1,
            'paragraph_size': 1,
            'subject_pool': 2,
            'paragraph_type': 'chain'
        })

        self.assertIsInstance(self.frame.num_paragraphs, IntSpinBox)
        self.assertIsInstance(self.frame.paragraph_size, IntSpinBox)
        self.assertIsInstance(self.frame.subject_pool, IntSpinBox)

        self.assertEqual(self.frame.num_paragraphs.range, (1, 10))
        self.assertEqual(self.frame.paragraph_size.range, (1, 20))
        self.assertEqual(self.frame.subject_pool.range, (2, 15))
        self.assertEqual(self.frame.paragraph_type.get(), 'chain')

    def test_radio_button(self):
        expected_values = ['pool', 'chain']
        radio_frame = None
        for child in self.frame.winfo_children():
            if isinstance(child, tk.Frame):
                radio_frame = child
                break
        for child in radio_frame.winfo_children():
            if isinstance(child, tk.Radiobutton):
                value = child.cget('value')
                self.assertIn(value, expected_values)
                child.select()
                self.assertEqual(value, self.frame.paragraph_type.get())

    def test_set_get_values(self):
        self.frame.paragraph_type.set('pool')
        self.frame.paragraph_size.insert(0, '100')
        self.frame.num_paragraphs.insert(0, '100')
        self.frame.subject_pool.insert(0, '100')
        self.assertEqual(self.frame.get_values(), {
            'num_paragraphs': 10,
            'paragraph_size': 20,
            'subject_pool': 15,
            'paragraph_type': 'pool'
        })
