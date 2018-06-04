import tkinter as tk
from tkinter.messagebox import showwarning

from sentences.gui.gui_tools import IntSpinBox, SetVariablesFrame


def validate_file_prefix(text):
    reserved = '"<>:\\/?*|'
    allowed = not any(char in reserved for char in text)
    with_spaces = reserved.replace('', ' ').strip()
    if not allowed:
        showwarning('illegal character', 'The following characters are not allowed: {}'.format(with_spaces))
    return allowed


class Actions(SetVariablesFrame):
    def __init__(self, *args, **kwargs):
        super(Actions, self).__init__(*args, **kwargs)

        self.font_size = IntSpinBox(master=self, range_=(2, 20))
        self.file_prefix = tk.StringVar()

        self.save_settings = tk.Button(master=self, text='Save current settings', bg='CadetBlue1')
        self.export_settings = tk.Button(master=self, text='Export\nsettings', bg='CadetBlue1')
        self.reload_config = tk.Button(master=self, text='Reset to saved settings', bg='aquamarine2')
        self.load_config_file = tk.Button(master=self, text='Load\nconfig file', bg='aquamarine2')
        self.default_word_files = tk.Button(master=self, text='New default word files', bg='plum1')
        self.factory_reset = tk.Button(master=self, text='Factory Reset', bg='firebrick1')

        self.make_pdfs = tk.Button(master=self, text='Make me some PDFs', bg='chartreuse2')
        self.read_me = tk.Button(master=self, text='Help', bg='light blue')

        self._pack_action_frame()

    def _pack_action_frame(self):
        padx, pady = (20, 5)

        col_row = {
            self.save_settings: (1, 0),
            self.export_settings: (0, 0),
            self.reload_config: (1, 1),
            self.load_config_file: (0, 1),
            self.default_word_files: (1, 3),
            self.factory_reset: (1, 4)
        }

        for button, col_row in col_row.items():
            col, row = col_row
            button.grid(row=row, column=col, padx=padx, pady=pady)

        validate = 'key'
        entry = tk.Entry(master=self, textvar=self.file_prefix, validate=validate)
        check_int = (self.register(validate_file_prefix), '%P')
        entry.config(vcmd=check_int)
        entry.grid(row=0, column=2, sticky=tk.E, padx=2, pady=pady)

        self.font_size.grid(row=1, column=2, padx=2, pady=pady, sticky=tk.E)

        self.make_pdfs.grid(row=2, column=2, padx=padx, pady=pady)

        tk.Label(master=self, text='Add a file prefix').grid(row=0, column=3, padx=2, pady=pady, sticky=tk.W)
        tk.Label(master=self, text='Font Size').grid(row=1, column=3, padx=2, pady=pady, sticky=tk.W)

        self.read_me.grid(row=3, column=3, sticky=(tk.E,))

    def get_values(self):
        """
        :keys:
            - font_size
            - file_prefix
        """
        file_prefix = self.file_prefix.get().strip()
        return {'font_size': self.font_size.get_int(),
                'file_prefix': file_prefix}
