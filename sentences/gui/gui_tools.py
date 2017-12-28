import tkinter as tk


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

