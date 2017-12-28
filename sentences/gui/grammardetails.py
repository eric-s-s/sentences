import tkinter as tk


def validate_int(new_val):
    return new_val.isdigit() or new_val == ''


class GrammarDetails(tk.Frame):

    def __init__(self, *args, **kwargs):
        """
        present_tense = true
        probability_plural_noun = 0.3
        probability_negative_verb = 0.3
        probability_pronoun = 0.2
        """
        super(GrammarDetails, self).__init__(*args, **kwargs)
        check_int = (self.register(validate_int), '%P')

        self.num_paragraphs_range = (1, 10)
        self.paragraph_size_range = (1, 20)
        self.subject_pool_range = (2, 15)

        self.num_paragraphs = tk.Spinbox(master=self, validate='key', vcmd=check_int,
                                         from_=self.num_paragraphs_range[0], to=self.num_paragraphs_range[1])
        self.paragraph_size = tk.Spinbox(master=self, validate='key', vcmd=check_int,
                                         from_=self.paragraph_size_range[0], to=self.paragraph_size_range[1])
        self.subject_pool = tk.Spinbox(master=self, validate='key', vcmd=check_int,
                                       from_=self.subject_pool_range[0], to=self.subject_pool_range[1])
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
            'num_paragraphs': self._get_pct('num_paragraphs'),
            'paragraph_size': self._get_pct('paragraph_size'),
            'subject_pool': self._get_pct('subject_pool'),
            'paragraph_type': self.paragraph_type.get()
        }

    def _get_pct(self, key):
        container_range = {
            'num_paragraphs': (self.num_paragraphs, self.num_paragraphs_range),
            'paragraph_size': (self.paragraph_size, self.paragraph_size_range),
            'subject_pool': (self.subject_pool, self.subject_pool_range)
        }
        container, ranges = container_range[key]
        base_val = container.get()
        if not base_val:
            answer = ranges[0]
        else:
            answer = min(ranges[1], max(ranges[0], int(base_val)))
        container.delete(0, tk.END)
        container.insert(0, answer)
        return answer

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