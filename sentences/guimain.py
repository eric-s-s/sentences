import tkinter as tk
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
from sentences.gui.gui_tools import IntSpinBox


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.iconbitmap(os.path.join(DATA_PATH, 'go_time.ico'))

        action_frame = tk.Frame(master=self)
        self.font_size = IntSpinBox(master=action_frame, range_=(2, 20))
        self.font_size.set_int(13)

        self._pack_action_frame(action_frame)

        self.frames = self._pack_set_variable_frames()
        self.load_config()

        self.paragraph_generator = ParagraphsGenerator(self.get_state())

    def _pack_action_frame(self, action_frame):
        padx, pady = (20, 2)
        tk.Button(master=action_frame, text='Save current settings', command=self.set_config).grid(
            row=0, column=0, padx=padx, pady=pady)
        tk.Button(master=action_frame, text='Reset to saved settings', command=self.load_config).grid(
            row=1, column=0, padx=padx, pady=pady)
        tk.Button(master=action_frame, text='Update from word files', command=self.reload_files).grid(
            row=2, column=0, padx=padx, pady=pady)
        tk.Button(master=action_frame, text='New default word files', command=self.default_word_files).grid(
            row=3, column=0, padx=padx, pady=pady)
        tk.Button(master=action_frame, text='Factory Reset', command=self.revert_to_original).grid(
            row=4, column=0, padx=padx, pady=pady)
        tk.Label(master=action_frame, text='Font Size').grid(row=0, column=1, padx=padx, pady=pady)
        self.font_size.grid(row=1, column=1, padx=padx, pady=pady)
        tk.Button(master=action_frame, text='Make me some PDFs', command=self.create_texts).grid(
            row=2, column=1, padx=padx, pady=pady)
        action_frame.grid(row=0, column=0, columnspan=2)

    def _pack_set_variable_frames(self):
        error_details = ErrorDetails(master=self)
        error_details.set_bg('light yellow2')

        paragraph_type = ParagraphType(master=self)
        paragraph_type.set_bg('light cyan')

        grammar_details = GrammarDetails(master=self)
        grammar_details.set_bg('thistle1')

        file_management = FileManagement(master=self)
        file_management.set_bg('light blue')

        expand_out = {'sticky': tk.N + tk.S + tk.E + tk.W}
        error_details.grid(row=1, column=0, rowspan=2, **expand_out)
        paragraph_type.grid(row=1, column=1, **expand_out)
        grammar_details.grid(row=2, column=1, **expand_out)
        file_management.grid(row=3, column=0, columnspan=2, **expand_out)
        return error_details, file_management, grammar_details, paragraph_type

    def reload_files(self):
        self.paragraph_generator.load_lists_from_file()

    def default_word_files(self):
        home = self.get_state()['home_directory']
        create_default_word_files(home)

    def load_config(self):
        loader = ConfigLoader()
        for frame in self.frames:
            loader.set_up_frame(frame)

    def set_config(self):
        save_config(self.get_state())

    def get_state(self):
        answer = {}
        for frame in self.frames:
            answer.update(frame.get_values())
        return answer

    def create_texts(self):
        state = self.get_state()
        self.paragraph_generator.update_options(state)
        answer, error = self.paragraph_generator.create_answer_and_error_paragraphs()
        create_pdf(state['save_directory'], answer, error, error_font_size=self.font_size.get_int())

    def revert_to_original(self):
        loader = ConfigLoader()
        loader.revert_to_default()
        self.load_config()


def main_app():
    app = MainFrame()
    app.title('Go Time')
    app.mainloop()


if __name__ == '__main__':
    main_app()
