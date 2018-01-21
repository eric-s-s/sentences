from functools import wraps
import tkinter as tk
from tkinter.messagebox import showerror
import os

from sentences import DATA_PATH

from sentences.create_pdf import create_pdf
from sentences.configloader import ConfigLoader
from sentences.paragraphsgenerator import ParagraphsGenerator
from sentences.configloader import save_config
from sentences.backend.create_word_files import create_default_word_files

from sentences.gui.errordetails import ErrorDetails
from sentences.gui.paragraphtype import ParagraphType
from sentences.gui.grammardetails import GrammarDetails
from sentences.gui.filemanagement import FileManagement
from sentences.gui.gui_tools import IntSpinBox, CancelableMessagePopup
from sentences.gui.readme_text import ReadMeText

from sentences.backend.loader import LoaderError


def catch_errors(title, extra_message=''):
    def decorator(func):
        @wraps(func)
        def catch_wrapper(*args):
            try:
                return func(*args)
            except (ValueError, LoaderError) as e:
                message = extra_message + '{}: {}'.format(e.__class__.__name__, e.args[0])
                showerror(title, message)

        return catch_wrapper
    return decorator


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.iconbitmap(os.path.join(DATA_PATH, 'go_time.ico'))

        action_frame = tk.Frame(master=self)
        self.font_size = IntSpinBox(master=action_frame, range_=(2, 20))
        self.file_prefix = tk.StringVar()

        self._pack_action_frame(action_frame)

        self.frames = self._pack_set_variable_frames()
        self.load_config()

        try:
            self.paragraph_generator = ParagraphsGenerator(self.get_state())
        except LoaderError as e:
            self.default_word_files()
            self.revert_to_original()
            self.paragraph_generator = ParagraphsGenerator(self.get_state())
            message = ('On loading, caught the following error:\n{}: {}\n\n' +
                       'The original word files were moved to <name>_old_(number).csv and replaced with new files.')
            showerror('Bad start file', message.format(e.__class__.__name__, e.args[0]))

        for frame in self.frames:
            if isinstance(frame, FileManagement):
                frame.trace_file_names(self.update_paragraph_generator)

        self.do_not_show_popup = tk.IntVar()
        self.do_not_show_popup.set(0)

    def _pack_action_frame(self, action_frame):
        padx, pady = (20, 5)

        button_kwargs = [
            {'text': 'Save current settings', 'command': self.set_config, 'bg': 'CadetBlue1'},
            {'text': 'Reset to saved settings', 'command': self.load_config, 'bg': 'aquamarine2'},
            {},
            {'text': 'New default word files', 'command': self.default_word_files, 'bg': 'plum1'},
            {'text': 'Factory Reset', 'command': self.revert_to_original, 'bg': 'firebrick1'},
        ]
        for row, kwargs in enumerate(button_kwargs):
            if not kwargs:
                continue
            tk.Button(master=action_frame, **kwargs).grid(row=row, column=0, padx=padx, pady=pady)

        tk.Entry(master=action_frame, textvar=self.file_prefix).grid(row=0, column=1, sticky=tk.E, padx=2, pady=pady)
        self.font_size.grid(row=1, column=1, padx=2, pady=pady, sticky=tk.E)

        pdf_button = tk.Button(master=action_frame, text='Make me some PDFs',
                               command=self.create_texts, bg='chartreuse2')
        pdf_button.grid(row=2, column=1, padx=padx, pady=pady)

        tk.Label(master=action_frame, text='Add a file prefix').grid(row=0, column=2, padx=2, pady=pady, sticky=tk.W)
        tk.Label(master=action_frame, text='Font Size').grid(row=1, column=2, padx=2, pady=pady, sticky=tk.W)

        help_btn = tk.Button(master=action_frame, text='Help', command=self.read_me, bg='light blue')
        help_btn.grid(row=3, column=2, sticky=(tk.E,))

        action_frame.grid(row=0, column=0, columnspan=2)

    def _pack_set_variable_frames(self):
        error_details = ErrorDetails(master=self)
        error_details.set_bg('light cyan')

        paragraph_type = ParagraphType(master=self)
        paragraph_type.set_bg('honeydew2')

        grammar_details = GrammarDetails(master=self)
        grammar_details.set_bg('snow2')

        file_management = FileManagement(master=self)
        file_management.set_bg('light blue')

        expand_out = {'sticky': tk.N + tk.S + tk.E + tk.W}
        error_details.grid(row=1, column=0, rowspan=2, **expand_out)
        paragraph_type.grid(row=1, column=1, **expand_out)
        grammar_details.grid(row=2, column=1, **expand_out)
        file_management.grid(row=3, column=0, columnspan=2, **expand_out)

        return error_details, file_management, grammar_details, paragraph_type

    @catch_errors('Bad file')
    def update_paragraph_generator(self, *call_back_args):
        self.paragraph_generator.update_options(self.get_state())

    def reload_files(self):
        try:
            self.paragraph_generator.load_lists_from_file()
        except LoaderError as e:
            showerror('Bad file', '{}: {}'.format(e.__class__.__name__, e.args[0]))

    def default_word_files(self):
        home = self.get_state()['home_directory']
        create_default_word_files(home)

    def load_config(self):
        loader = ConfigLoader()
        self._load_local(loader.state)
        for frame in self.frames:
            loader.set_up_frame(frame)

    def _load_local(self, state):
        self.font_size.set_int(state['font_size'])
        file_prefix = state['file_prefix']
        self.file_prefix.set(file_prefix if file_prefix is not None else '')

    def set_config(self):
        save_config(self.get_state())

    def get_state(self):
        answer = {}
        for frame in self.frames:
            answer.update(frame.get_values())
        answer.update(self._get_local())
        return answer

    def _get_local(self):
        file_prefix = self.file_prefix.get().strip()
        if not file_prefix:
            file_prefix = None
        return {'font_size': self.font_size.get_int(), 'file_prefix': file_prefix}

    @catch_errors('Uh-oh!')
    def create_texts(self):
        state = self.get_state()
        file_prefix = self.file_prefix.get().strip()
        font_size = self.font_size.get_int()

        self.paragraph_generator.update_options(state)
        self.paragraph_generator.load_lists_from_file()
        answer, error = self.paragraph_generator.create_answer_and_error_paragraphs()
        create_pdf(state['save_directory'], answer, error,
                   error_font_size=font_size, named_prefix=file_prefix)

        if not self.do_not_show_popup.get():
            CancelableMessagePopup('success',
                                   'Your files are located at:\n{}'.format(self.get_state()['save_directory']),
                                   self.do_not_show_popup)

    def revert_to_original(self):
        loader = ConfigLoader()
        loader.revert_to_default()
        self.load_config()

    def read_me(self):
        popup = tk.Toplevel(self)

        scrollbar = tk.Scrollbar(popup)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_frame = ReadMeText(popup)

        text_frame.config(wrap=tk.WORD)
        text_frame.pack(expand=True, fill=tk.BOTH)

        text_frame.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_frame.yview)


def main_app():
    app = MainFrame()
    app.title('Go Time')
    app.mainloop()


if __name__ == '__main__':
    main_app()
