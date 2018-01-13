import unittest
import os
from tkinter.font import nametofont

from sentences import DATA_PATH

from sentences.gui.readme_text import (get_read_me_paragraphs, group_text, is_new_paragraph,
                                       find_second_margin, ReadMeText)


TEST_LINES = """sentences v2.1
==============

This module creates randomly generated paragraphs and then assigns specific
kinds of errors to those paragraphs. It outputs this text to a pdf file.

GUI options details
-------------------

- MAIN OPTIONS
    - "Save current settings": Saves the current setting to the config file.
                               They will be set at startup.
    - "Reset to saved settings": Reloads the config file.""".split('\n')


class TestReadMeText(unittest.TestCase):
    def test_is_new_paragraph(self):
        true_indices = [1, 2, 5, 7, 8, 9, 10, 12]
        for index, line in enumerate(TEST_LINES):
            if index in true_indices:
                self.assertTrue(is_new_paragraph(line))
            else:
                self.assertFalse(is_new_paragraph(line))

    def test_group_text(self):
        answer = group_text(TEST_LINES)
        expected = [
            "sentences v2.1",
            "==============",
            ("This module creates randomly generated paragraphs and then assigns specific kinds of errors to those " +
             "paragraphs. It outputs this text to a pdf file."),
            "GUI options details",
            "-------------------",
            '',
            "- MAIN OPTIONS",
            '    - "Save current settings": Saves the current setting to the config file. They will be set at startup.',
            '    - "Reset to saved settings": Reloads the config file.'
        ]
        self.assertEqual(answer, expected)

    def test_find_second_margin(self):
        answers = [0] * 7 + [len('    - "Save current settings": '),
                             len('    - "Reset to saved settings": ')]
        for line in group_text(TEST_LINES):
            self.assertEqual(answers.pop(0), find_second_margin(line))

    def test_get_read_me_paragraphs(self):
        with open(os.path.join(DATA_PATH, 'README.txt'), 'r') as f:
            paragraphs = group_text(f.read().split('\n'))
        self.assertEqual(paragraphs, get_read_me_paragraphs())

    def test_ReadMeText(self):
        text = ReadMeText()
        self.assertEqual(text.cget('state'), 'disabled')
        fontsize = nametofont(text.cget('font')).cget('size')
        for index, paragraph in enumerate(get_read_me_paragraphs()):
            tag_name = str(index)
            self.assertEqual(text.get(*text.tag_ranges(tag_name)), paragraph + '\n\n')
            self.assertEqual(text.tag_cget(tag_name, 'lmargin1'), '0')
            lmargin2 = str(find_second_margin(paragraph) * fontsize)
            self.assertEqual(text.tag_cget(tag_name, 'lmargin2'), lmargin2)

