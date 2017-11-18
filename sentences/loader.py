from sentences.words.noun import Noun
from sentences.words.verb import BasicVerb
from sentences.words.word import Word


def load_csv(filename):
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
    return [split_and_strip(line) for line in lines[1:] if line.strip()]


def split_and_strip(line):
    return [word.strip() for word in line.split(',')]


def countable_nouns(filename=''):
    if not filename:
        filename = 'word_lists/nouns.csv'
    raw_lines = load_csv(filename)
    return [Noun(*line) for line in raw_lines]


def uncountable_nouns(filename=''):
    if not filename:
        filename = 'word_lists/uncountable.csv'
    raw_lines = load_csv(filename)
    return [Noun(*line) for line in raw_lines]


def verbs(filename=''):
    if not filename:
        filename = 'word_lists/verbs.csv'
    raw_lines = load_csv(filename)
    return [get_verb_dict(verb_line) for verb_line in raw_lines]


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

    return {'verb': verb, 'preposition': preposition, 'objects': obj_num}
