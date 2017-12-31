import os

from sentences.gui.gui_tools import SetVariablesFrame
from sentences import DATA_PATH, APP_NAME

DEFAULT_SAVE_DIR = 'pdfs'
COUNTABLE_NOUNS_CSV = 'nouns.csv'
UNCOUNTABLE_NOUNS_CSV = 'uncountable.csv'
VERBS_CSV = 'verbs.csv'

CONFIG_FILE = os.path.join(DATA_PATH, 'config.cfg')
DEFAULT_CONFIG = os.path.join(DATA_PATH, 'default.cfg')


class ConfigLoader(object):
    def __init__(self):
        try:
            self._dictionary = load_config(CONFIG_FILE)
        except (ValueError, OSError):
            create_default_config()
            self._dictionary = load_config(CONFIG_FILE)

        self._set_up_directories()
        self._set_up_word_files()

    def _set_up_directories(self):
        home_dir = self._dictionary['home_directory']
        save_dir = self._dictionary['save_directory']

        if home_dir is None:
            home_dir = os.path.join(get_documents_folder(), APP_NAME)
        if save_dir is None:
            save_dir = os.path.join(home_dir, DEFAULT_SAVE_DIR)

        if not os.path.exists(home_dir):
            os.mkdir(home_dir)
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        self._dictionary['home_directory'] = home_dir
        self._dictionary['save_directory'] = save_dir

    def _set_up_word_files(self):
        home_dir = self._dictionary['home_directory']
        file_keys = ['countable_nouns', 'uncountable_nouns', 'verbs']
        default_names = [COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV]
        for key, default_name in zip(file_keys, default_names):
            full_default_name = os.path.join(home_dir, default_name)

            filename = self._dictionary[key]
            if filename is None:
                filename = full_default_name

            while not os.path.exists(filename):
                if filename == full_default_name:
                    with open(os.path.join(DATA_PATH, default_name), 'r') as read_file:
                        with open(filename, 'w') as write_file:
                            write_file.write(read_file.read())
                else:
                    filename = full_default_name
            self._dictionary[key] = filename

    def reload(self):
        self._dictionary = load_config(CONFIG_FILE)
        self._set_up_directories()
        self._set_up_word_files()

    def save_and_reload(self, config_dict):
        save_config(config_dict)
        self.reload()

    def revert_to_default(self):
        app_folder = os.path.join(get_documents_folder(), APP_NAME)
        for filename in [COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV]:
            full_path = os.path.join(app_folder, filename)
            if os.path.exists(full_path):
                os.remove(full_path)
        create_default_config()
        self.reload()

    def set_up_frame(self, frame: SetVariablesFrame):
        for key, value in self._dictionary.items():
            try:
                frame.set_variable(key, value)
            except AttributeError:
                continue


def create_default_config():
    with open(DEFAULT_CONFIG, 'r') as default_file:
        default_text = default_file.read()

    with open(CONFIG_FILE, 'w') as target:
        target.write(default_text)


def save_config(dictionary):
    lines = _get_key_value_list(DEFAULT_CONFIG)
    to_write = []
    for key, value in lines:
        if not key or key.startswith('#'):
            to_write.append(key)
        else:
            if key in dictionary:
                value = dictionary[key]
            to_write.append(_create_line(key, value))
    with open(CONFIG_FILE, 'w') as f:
        f.write('\n'.join(to_write))


def load_config(config_file):
    key_val_list = _get_key_value_list(config_file)
    return {key: value for key, value in key_val_list if key and not key.startswith('#')}


def _get_key_value_list(config_file):
    with open(config_file, 'r') as f:
        lines = f.read().split('\n')
    answer = []
    for line in lines:
        if line.startswith('#'):
            answer.append((line, None))
        else:
            answer.append(_get_key_value(line))
    return answer


def _get_key_value(line):
    if not line.strip():
        return '', None
    key, value = line.split('=')
    key = key.strip()
    value = value.strip()
    if value.isdigit():
        return key, int(value)

    try:
        return key, float(value)
    except ValueError:
        pass

    special_strings = {'none': None, 'true': True, 'false': False}
    try:
        return key, special_strings[value.lower()]
    except KeyError:
        return key, value


def _create_line(key, value):
    value_str = str(value)
    if value_str in ['True', 'False', 'None']:
        value_str = value_str.lower()
    line = ' = '.join((key, value_str))
    return line


def get_documents_folder():
    user_location = os.path.expanduser('~')
    user_folder = os.listdir(user_location)
    if 'My Documents' in user_folder:
        return os.path.join(user_location, 'My Documents')
    elif 'Documents' in user_folder:
        return os.path.join(user_location, 'Documents')
    else:
        return user_location
