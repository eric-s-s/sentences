from sentences.words.pronoun import Pronoun, CapitalPronoun, AbstractPronoun
from sentences.words.verb import Verb
from sentences.words.noun import Noun
from sentences.words.basicword import BasicWord
from sentences.tags.wordtag import WordTag


def get_present_be_verb(sentence):
    subj_index = find_subject(sentence)
    if subj_index == -1:
        return BasicWord('be')
    subj = sentence[subj_index]
    if requires_third_person(sentence):
        return BasicWord('is')
    elif subj in (Pronoun.I, Pronoun.ME, CapitalPronoun.I, CapitalPronoun.ME):
        return BasicWord('am')
    else:
        return BasicWord('are')


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
    first_person = [Pronoun.I, Pronoun.ME, CapitalPronoun.I, CapitalPronoun.ME]
    if isinstance(word, (Noun, AbstractPronoun)) and word not in first_person:
        return not word.has_tags(WordTag.PLURAL)
    return False
