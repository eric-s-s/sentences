import os

from sentences.text_to_pdf import create_pdf, get_file_prefix
from sentences.generate_text import generate_text

APP_NAME = 'sentence_mangler'

FILE_NAME = APP_NAME + '.cfg'

def get_default_dir():
    base_dir = os.path.expanduser('~')
    home = APP_NAME
    full_path = os.path.join(base_dir, home)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    return full_path


class ConfigLoader(object):
    def __init__(self, dir_location=''):
        if not dir_location:
            dir_location = get_default_dir()
        if not config_file_exists(dir_location):
            self._create_config(dir_location)

        self._dir = dir_location

    @staticmethod
    def _create_config(location):
        with open('./' + FILE_NAME, 'r') as r_file:
            text = r_file.read()
        with open(full_file_name(location), 'w') as w_file:
            w_file.write(text)

    @property
    def location(self):
        return self._dir

    def get_text(self):
        with open(full_file_name(self._dir), 'r') as f:
            text = f.read()
        return text


def config_file_exists(directory):
    if not directory:
        return False
    file_name = full_file_name(directory)
    return os.path.exists(file_name)


def full_file_name(directory):
    if '\\' in directory and not directory.endswith('\\'):
        file_name = directory + '\\' + FILE_NAME
    elif '/' in directory and not directory.endswith('/'):
        file_name = directory + '/' + FILE_NAME
    else:
        file_name = directory + FILE_NAME
    return file_name

