

import tkinter as tk

from sentences.gui.gui_tools import PctSpinBox, SetVariablesFrame, INTBOX_WIDTH


class GrammarDetails(SetVariablesFrame):

    def __init__(self, *args, **kwargs):
        super(GrammarDetails, self).__init__(*args, **kwargs)

        self.probability_plural_noun = PctSpinBox(master=self, width=INTBOX_WIDTH)
        self.probability_negative_verb = PctSpinBox(master=self, width=INTBOX_WIDTH)
        self.probability_pronoun = PctSpinBox(master=self, width=INTBOX_WIDTH)
        plu_label = tk.Label(master=self, text='% chance of plural noun')
        neg_label = tk.Label(master=self, text='% chance of negative verb')
        pro_label = tk.Label(master=self, text='% chance of pronoun')

        self.tense = tk.StringVar()
        self._init_radio_button()

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
