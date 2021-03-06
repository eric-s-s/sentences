
import tkinter as tk

from sentences.gui.gui_tools import IntSpinBox, SetVariablesFrame, INTBOX_WIDTH


class ParagraphType(SetVariablesFrame):

    def __init__(self, *args, **kwargs):
        super(ParagraphType, self).__init__(*args, **kwargs)

        num_paragraphs_range = (1, 10)
        paragraph_size_range = (1, 20)
        subject_pool_range = (2, 15)

        self.num_paragraphs = IntSpinBox(master=self, range_=num_paragraphs_range, width=INTBOX_WIDTH)
        self.paragraph_size = IntSpinBox(master=self, range_=paragraph_size_range, width=INTBOX_WIDTH)
        self.subject_pool = IntSpinBox(master=self, range_=subject_pool_range, width=INTBOX_WIDTH)
        np_label = tk.Label(master=self, text='number of paragraphs')
        ns_label = tk.Label(master=self, text='sentences per paragraph')
        sp_label = tk.Label(master=self, text='subject pool size')

        self.paragraph_type = tk.StringVar()
        self._init_radio_button()

        np_label.grid(row=0)
        self.num_paragraphs.grid(row=0, column=1)
        ns_label.grid(row=1)
        self.paragraph_size.grid(row=1, column=1)
        sp_label.grid(row=2)
        self.subject_pool.grid(row=2, column=1)

    def _init_radio_button(self):
        self.paragraph_type.set('chain')
        radio_button_frame = tk.Frame(master=self, borderwidth=10, relief=tk.GROOVE)
        tk.Label(master=radio_button_frame, text='choose a paragraph type').pack(anchor=tk.W)
        button_choices = [('chain paragraph', 'chain'), ('subject pool paragraph', 'pool')]
        for text, value in button_choices:
            b = tk.Radiobutton(master=radio_button_frame, text=text,
                               variable=self.paragraph_type, value=value)
            b.pack(anchor=tk.W)
        radio_button_frame.grid(rowspan=len(button_choices) + 1, column=2, padx=10)

    def get_values(self):
        """
        :keys:
            - num_paragraphs
            - paragraph_size
            - subject_pool
            - paragraph_type
        """
        return {
            'num_paragraphs': self.num_paragraphs.get_int(),
            'paragraph_size': self.paragraph_size.get_int(),
            'subject_pool': self.subject_pool.get_int(),
            'paragraph_type': self.paragraph_type.get()
        }
