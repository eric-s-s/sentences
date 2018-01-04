import tkinter as tk
import os

from sentences import DATA_PATH

from sentences.create_pdf import create_pdf
from sentences.configloader import ConfigLoader
from sentences.paragraphsgenerator import ParagraphsGenerator
from sentences.configloader import save_config

from sentences.gui.errordetails import ErrorDetails
from sentences.gui.paragraphtype import ParagraphType
from sentences.gui.grammardetails import GrammarDetails
from sentences.gui.filemanagement import FileManagement


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.iconbitmap(os.path.join(DATA_PATH, 'go_time.ico'))
        error = ErrorDetails(master=self)
        ptype = ParagraphType(master=self)
        gd = GrammarDetails(master=self)
        fm = FileManagement(master=self)

        self.frames = (error, ptype, gd, fm)
        self.load_frames()

        self.pg = ParagraphsGenerator(self.get_state())

        action_frame = tk.Frame(master=self)
        tk.Button(master=action_frame, text='reload files', command=self.reload_files).pack()
        tk.Button(master=action_frame, text='reload config', command=self.reload_config).pack()
        tk.Button(master=action_frame, text='set_config', command=self.set_config).pack()
        tk.Button(master=action_frame, text='create_texts', command=self.create_texts).pack()
        tk.Button(master=action_frame, text='revert', command=self.revert_to_original).pack()
        action_frame.pack()
        for frame in self.frames:
            frame.pack()

    def load_frames(self):
        config = ConfigLoader()
        for frame in self.frames:
            config.set_up_frame(frame)

    def reload_files(self):
        self.pg.load_lists_from_file()

    def reload_config(self):
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
        self.pg.update_options(state)
        answer, error = self.pg.create_answer_and_error_paragraphs()
        create_pdf(state['save_directory'], answer, error)

    def revert_to_original(self):
        loader = ConfigLoader()
        loader.revert_to_default()
        self.reload_config()


def main_app():
    app = MainFrame(screenName='GO TIME', baseName='GO TIME', className='Go time')
    app.mainloop()


if __name__ == '__main__':
    main_app()
