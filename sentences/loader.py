import os

from sentences import DATA_PATH

from sentences.words.noun import Noun, UncountableNoun
from sentences.words.verb import BasicVerb
from sentences.words.word import Word


def load_csv(filename):
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
    return [split_and_strip(line) for line in lines if line.strip() and not line.startswith('#')]


def split_and_strip(line):
    return [word.strip() for word in line.split(',')]


def countable_nouns(filename=''):
    new_filename = _default_or_file_name(filename, 'nouns.csv')
    raw_lines = load_csv(new_filename)
    return [Noun(*line) for line in raw_lines]


def uncountable_nouns(filename=''):
    new_filename = _default_or_file_name(filename, 'uncountable.csv')
    raw_lines = load_csv(new_filename)
    return [UncountableNoun(*line) for line in raw_lines]


def verbs(filename=''):
    new_filename = _default_or_file_name(filename, 'verbs.csv')
    raw_lines = load_csv(new_filename)
    return [get_verb_dict(verb_line) for verb_line in raw_lines]


def _default_or_file_name(file_name, default_name):
    if not file_name:
        file_name = os.path.join(DATA_PATH, default_name)
    return file_name


def get_verb_dict(str_lst, intransitive=False):
    inf = str_lst[0]
    past = str_lst[1]
    if past == 'null':
        past = ''
    verb = BasicVerb(inf, past)

    prep = str_lst[2]
    if prep == 'null':
        preposition = None
    else:
        preposition = Word(prep)

    if intransitive:
        obj_num = 0
    elif len(str_lst) > 3:
        obj_num = int(str_lst[3])
    else:
        obj_num = 1

    if len(str_lst) >= 5 and str_lst[4].lower() == 'true':
        insert_preposition = True
    else:
        insert_preposition = False

    return {'verb': verb, 'preposition': preposition, 'objects': obj_num, 'insert_preposition': insert_preposition}
