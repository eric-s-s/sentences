import unittest
import tkinter as tk

from sentences.gui.grammardetails import GrammarDetails
from sentences.gui.gui_tools import PctSpinBox


class TestParagraphType(unittest.TestCase):
    def setUp(self):
        self.frame = GrammarDetails()

    def test_init(self):
        answer = self.frame.get_values()
        self.assertEqual(answer, {
            'tense': 'simple_present',
            'probability_plural_noun': 0.0,
            'probability_negative_verb': 0.0,
            'probability_pronoun': 0.0
        })

        self.assertIsInstance(self.frame.probability_plural_noun, PctSpinBox)
        self.assertIsInstance(self.frame.probability_negative_verb, PctSpinBox)
        self.assertIsInstance(self.frame.probability_pronoun, PctSpinBox)

        self.assertEqual(self.frame.tense.get(), 'simple_present')

    def test_radio_button(self):
        expected_values = ['simple_present', 'simple_past']
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
                self.assertEqual(value, self.frame.tense.get())

    def test_set_get_values(self):
        self.frame.set_variable('tense', 'simple_past')
        self.frame.set_variable('probability_plural_noun', 0.2)
        self.frame.set_variable('probability_negative_verb', 0.5)
        self.frame.set_variable('probability_pronoun', 1.0)
        self.assertEqual(self.frame.get_values(), {
            'tense': 'simple_past',
            'probability_plural_noun': 0.2,
            'probability_negative_verb': 0.5,
            'probability_pronoun': 1.0
        })
