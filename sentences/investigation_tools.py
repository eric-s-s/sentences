from sentences.words.pronoun import Pronoun
from sentences.words.verb import Verb
from sentences.words.noun import Noun, PluralNoun

from sentences.loader import uncountable_nouns


def requires_third_person(raw_sentence) -> bool:
    index = find_subject(raw_sentence)
    if index == -1:
        return False
    return is_third_person(raw_sentence[index])


def find_subject(raw_sentence) -> int:
    index = -1
    for i, val in enumerate(raw_sentence):
        if isinstance(val, Verb):
            index = i - 1
            break
    return index


def is_third_person(word) -> bool:
    if isinstance(word, Pronoun):
        return word in (Pronoun.HE, Pronoun.HIM, Pronoun.SHE, Pronoun.HER, Pronoun.IT)
    if isinstance(word, Noun):
        return not isinstance(word, PluralNoun)
    return False


def is_countable(word) -> bool:
    basic_uncountable = uncountable_nouns()
    definite_uncountable = [noun.definite() for noun in basic_uncountable]
    return word not in (basic_uncountable + definite_uncountable)


def is_word_in_sentence(word, raw_sentence):
    if isinstance(word, Pronoun):
        return any(word.is_pair(element) for element in raw_sentence)
    return word in raw_sentence
