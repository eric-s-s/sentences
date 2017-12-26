import os

from sentences import DATA_PATH



"""


"""
CONFIG_FILE = os.path.join(DATA_PATH, 'config.cfg')


def has_config_file():
    return os.path.exists(CONFIG_FILE)


def create_default_file():
    default_location = os.path.join(DATA_PATH, 'default.cfg')
    with open(default_location, 'r') as default_file:
        default_text = default_file.read()

    with open(CONFIG_FILE, 'w') as target:
        target.write(default_text)



