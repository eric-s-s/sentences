import tkinter as tk

from sentences.gui.gui_tools import FilenameVar, DirectoryVar, SetVariablesFrame


class FileManagement(SetVariablesFrame):
    def __init__(self, *args, **kwargs):
        super(FileManagement, self).__init__(*args, **kwargs)
        self.home_directory = DirectoryVar('home folder:')
        self.save_directory = DirectoryVar('save folder:')
        self.countable_nouns = FilenameVar('countable nouns:')
        self.uncountable_nouns = FilenameVar('uncountable nouns:')
        self.proper_nouns = FilenameVar('proper nouns:')
        self.verbs = FilenameVar('verbs:')

        self._set_to_none()

        self._setup_file_area()

    def _setup_file_area(self):
        file_area = tk.Frame(master=self)
        values = [(self.home_directory, tk.RIDGE), (self.save_directory, tk.RIDGE),
                  (self.countable_nouns, tk.FLAT), (self.uncountable_nouns, tk.FLAT), (self.proper_nouns, tk.FLAT),
                  (self.verbs, tk.GROOVE)]
        for row, pair in enumerate(values):
            popup_var, relief = pair

            set_btn = tk.Button(master=file_area, text='SET', command=popup_var.set_with_popup)
            file_type = tk.Label(master=file_area, text=popup_var.popup_title, relief=relief, anchor=tk.W)
            location = tk.Label(master=file_area, textvar=popup_var)

            set_btn.grid(row=row, column=0,  padx=10, pady=5)
            file_type.grid(row=row, column=1, sticky=tk.W+tk.E)
            location.grid(row=row, column=2, sticky=tk.W)

        file_area.pack()

    def _set_to_none(self):
        self.home_directory.set('none')
        self.save_directory.set('none')
        self.countable_nouns.set('none')
        self.uncountable_nouns.set('none')
        self.proper_nouns.set('none')
        self.verbs.set('none')

    def get_values(self):
        """
        :keys:
            - 'home_directory'
            - 'save_directory'
            - 'countable_nouns'
            - 'uncountable_nouns'
            - 'proper_nouns'
            - 'verbs'
        """
        return {
            'home_directory': self.home_directory.get(),
            'save_directory': self.save_directory.get(),
            'countable_nouns': self.countable_nouns.get(),
            'uncountable_nouns': self.uncountable_nouns.get(),
            'proper_nouns': self.proper_nouns.get(),
            'verbs': self.verbs.get()
        }

    def trace_file_names(self, callback):
        self.countable_nouns.trace_variable('w', callback)
        self.uncountable_nouns.trace_variable('w', callback)
        self.proper_nouns.trace_variable('w', callback)
        self.verbs.trace_variable('w', callback)
