from sentences.words.noun import Noun


def load_csv(filename):
    with open('word_lists/' + filename, 'r') as f:
        lines = f.read().split('\n')
    return [line.split(', ') for line in lines[1:] if line]


def countable_nouns():
    raw_lines = load_csv('nouns.csv')
    return [Noun(*line) for line in raw_lines]


def uncountable_nouns():
    raw_lines = load_csv('uncountable.csv')
    return [Noun(*line) for line in raw_lines]


def get_noun(lst):
    if len(lst) == 1:
        return Noun(lst[0])
    return Noun(*lst)