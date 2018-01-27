import csv

from sentences.words.noun import Noun, UncountableNoun, ProperNoun, PluralProperNoun
from sentences.words.verb import Verb
from sentences.words.word import Preposition, SeparableParticle


class LoaderError(ValueError):
    pass


def load_csv(filename):
    try:
        with open(filename, 'r', newline='') as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar='"', doublequote=True, skipinitialspace=True)
            raw = [row for row in csv_reader if row and not row[0].startswith('#')]
    except (OSError, UnicodeError):
        message = ('Could not read CSV file. If you edited it in MSWord or something similar, ' +
                   'it got formatted. Use "notepad"')
        raise LoaderError(message)
    else:
        answer = strip_spaces(raw)
        return remove_empty_values(answer)


def strip_spaces(rows):
    return [[word.strip() for word in row] for row in rows]


def remove_empty_values(rows):
    return [row for row in rows if not all(word == '' for word in row)]


def countable_nouns(filename=''):
    return _nouns(filename, countable=True)


def uncountable_nouns(filename=''):
    return _nouns(filename, countable=False)


def _nouns(filename, countable=True):
    if countable:
        class_ = Noun
        columns = 2
    else:
        class_ = UncountableNoun
        columns = 1

    raw_lines = load_csv(filename)
    return [class_(*line[:columns]) for line in raw_lines]


def proper_nouns(filename):
    raw_lines = load_csv(filename)
    return [_get_proper_noun_class(row)(row[0]) for row in raw_lines]


def _get_proper_noun_class(row):
    if len(row) < 2 or row[1] != 'p':
        return ProperNoun
    return PluralProperNoun


def verbs(filename):
    raw_lines = load_csv(filename)
    try:
        answer = [get_verb_dict(verb_line) for verb_line in raw_lines]
    except ValueError:
        raise LoaderError('Bad values in columns for CSV for verbs. See default for example.')
    return answer


def get_verb_dict(str_lst):
    str_lst = _make_list_correct_len_with_nulls(str_lst)

    raw_infinitive, raw_past, preposition_str, obj_num_str = str_lst

    infinitive, particle_inf = split_verb(raw_infinitive)
    past_tense, particle_past = split_verb(raw_past)

    _raise_error_for_bad_particles(particle_inf, particle_past, infinitive)

    if past_tense == 'null':
        past_tense = ''
    verb = Verb(infinitive, past_tense, '')

    if particle_inf == '':
        particle = None
    else:
        particle = SeparableParticle(particle_inf)

    if preposition_str == 'null':
        preposition = None
    else:
        preposition = Preposition(preposition_str)

    if obj_num_str == 'null':
        obj_num = 1
    else:
        obj_num = int(obj_num_str)

    return {'verb': verb, 'preposition': preposition, 'objects': obj_num, 'particle': particle}


def _make_list_correct_len_with_nulls(input_list):
    expected_len = 4
    diff = expected_len - len(input_list)
    output_list = input_list[:expected_len] + diff * ['null']

    return [value if value else 'null' for value in output_list]


def split_verb(raw_str):
    parts = raw_str.split(' ')
    verb = parts[0]
    particle = ''
    if len(parts) > 1:
        particle = parts[1]
    return verb, particle


def _raise_error_for_bad_particles(particle_inf, particle_past, infinitive):
    if particle_past and particle_inf != particle_past:
        raise LoaderError('Phrasal verb, {}, has mismatched particles'.format(infinitive))
