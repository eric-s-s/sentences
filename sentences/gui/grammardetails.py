

import tkinter as tk

from sentences.gui.gui_tools import PctSpinBox, SetVariablesFrame


class GrammarDetails(SetVariablesFrame):

    def __init__(self, *args, **kwargs):

        """
        present_tense = true
        probability_plural_noun = 0.3
        probability_negative_verb = 0.3
        probability_pronoun = 0.2
        """
        super(GrammarDetails, self).__init__(*args, **kwargs)

        self.probability_plural_noun = PctSpinBox(master=self)
        self.probability_negative_verb = PctSpinBox(master=self)
        self.probability_pronoun = PctSpinBox(master=self)
        plu_label = tk.Label(master=self, text='% chance of plural noun')
        neg_label = tk.Label(master=self, text='% chance of negative verb')
        pro_label = tk.Label(master=self, text='% chance of pronoun')

        self.tense = tk.StringVar()
        self._init_radio_button()

        # TODO DELETE
        self.get_button = tk.Button(master=self, text='get some', command=self.get_num)
        self.label_var = tk.StringVar()
        self.label_output = tk.Label(master=self, textvariable=self.label_var)

        self.label_output.grid(row=3, columnspan=2)
        self.get_button.grid(row=4, columnspan=2)
        # TODO DELETE

        plu_label.grid(row=0)
        self.probability_plural_noun.grid(row=0, column=1)
        neg_label.grid(row=1)
        self.probability_negative_verb.grid(row=1, column=1)
        pro_label.grid(row=2)
        self.probability_pronoun.grid(row=2, column=1)

    def _init_radio_button(self):
        self.tense.set('simple_present')
        radio_button_frame = tk.Frame(master=self, borderwidth=10, relief=tk.GROOVE)
        tk.Label(master=radio_button_frame, text='choose a tense').pack(anchor=tk.W)
        button_choices = [('simple present', 'simple_present'), ('simple past', 'simple_past')]
        for text, value in button_choices:
            b = tk.Radiobutton(master=radio_button_frame, text=text,
                               variable=self.tense, value=value)
            b.pack(anchor=tk.W)
        radio_button_frame.grid(rowspan=len(button_choices) + 1, column=2, padx=10)

    def get_values(self):
        """
        :keys:
        - tense
        - probability_plural_noun
        - probability_negative_verb
        - probability_pronoun
        """
        return {
            'tense': self.tense.get(),
            'probability_plural_noun': self.probability_plural_noun.get_probability(),
            'probability_negative_verb': self.probability_negative_verb.get_probability(),
            'probability_pronoun': self.probability_pronoun.get_probability()
        }

    def get_num(self):
        self.label_var.set('{}'.format(self.get_values()).replace(',', '\n'))


# TODO DELETE
def main():
    thing = tk.Tk()
    p_type = GrammarDetails(master=thing)
    p_type.pack()
    thing.mainloop()


if __name__ == '__main__':
    main()