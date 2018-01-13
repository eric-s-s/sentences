import csv
import os
import sys
from sentences.configloader import ConfigLoader


def load_file(file_name):
    with open(file_name, 'r', newline='') as f:
        reader = csv.reader(f)
        new_lst = sorted([lst for lst in reader if lst])
    return new_lst


def write_file(file_name, lst):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        for line in lst:
            writer.writerow(line)


def alphabetize(file_name, replace=True):
    if not os.path.exists(file_name):
        loader = ConfigLoader()
        file_name = os.path.join(loader.state['home_directory'], file_name)
    lst = load_file(file_name)
    if replace:
        new_name = file_name
    else:
        new_name = file_name.replace('.csv', '_sorted.csv')

    write_file(new_name, lst)


if __name__ == '__main__':
    alphabetize(sys.argv[1])
