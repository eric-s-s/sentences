import os
from sentences import DATA_PATH, VERBS_CSV, UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV


def create_default_word_files(directory):
    for filename in (VERBS_CSV, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV):
        full_filename = os.path.join(directory, filename)
        if os.path.exists(full_filename):
            copy_to_numbered_old_file(directory, filename)
        with open(os.path.join(DATA_PATH, filename), 'r') as read_file:
            with open(full_filename, 'w') as write_file:
                write_file.write(read_file.read())


def copy_to_numbered_old_file(directory, filename):
    suffix = '_old_{:0>2}.csv'
    count = 0
    filename_already_exists = True
    save_destination = ''
    while filename_already_exists:
        count += 1
        use_filename = filename.replace('.csv', suffix.format(count))

        save_destination = os.path.join(directory, use_filename)
        filename_already_exists = os.path.exists(save_destination)

    try:
        with open(os.path.join(directory, filename), 'r') as read_file:
            to_write = read_file.read()
    except (OSError, UnicodeError):
        to_write = ''

    with open(save_destination, 'w') as write_file:
        write_file.write(to_write)

    return save_destination
