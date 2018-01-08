import os
from sentences import DATA_PATH, VERBS_CSV, UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV


def create_default_word_files(directory):
    for filename in (VERBS_CSV, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV):
        full_filename = os.path.join(directory, filename)
        if os.path.exists(full_filename):
            move_to_old(directory, filename)
        with open(os.path.join(DATA_PATH, filename), 'w') as read_file:
            with open(full_filename, 'w') as write_file:
                write_file.write(read_file.read())


def move_to_old(directory, filename):
    suffix = '_old_{:0>2}.csv'
    count = 0
    filename_already_exists = True
    save_destination = ''
    while filename_already_exists:
        count += 1
        use_filename = filename.replace('.csv', suffix.format(count))

        save_destination = os.path.join(directory, use_filename)
        filename_already_exists = os.path.exists(save_destination)

    with open(os.path.join(directory, filename), 'r') as read_file:
        with open(save_destination, 'w') as write_file:
            write_file.write(read_file.read())

    return save_destination
