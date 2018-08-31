from functools import wraps
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.filedialog import asksaveasfilename, askopenfilename
import os

from sentences import DATA_PATH

from sentences.create_pdf import create_pdf
from sentences.configloader import ConfigLoader, save_config, save_config_to_filename, ConfigFileError
from sentences.paragraphsgenerator import ParagraphsGenerator
from sentences.backend.create_word_files import create_default_word_files

from sentences.gui.errordetails import ErrorDetails
from sentences.gui.paragraphtype import ParagraphType
from sentences.gui.grammardetails import GrammarDetails
from sentences.gui.filemanagement import FileManagement
from sentences.gui.actions import Actions
from sentences.gui.gui_tools import CancelableMessagePopup
from sentences.gui.readme_text import ReadMeText

from sentences.backend.loader import LoaderError


def catch_errors(title, extra_message=''):
    def decorator(func):
        @wraps(func)
        def catch_wrapper(*args):
            try:
                return func(*args)
            except (ConfigFileError, ValueError, LoaderError) as e:
                message = extra_message + '{}: {}'.format(e.__class__.__name__, e.args[0])
                showerror(title, message)

        return catch_wrapper
    return decorator


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)

        try:
            self.wm_iconbitmap(os.path.join(DATA_PATH, 'go_time.ico'))
        except tk.TclError:
            pass

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

    def _pack_set_variable_frames(self):
        error_details = ErrorDetails(master=self)
        error_details.set_bg('light cyan')

        paragraph_type = ParagraphType(master=self)
        paragraph_type.set_bg('honeydew2')

        grammar_details = GrammarDetails(master=self)
        grammar_details.set_bg('snow2')

        file_management = FileManagement(master=self)
        file_management.set_bg('light blue')

        action_frame = Actions(master=self)
        actions = [
            (action_frame.save_settings, self.set_config),
            (action_frame.export_settings, self.export_config_file),
            (action_frame.reload_config, self.load_config),
            (action_frame.load_config_file, self.load_config_from_file),
            (action_frame.default_word_files, self.default_word_files),
            (action_frame.factory_reset, self.revert_to_original),
            (action_frame.make_pdfs, self.create_texts),
            (action_frame.read_me, self.read_me)
        ]
        for btn, command in actions:
            btn.config(command=command)

        expand_out = {'sticky': tk.N + tk.S + tk.E + tk.W}
        action_frame.grid(row=0, column=0, columnspan=2)
        error_details.grid(row=1, column=0, rowspan=2, **expand_out)
        paragraph_type.grid(row=1, column=1, **expand_out)
        grammar_details.grid(row=2, column=1, **expand_out)
        file_management.grid(row=3, column=0, columnspan=2, **expand_out)

        return error_details, file_management, grammar_details, paragraph_type, action_frame

    @catch_errors('Bad file')
    def update_paragraph_generator(self, *call_back_args):
        self.paragraph_generator.update_options(self.get_state())

    @catch_errors('Bad file')
    def reload_files(self):
        self.paragraph_generator.load_lists_from_file()

    def default_word_files(self):
        home = self.get_state()['home_directory']
        create_default_word_files(home)

    @catch_errors('bad config')
    def load_config(self):
        loader = ConfigLoader()
        self._load_new_state(loader)

    @catch_errors('bad config file')
    def load_config_from_file(self):
        loader = ConfigLoader()

        filename = askopenfilename(initialdir=self.get_state()['home_directory'], title='select .cfg file',
                                   defaultextension='.cfg')
        if not filename:
            return None

        loader.set_state_from_file(filename)
        self._load_new_state(loader)

    def _load_new_state(self, loader):
        try:
            for frame in self.frames:
                loader.set_up_frame(frame)
        except ConfigFileError as error:
            self.revert_to_original()
            raise ConfigFileError(error.args[0])

    def export_config_file(self):
        filename = asksaveasfilename(initialdir=self.get_state()['home_directory'], title='select .cfg file',
                                     initialfile='exported_config.cfg', defaultextension='.cfg')
        if not filename:
            return None
        save_config_to_filename(self.get_state(), filename)

    def set_config(self):
        save_config(self.get_state())

    def get_state(self):
        answer = {}
        for frame in self.frames:
            answer.update(frame.get_values())
        return answer

    @catch_errors('Uh-oh!')
    def create_texts(self):
        state = self.get_state()
        file_prefix = state['file_prefix']
        font_size = state['font_size']

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
