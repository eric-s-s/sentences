import random
from copy import deepcopy
from typing import List, Union

from sentences.backend.investigation_tools import requires_third_person, find_subject
from sentences.words.pronoun import AbstractPronoun
from sentences.words.punctuation import Punctuation
from sentences.words.noun import Noun
from sentences.words.verb import Verb
from sentences.words.wordtools.abstractword import AbstractWord
from sentences.words.wordtools.wordtag import WordTag

Paragraph = List[List[Union[AbstractWord, AbstractPronoun, Punctuation]]]


class Grammarizer(object):
    def __init__(self, paragraph: Paragraph, present_tense: bool = True,
                 probability_plural_noun: float = 0.3, probability_negative_verb: float = 0.3):
        self._raw = [sentence[:] for sentence in paragraph]

        self.present_tense = present_tense
        self._plural = normalize_probability(probability_plural_noun)
        self._negative = normalize_probability(probability_negative_verb)

        self._noun_info = None
        self.set_nouns()

    @property
    def noun_info(self):
        return deepcopy(self._noun_info)

    @property
    def plural(self):
        return self._plural

    @plural.setter
    def plural(self, new: float):
        self._plural = normalize_probability(new)

    @property
    def negative(self):
        return self._negative

    @negative.setter
    def negative(self, new: float):
        self._negative = normalize_probability(new)

    def reset_definite_nouns(self):
        for value in self._noun_info.values():
            value['definite'] = False

    def set_nouns(self):
        nouns = get_non_proper_nouns(self._raw)
        pool = {}
        for noun in nouns:
            use_plural = False
            countable = not noun.has_tags(WordTag.UNCOUNTABLE)
            if countable and random.random() < self._plural:
                use_plural = True
            pool[noun] = {'plural': use_plural, 'definite': False, 'countable': countable}
        self._noun_info = pool

    def generate_paragraph(self):
        self.reset_definite_nouns()
        answer = []
        for sentence in self._raw:
            new_sentence = []
            for original_wd in sentence:
                new_wd = original_wd

                if is_non_proper_noun(new_wd):
                    new_wd = self._modify_noun(new_wd)

                if isinstance(new_wd, Verb):
                    new_wd = self._assign_negatives(new_wd)

                new_sentence.append(new_wd)

            answer.append(new_sentence)

        for sentence in answer:
            self._modify_verb_tense(sentence)
            sentence[0] = sentence[0].capitalize()

        return answer

    def _modify_noun(self, new_wd):
        info = self._noun_info[new_wd]
        if info['plural']:
            new_wd = new_wd.plural()
        if info['definite']:
            new_wd = new_wd.definite()
        else:
            info['definite'] = True
            if info['countable'] and not new_wd.has_tags(WordTag.PLURAL):
                new_wd = new_wd.indefinite()
        return new_wd

    def _assign_negatives(self, new_wd):
        if random.random() < self._negative:
            new_wd = new_wd.negative()
        return new_wd

    def _modify_verb_tense(self, sentence):
        verb_index = find_subject(sentence) + 1
        if self.present_tense:
            if requires_third_person(sentence):
                sentence[verb_index] = sentence[verb_index].third_person()
        else:
            sentence[verb_index] = sentence[verb_index].past_tense()


def normalize_probability(probability: float):
    return min(1.0, max(probability, 0))


def get_non_proper_nouns(paragraph: Paragraph) -> list:
    answer = []
    for sentence in paragraph:
        for word in sentence:
            if is_non_proper_noun(word) and word not in answer:  # Sets and random choice are untestable
                answer.append(word)
    return answer


def is_non_proper_noun(word):
    return isinstance(word, Noun) and not word.has_tags(WordTag.PROPER)
