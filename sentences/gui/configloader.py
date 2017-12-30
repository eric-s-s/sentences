import os

from sentences import DATA_PATH, APP_NAME



"""
    def generate_default_csv_files(self):
        self.move_old_files_to_new_location()
        for filename in DEFAULT_CSVS:
            default_filename = os.path.join(DATA_PATH, filename)
            target_filename = os.path.join(self.home_directory.get(), filename)
            with open(default_filename, 'r') as read_file:
                with open(target_filename, 'w') as write_file:
                    write_file.write(read_file.read())
        self._set_default_csv_values()

    def move_old_files_to_new_location(self):
        home_folder = self.home_directory.get()
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

"""
CONFIG_FILE = os.path.join(DATA_PATH, 'config.cfg')


def has_config_file():
    return os.path.exists(CONFIG_FILE)


def create_default_config():
    default_location = os.path.join(DATA_PATH, 'default.cfg')
    with open(default_location, 'r') as default_file:
        default_text = default_file.read()

    with open(CONFIG_FILE, 'w') as target:
        target.write(default_text)


def get_documents_folder():
    user_location = os.path.expanduser('~')
    user_folder = os.listdir(user_location)
    if 'My Documents' in user_folder:
        return os.path.join(user_location, 'My Documents')
    elif 'Documents' in user_folder:
        return os.path.join(user_location, 'Documents')
    else:
        return user_location


def get_key_value_list(config_file):
    with open(config_file, 'r') as f:
        lines = f.read().split('\n')
    answer = []
    for line in lines:
        if line.startswith('#'):
            answer.append((line, None))
        else:
            answer.append(get_key_value(line))
    return answer


def get_key_value(line):
    if not line.strip():
        return None, None
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

# class ConfigLoader(object):
#     def __init__(self):
#         if not has_config_file():
#             create_default_config()
#
#         self.dictionary = self._load_config
