import unittest
import tkinter as tk
from sentences.gui.filemanagement import FileManagement
from sentences.gui.gui_tools import FilenameVar, DirectoryVar


class TestFileManagement(unittest.TestCase):
    def setUp(self):
        self.frame = FileManagement()

    def test_init(self):
        answer = self.frame.get_values()
        self.assertEqual(answer, {
            'home_directory': 'none',
            'save_directory': 'none',
            'countable_nouns': 'none',
            'uncountable_nouns': 'none',
            'verbs': 'none'
        })

        self.assertIsInstance(self.frame.home_directory, DirectoryVar)
        self.assertIsInstance(self.frame.save_directory, DirectoryVar)
        self.assertIsInstance(self.frame.countable_nouns, FilenameVar)
        self.assertIsInstance(self.frame.uncountable_nouns, FilenameVar)
        self.assertIsInstance(self.frame.verbs, FilenameVar)

    def test_set_get_values(self):
        self.frame.set_variable('home_directory', 'home')
        self.frame.set_variable('save_directory', 'save')
        self.frame.set_variable('countable_nouns', 'countable')
        self.frame.set_variable('uncountable_nouns', 'uncountable')
        self.frame.set_variable('verbs', 'verbs')
        self.assertEqual(self.frame.get_values(), {
            'home_directory': 'home',
            'save_directory': 'save',
            'countable_nouns': 'countable',
            'uncountable_nouns': 'uncountable',
            'verbs': 'verbs'
        })

    def test_callback_assignment(self):
        def get_file(initialdir, title):
            return 'file: ' + title

        def get_dir(initialdir, title):
            return title

        original_file_var_func = FilenameVar.popup_func
        original_dir_var_func = DirectoryVar.popup_func

        FilenameVar.popup_func = get_file
        DirectoryVar.popup_func = get_dir
        new_frame = FileManagement()
        for child in new_frame.winfo_children():
            if isinstance(child, tk.Frame):
                for grand_child in child.winfo_children():
                    if isinstance(grand_child, tk.Button):
                        grand_child.invoke()
        self.assertEqual(new_frame.get_values(), {
            'home_directory': 'home folder:',
            'save_directory': 'save folder:',
            'countable_nouns': 'file: countable nouns:',
            'uncountable_nouns': 'file: uncountable nouns:',
            'verbs': 'file: verbs:'
        })

        FilenameVar.popup_func = original_file_var_func
        DirectoryVar.popup_func = original_dir_var_func
