import csv


def load_file(file_name):
    with open('data/' + file_name, 'r', newline='') as f:
        reader = csv.reader(f)
        new_lst = sorted([lst for lst in reader if lst])
    return new_lst


def write_file(file_name, lst):
    with open('data/' + file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        for line in lst:
            writer.writerow(line)


def alphabetize(file_name, replace=False):
    lst = load_file(file_name)
    if replace:
        new_name = file_name
    else:
        new_name = file_name.replace('.csv', '_sorted.csv')

    write_file(new_name, lst)


if __name__ == '__main__':
    filename = 'uncountable.csv'
    alphabetize(filename, True)