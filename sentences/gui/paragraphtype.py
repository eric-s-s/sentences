
import tkinter as tk

from sentences.gui.gui_tools import IntSpinBox


class ParagraphType(tk.Frame):

    def __init__(self, *args, **kwargs):
        super(ParagraphType, self).__init__(*args, **kwargs)

        num_paragraphs_range = (1, 10)
        paragraph_size_range = (1, 20)
        subject_pool_range = (2, 15)

        self.num_paragraphs = IntSpinBox(master=self, range_=num_paragraphs_range)
        self.paragraph_size = IntSpinBox(master=self, range_=paragraph_size_range)
        self.subject_pool = IntSpinBox(master=self, range_=subject_pool_range)
        np_label = tk.Label(master=self, text='number of paragraphs')
        ns_label = tk.Label(master=self, text='sentences per paragraph')
        sp_label = tk.Label(master=self, text='subject pool size')

        self.paragraph_type = tk.StringVar()
        self._init_radio_button()

        # TODO DELETE
        self.get_button = tk.Button(master=self, text='get some', command=self.get_num)
        self.label_var = tk.StringVar()
        self.label_output = tk.Label(master=self, textvariable=self.label_var)

        self.label_output.grid(row=3, columnspan=2)
        self.get_button.grid(row=4, columnspan=2)
        # TODO DELETE

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

    def get_num(self):
        self.label_var.set('{}'.format(self.get_values()).replace(',', '\n'))


# TODO DELETE
def main():
    thing = tk.Tk()
    p_type = ParagraphType(master=thing)
    p_type.pack()
    thing.mainloop()


if __name__ == '__main__':
    main()