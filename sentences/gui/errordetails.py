
import tkinter as tk
from sentences.gui.gui_tools import PctSpinBox, SetVariablesFrame


class ErrorDetails(SetVariablesFrame):

    def __init__(self, *args, **kwargs):

        """
        probability_error = 0.2

        noun_errors = true
        verb_errors = true
        punctuation_errors = true

        """
        super(ErrorDetails, self).__init__(*args, **kwargs)

        error_probability = tk.Frame(master=self)
        tk.Label(master=error_probability, text='% chance for error: ').pack(side=tk.LEFT)
        self.error_probability = PctSpinBox(master=error_probability)
        self.error_probability.pack(side=tk.LEFT)

        self.noun_errors = tk.IntVar()
        self.verb_errors = tk.IntVar()
        self.punctuation_errors = tk.IntVar()
        self.select_all = tk.IntVar()

        error_probability.pack()
        tk.Label(master=self, text='select types of errors\n-------------').pack()
        tk.Checkbutton(master=self, text='select/de-select all', variable=self.select_all,
                       command=self._toggle_all).pack(anchor=tk.W)
        tk.Checkbutton(master=self, text='noun errors', variable=self.noun_errors).pack(anchor=tk.W, padx=15)
        tk.Checkbutton(master=self, text='verb errors', variable=self.verb_errors).pack(anchor=tk.W, padx=15)
        tk.Checkbutton(master=self, text='period errors', variable=self.punctuation_errors).pack(anchor=tk.W, padx=15)

        # TODO DELETE
        self.get_button = tk.Button(master=self, text='get some', command=self.get_num)
        self.label_var = tk.StringVar()
        self.label_output = tk.Label(master=self, textvariable=self.label_var)

        self.label_output.pack()
        self.get_button.pack()
        # TODO DELETE

    def _toggle_all(self):
        all_state = self.select_all.get()
        for intvar in [self.noun_errors, self.verb_errors, self.punctuation_errors]:
            intvar.set(all_state)

    def get_values(self):
        """
        :keys:
        - error_probability
        - noun_errors
        - verb_errors
        - punctuation_errors
        """
        return {
            'error_probability': self.error_probability.get_probability(),
            'noun_errors': bool(self.noun_errors.get()),
            'verb_errors': bool(self.verb_errors.get()),
            'punctuation_errors': bool(self.punctuation_errors.get())
        }

    def get_num(self):
        self.label_var.set('{}'.format(self.get_values()).replace(',', '\n'))


# TODO DELETE
def main():
    thing = tk.Tk()
    p_type = ErrorDetails(master=thing)
    p_type.pack()
    thing.mainloop()


if __name__ == '__main__':
    main()