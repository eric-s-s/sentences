import unittest

from sentences.gui.actions import Actions
from sentences.gui.gui_tools import IntSpinBox


class TestGrammarDetails(unittest.TestCase):
    def setUp(self):
        self.frame = Actions()

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
