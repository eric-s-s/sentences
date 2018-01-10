
import tkinter as tk
from tkinter.font import Font
from sentences.gui.gui_tools import PctSpinBox, SetVariablesFrame, INTBOX_WIDTH


class ErrorDetails(SetVariablesFrame):

    def __init__(self, *args, **kwargs):
        super(ErrorDetails, self).__init__(*args, **kwargs)

        error_probability = tk.Frame(master=self)

        default_size = Font(font='TkDefaultFont').cget('size')
        tk.Label(master=error_probability, text='% chance for error: ', font=(None, default_size + 2)).pack(
            side=tk.LEFT)

        self.error_probability = PctSpinBox(master=error_probability, width=INTBOX_WIDTH)
        self.error_probability.pack(side=tk.LEFT)

        self.noun_errors = tk.IntVar()
        self.verb_errors = tk.IntVar()
        self.is_do_errors = tk.IntVar()
        self.preposition_transpose_errors = tk.IntVar()
        self.punctuation_errors = tk.IntVar()
        self.select_all = tk.IntVar()

        error_probability.pack(padx=10, pady=10)
        tk.Label(master=self, text='select types of errors\n-------------').pack()
        tk.Checkbutton(master=self, text='select/de-select all', variable=self.select_all,
                       command=self._toggle_all).pack(anchor=tk.W)
        tk.Checkbutton(master=self, text='noun errors', variable=self.noun_errors).pack(anchor=tk.W, padx=15)
        tk.Checkbutton(master=self, text='verb errors', variable=self.verb_errors).pack(anchor=tk.W, padx=15)
        tk.Checkbutton(master=self, text='is do errors', variable=self.is_do_errors).pack(anchor=tk.W, padx=15)
        tk.Checkbutton(
            master=self, text='transpose preposition errors', variable=self.preposition_transpose_errors
        ).pack(anchor=tk.W, padx=15)
        tk.Checkbutton(master=self, text='period errors', variable=self.punctuation_errors).pack(anchor=tk.W, padx=15)

    def _toggle_all(self):
        all_state = self.select_all.get()
        for intvar in [self.noun_errors, self.verb_errors, self.is_do_errors,
                       self.preposition_transpose_errors, self.punctuation_errors]:
            intvar.set(all_state)

    def get_values(self):
        """
        :keys:
        - error_probability
        - noun_errors
        - verb_errors
        - 'is_do_errors'
        - 'preposition_transpose_errors'
        - 'punctuation_errors'
        """
        return {
            'error_probability': self.error_probability.get_probability(),
            'noun_errors': bool(self.noun_errors.get()),
            'verb_errors': bool(self.verb_errors.get()),
            'is_do_errors': bool(self.is_do_errors.get()),
            'preposition_transpose_errors': bool(self.preposition_transpose_errors.get()),
            'punctuation_errors': bool(self.punctuation_errors.get())
        }
