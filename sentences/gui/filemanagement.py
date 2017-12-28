import os
import tkinter as tk

from sentences import APP_NAME, DATA_PATH

from sentences.gui.gui_tools import FilenameVar, DirectoryVar

NOUN_CSV = 'nouns.csv'
UNCOUNTABLE_CSV = 'uncountable.csv'
VERBS_CSV = 'verbs.csv'

DEFAULT_CSVS = (NOUN_CSV, UNCOUNTABLE_CSV, VERBS_CSV)


def get_documents_folder():
    user_location = os.path.expanduser('~')
    user_folder = os.listdir(user_location)
    if 'My Documents' in user_folder:
        return os.path.join(user_location, 'My Documents')
    elif 'Documents' in user_folder:
        return os.path.join(user_location, 'Documents')
    else:
        return user_location


class FileManagement(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(FileManagement, self).__init__(*args, **kwargs)
        self.home_folder = DirectoryVar('home folder:')
        self.save_folder = DirectoryVar('save folder:')
        self.noun_file = FilenameVar('countable nouns:')
        self.verb_file = FilenameVar('uncountable nouns:')
        self.uncountable_file = FilenameVar('verbs:')

        self._set_defaults()

        self._setup_resets_area()
        self._setup_file_area()

    def _setup_resets_area(self):
        reset_area = tk.Frame(master=self, borderwidth=10, relief=tk.GROOVE)
        tk.Button(master=reset_area, text='CREATE DEFAULT\nCSV FILES', command=self.generate_default_csv_files).pack(
            side=tk.LEFT, anchor=tk.N, padx=10, pady=5)
        tk.Button(master=reset_area, text='RESET', command=self._set_defaults).pack(
            side=tk.LEFT, anchor=tk.N, padx=10, pady=5)
        reset_area.pack(anchor=tk.W)

    def _setup_file_area(self):
        file_area = tk.Frame(master=self)
        values = [self.home_folder, self.save_folder, self.noun_file, self.uncountable_file, self.verb_file]
        for row, popup_var in enumerate(values):
            tk.Label(master=file_area, text=popup_var.popup_title).grid(row=row, column=1, sticky=tk.W)
            tk.Label(master=file_area, textvar=popup_var).grid(row=row, column=2, sticky=tk.W)
            tk.Button(master=file_area, text='SET', command=popup_var.set_with_popup).grid(row=row, column=0,
                                                                                           padx=10, pady=5)
        file_area.pack()

    def _set_defaults(self):
        default_home = os.path.join(get_documents_folder(), APP_NAME)
        default_save = os.path.join(default_home, 'pdfs')
        if not os.path.exists(default_home):
            os.mkdir(default_home)
        if not os.path.exists(default_save):
            os.mkdir(default_save)
        self.home_folder.set(default_home)
        self.save_folder.set(default_save)
        self.noun_file.set('none')
        self.verb_file.set('none')
        self.uncountable_file.set('none')
        self._set_default_csv_values()

    def _set_default_csv_values(self):
        str_vars = [self.verb_file, self.noun_file, self.uncountable_file]
        csvs = [VERBS_CSV, NOUN_CSV, UNCOUNTABLE_CSV]
        home_folder = self.home_folder.get()
        for str_var, csv in zip(str_vars, csvs):
            target_filename = os.path.join(home_folder, csv)
            if os.path.exists(target_filename):
                str_var.set(target_filename)

    def generate_default_csv_files(self):
        self.move_old_files_to_new_location()
        for filename in DEFAULT_CSVS:
            default_filename = os.path.join(DATA_PATH, filename)
            target_filename = os.path.join(self.home_folder.get(), filename)
            with open(default_filename, 'r') as read_file:
                with open(target_filename, 'w') as write_file:
                    write_file.write(read_file.read())
        self._set_default_csv_values()

    def move_old_files_to_new_location(self):
        home_folder = self.home_folder.get()
        for filename in DEFAULT_CSVS:
            try:
                with open(os.path.join(home_folder, filename), 'r') as original:
                    original_text = original.read()
            except (IOError, FileNotFoundError, OSError):
                continue

            base_filename = os.path.join(home_folder, filename.replace('.csv', '_old_{}.csv'))
            counter = 0
            while os.path.exists(base_filename.format(counter)):
                counter += 1

            with open(base_filename.format(counter), 'w') as target:
                target.write(original_text)

    def get_values(self):
        return {
            'home_directory': self.home_folder.get(),
            'save_directory': self.save_folder.get(),
            'countable_nouns': self.noun_file.get(),
            'uncountable_nouns': self.uncountable_file.get(),
            'verbs': self.verb_file.get()
        }


# TODO DELETE
def main():
    thing = tk.Tk()
    p_type = FileManagement(master=thing)
    p_type.pack()
    thing.mainloop()


if __name__ == '__main__':
    main()
