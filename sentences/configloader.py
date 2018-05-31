import os

from sentences.gui.gui_tools import SetVariablesFrame
from sentences import (DATA_PATH, APP_NAME, DEFAULT_CONFIG, VERBS_CSV,
                       COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, PROPER_NOUNS_CSV, ConfigFileError)

DEFAULT_SAVE_DIR = 'pdfs'
CONFIG_FILE = os.path.join(DATA_PATH, 'config.cfg')


class ConfigLoader(object):
    def __init__(self):
        try:
            self._dictionary = load_config(CONFIG_FILE)
        except (ValueError, OSError):
            create_default_config()
            self._dictionary = load_config(CONFIG_FILE)

        self._set_up_directories()
        self._set_up_word_files()
        self._create_empty_csv()

    def set_state_from_file(self, filename):
        try:
            self._dictionary.update(load_config(filename))
        except (ValueError, OSError) as error:
            msg = 'Error loading file. Original error:\n{}: {}'
            raise ConfigFileError(msg.format(error.__class__.__name__, error))

        self._set_up_directories()
        self._set_up_word_files()

    @property
    def state(self):
        return self._dictionary.copy()

    def _set_up_directories(self):
        home_dir = self._dictionary['home_directory']
        save_dir = self._dictionary['save_directory']

        if home_dir is None:
            home_dir = os.path.join(get_documents_folder(), APP_NAME)
        if save_dir is None:
            save_dir = os.path.join(home_dir, DEFAULT_SAVE_DIR)

        def create_if_not_exists(directory_name):
            if not os.path.exists(directory_name):
                try:
                    os.mkdir(directory_name)
                except OSError as error:
                    msg = 'Config Loader failed to create the following directory:\n{}\nOriginal error message:\n'
                    msg += '{}: {}'.format(error.__class__.__name__, error)
                    raise ConfigFileError(msg.format(os.path.abspath(directory_name)))

        create_if_not_exists(home_dir)
        create_if_not_exists(save_dir)

        self._dictionary['home_directory'] = home_dir
        self._dictionary['save_directory'] = save_dir

    def _create_empty_csv(self):
        home_dir = self._dictionary['home_directory']
        with open(os.path.join(home_dir, 'EMPTY.csv'), 'w') as f:
            f.write('')

    def _set_up_word_files(self):
        home_dir = self._dictionary['home_directory']
        file_keys = ['countable_nouns', 'uncountable_nouns', 'proper_nouns', 'verbs']
        default_names = [COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, PROPER_NOUNS_CSV, VERBS_CSV]
        for key, default_name in zip(file_keys, default_names):
            full_default_name = os.path.join(home_dir, default_name)

            filename = self._dictionary[key]
            if filename is None:
                filename = full_default_name

            if not os.path.exists(filename):
                filename = full_default_name
                with open(os.path.join(DATA_PATH, default_name), 'r') as read_file:
                    with open(filename, 'w') as write_file:
                        write_file.write(read_file.read())
            self._dictionary[key] = filename

    def reload(self):
        self._dictionary = load_config(CONFIG_FILE)
        self._set_up_directories()
        self._set_up_word_files()

    def revert_to_default(self):
        default_home_path = os.path.join(get_documents_folder(), APP_NAME)
        for filename in [COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV]:
            default_csv_path = os.path.join(default_home_path, filename)
            if os.path.exists(default_csv_path):
                os.remove(default_csv_path)
        create_default_config()
        self.reload()

    def set_up_frame(self, frame: SetVariablesFrame):
        for key, value in self._dictionary.items():
            try:
                frame.set_variable(key, value)
            except AttributeError:
                continue
            except ValueError:
                msg = 'Tried to set key: {!r} to incompatible value: {!r}.'.format(key, value)
                raise ConfigFileError(msg)


def create_default_config():
    with open(DEFAULT_CONFIG, 'r') as default_file:
        default_text = default_file.read()

    with open(CONFIG_FILE, 'w') as target:
        target.write(default_text)


def save_config(dictionary):
    save_config_to_filename(dictionary, CONFIG_FILE)


def save_config_to_filename(dictionary, filename):
    lines = get_key_value_pairs(DEFAULT_CONFIG)
    to_write = []
    for key, value in lines:
        if not key or key.startswith('#'):
            to_write.append(key)
        else:
            if key in dictionary:
                value = dictionary[key]
            to_write.append(create_config_text_line(key, value))
    with open(filename, 'w') as f:
        f.write('\n'.join(to_write))


def load_config(config_file):
    key_val_list = get_key_value_pairs(config_file)
    return {key: value for key, value in key_val_list if key and not key.startswith('#')}


def get_key_value_pairs(config_file):
    with open(config_file, 'r') as f:
        lines = f.read().split('\n')
    return [get_single_key_value_pair(line) for line in lines]


def get_single_key_value_pair(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return line, None
    key, value = line.split('=')
    key = key.strip()
    value = value.strip()
    if value.isdigit():
        return key, int(value)

    try:
        return key, float(value)
    except ValueError:
        pass

    special_strings = {'none': None, 'true': True, 'false': False, 'empty_string': ''}
    try:
        return key, special_strings[value.lower()]
    except KeyError:
        return key, value


def create_config_text_line(key, value):
    value_str = str(value)
    if value_str == '':
        value_str = 'empty_string'
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
