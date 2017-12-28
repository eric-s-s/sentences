import os

import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory

def validate_int(new_val):
    return new_val.isdigit() or new_val == ''


class IntSpinBox(tk.Spinbox):
    def __init__(self, range_, *args, **kwargs):
        self.range = range_
        from_, to = range_
        validate = 'key'
        super(IntSpinBox, self).__init__(from_=from_, to=to, validate=validate, *args, **kwargs)
        check_int = (self.register(validate_int), '%P')
        self.config(vcmd=check_int)

    def get_int(self):
        min_int, max_int = self.range
        base_val = self.get()
        if not base_val:
            answer = min_int
        else:
            answer = min(max_int, max(min_int, int(base_val)))
        self.delete(0, tk.END)
        self.insert(0, answer)
        return answer


class PctSpinBox(IntSpinBox):
    def __init__(self, *args, **kwargs):
        pct_range = (0, 100)
        super(PctSpinBox, self).__init__(range_=pct_range, *args, **kwargs)

    def get_probability(self):
        return self.get_int()/100.


class PopupSelectVar(tk.StringVar):
    popup_func = None

    def __init__(self, popup_title='', *args, **kwargs):
        self.popup_title = popup_title
        self.popup_func = self.__class__.popup_func
        super(PopupSelectVar, self).__init__(*args, **kwargs)

    def set_with_popup(self):
        initial = self.get()
        if not os.path.exists(initial):
            initial = os.path.expanduser('~')

        new_location = self.popup_func(initialdir=initial, title=self.popup_title)
        if new_location:
            self.set(new_location)


class FilenameVar(PopupSelectVar):
    popup_func = askopenfilename


class DirectoryVar(PopupSelectVar):
    popup_func = askdirectory
