import os

import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory


INTBOX_WIDTH = 7


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

    def set_int(self, num):
        self.delete(0, tk.END)
        self.insert(0, str(num))


class PctSpinBox(IntSpinBox):
    def __init__(self, *args, **kwargs):
        pct_range = (0, 100)
        super(PctSpinBox, self).__init__(range_=pct_range, *args, **kwargs)

    def get_probability(self):
        return self.get_int()/100.

    def set_probability(self, probability):
        pct = int(probability * 100)
        self.set_int(pct)


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


class SetVariablesFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(SetVariablesFrame, self).__init__(*args, **kwargs)

    def set_bg(self, color):
        self.config(bg=color)
        for child in all_children(self):
            child.config(bg=color)

    def set_variable(self, key, value):
        """

        :raises: ValueError, if value is the wrong type for a key.
        """
        variable = getattr(self, key)

        if isinstance(variable, PctSpinBox) and isinstance(value, float):
            variable.set_probability(value)
        elif isinstance(variable, IntSpinBox) and isinstance(value, int):
            variable.set_int(value)
        elif isinstance(variable, tk.IntVar) and isinstance(value, bool):
            variable.set(int(value))
        else:
            check_for_value_error(variable, value)
            variable.set(value)


def all_children(widget):
    children = widget.winfo_children()
    if not children:
        return []
    answer = children[:]
    for child in children:
        answer += all_children(child)
    return answer


def check_for_value_error(var, val):
    if isinstance(var, tk.IntVar):
        check_type = int
    elif isinstance(var, tk.BooleanVar):
        check_type = bool
    elif isinstance(var, tk.DoubleVar):
        check_type = float
    elif isinstance(var, tk.StringVar):
        check_type = str
    else:
        raise ValueError('Unrecognized variable type')

    if not isinstance(val, check_type):
        raise ValueError('value: {!r} is wrong type for variable: {}'.format(val, var))


class CancelableMessagePopup(tk.Toplevel):
    def __init__(self, title, message, int_var: tk.IntVar, *args, **kwargs):
        super(CancelableMessagePopup, self).__init__(*args, **kwargs)

        self.title(title)
        label = tk.Label(self, text=message, relief=tk.GROOVE, pady=10, padx=10, bg='light blue')
        label.grid(row=0, column=0, columnspan=2)
        check_btn = tk.Checkbutton(master=self, text='Don\'t show\nthis message again.', variable=int_var,
                                   justify=tk.LEFT, relief=tk.RIDGE)
        check_btn.grid(row=1, column=1)

        tk.Button(self, text="OK", command=self.ok, bg='light blue').grid(row=1, column=0)

    def ok(self):
        self.destroy()
