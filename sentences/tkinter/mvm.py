import os

from sentences import DATA_PATH, APP_NAME

from sentences.text_to_pdf import create_pdf, get_file_prefix
from sentences.generate_text import generate_text

CONFIG_NAME = APP_NAME + '.cfg'


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
        default_config_file = os.path.join(DATA_PATH, 'default.cfg')
        target = os.path.join(location, CONFIG_NAME)
        with open(default_config_file, 'r') as r_file:
            text = r_file.read()
        with open(target, 'w') as w_file:
            w_file.write(text)

    @property
    def location(self):
        return self._dir

    def get_text(self):
        with open(os.path.join(self._dir, CONFIG_NAME), 'r') as f:
            text = f.read()
        return text


def config_file_exists(directory):
    if not directory:
        return False
    file_name = os.path.join(directory, CONFIG_NAME)
    return os.path.exists(file_name)
