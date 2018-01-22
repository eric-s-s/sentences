import csv
import os

from sentences import DATA_PATH, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV

from sentences.words.noun import Noun, UncountableNoun, ProperNoun, PluralProperNoun
from sentences.words.verb import Verb
from sentences.words.word import Preposition


class LoaderError(ValueError):
    pass


def load_csv(filename):
    try:
        with open(filename, 'r', newline='') as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar='"', doublequote=True)
            raw = [row for row in csv_reader if row and not row[0].startswith('#')]
    except (OSError, UnicodeError):
        message = ('Could not read CSV file. If you edited it in MSWord or something similar, ' +
                   'it got formatted. Use "notepad"')
        raise LoaderError(message)
    else:
        return strip_spaces(raw)


def strip_spaces(rows):
    return [[word.strip() for word in row] for row in rows]


def countable_nouns(filename=''):
    return _nouns(filename, countable=True)


def uncountable_nouns(filename=''):
    return _nouns(filename, countable=False)


def _nouns(filename='', countable=True):
    if countable:
        class_ = Noun
        default = COUNTABLE_NOUNS_CSV
        columns = 2
    else:
        class_ = UncountableNoun
        default = UNCOUNTABLE_NOUNS_CSV
        columns = 1

    new_filename = _default_or_file_name(filename, default)
    raw_lines = load_csv(new_filename)

    return [class_(*line[:columns]) for line in raw_lines]


def proper_nouns(filename):
    raw_lines = load_csv(filename)
    return [_get_proper_noun_class(row)(row[0]) for row in raw_lines]


def _get_proper_noun_class(row):
    if len(row) < 2 or row[1] != 'p':
        return ProperNoun
    return PluralProperNoun


def verbs(filename=''):
    new_filename = _default_or_file_name(filename, VERBS_CSV)
    raw_lines = load_csv(new_filename)
    try:
        answer = [get_verb_dict(verb_line) for verb_line in raw_lines]
    except ValueError:
        raise LoaderError('Bad values in columns for CSV for verbs. See default for example.')
    return answer


def _default_or_file_name(file_name, default_name):
    if not file_name:
        file_name = os.path.join(DATA_PATH, default_name)
    return file_name


def get_verb_dict(str_lst):
    str_lst = _make_list_correct_len_with_nulls(str_lst)

    infinitive, past_tense, preposition_str, obj_num_str, insert_preposition = str_lst

    if past_tense == 'null':
        past_tense = ''
    verb = Verb(infinitive, past_tense, '')

    if preposition_str == 'null':
        preposition = None
    else:
        preposition = Preposition(preposition_str)

    if obj_num_str == 'null':
        obj_num = 1
    else:
        obj_num = int(obj_num_str)

    if insert_preposition.lower() == 'true':
        insert_bool = True
    else:
        insert_bool = False

    return {'verb': verb, 'preposition': preposition, 'objects': obj_num, 'insert_preposition': insert_bool}


def _make_list_correct_len_with_nulls(input_list):
    expected_len = 5
    diff = expected_len - len(input_list)
    output_list = input_list[:expected_len] + diff * ['null']

    return [value if value else 'null' for value in output_list]
