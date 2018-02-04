from sentences.words.pronoun import Pronoun, CapitalPronoun
from sentences.words.new_verb import NewVerb
from sentences.words.new_word import NewNoun
from sentences.words.basicword import BasicWord
from sentences.words.wordtools.wordtag import WordTag


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
        if isinstance(val, NewVerb):
            index = i - 1
            break
    return index


def is_third_person(word) -> bool:
    if isinstance(word, NewNoun):
        return not word.has_tags(WordTag.PLURAL)
    pronouns = [Pronoun.HE, Pronoun.HIM, Pronoun.SHE, Pronoun.HER, Pronoun.IT]
    capitals = [CapitalPronoun.HE, CapitalPronoun.HIM, CapitalPronoun.SHE, CapitalPronoun.HER, CapitalPronoun.IT]
    return word in pronouns or word in capitals


def is_word_in_sentence(word, raw_sentence):
    if isinstance(word, Pronoun):
        return any(word.is_pair(element) for element in raw_sentence)
    return word in raw_sentence
