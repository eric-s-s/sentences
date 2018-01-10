import os

from sentences import DATA_PATH, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV

from sentences.words.noun import Noun, UncountableNoun
from sentences.words.verb import Verb
from sentences.words.word import Preposition


def load_csv(filename):
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
    return [split_and_strip(line) for line in lines if line.strip() and not line.startswith('#')]


def split_and_strip(line):
    return [word.strip() for word in line.split(',')]


def countable_nouns(filename=''):
    new_filename = _default_or_file_name(filename, COUNTABLE_NOUNS_CSV)
    raw_lines = load_csv(new_filename)
    return [Noun(*line) for line in raw_lines]


def uncountable_nouns(filename=''):
    new_filename = _default_or_file_name(filename, UNCOUNTABLE_NOUNS_CSV)
    raw_lines = load_csv(new_filename)
    return [UncountableNoun(*line) for line in raw_lines]


def verbs(filename=''):
    new_filename = _default_or_file_name(filename, VERBS_CSV)
    raw_lines = load_csv(new_filename)
    return [get_verb_dict(verb_line) for verb_line in raw_lines]


def _default_or_file_name(file_name, default_name):
    if not file_name:
        file_name = os.path.join(DATA_PATH, default_name)
    return file_name


def get_verb_dict(str_lst):
    str_lst = _make_list_correct_len_with_nulls(str_lst)

    infinitive, past_tense, preposition_str, obj_num_str, insert_preposition = str_lst

    if past_tense == 'null':
        past_tense = ''
    verb = Verb(infinitive, '', past_tense)

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
    output_list = input_list[:] + diff * ['null']

    return [value if value else 'null' for value in output_list]
