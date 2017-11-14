import random
from typing import List, Union

from sentences.investigation_tools import requires_third_person, is_countable, find_subject

from sentences.words.word import Word
from sentences.words.verb import BasicVerb
from sentences.words.noun import Noun, PluralNoun
from sentences.words.punctuation import Punctuation
from sentences.words.pronoun import Pronoun


Paragraph = List[List[Union[Word, Pronoun, Punctuation]]]


class Grammarizer(object):
    def __init__(self, paragraph: Paragraph, present_tense: bool = True, p_plural: float = 0.3, p_negative: float = 0.3):
        self._raw = paragraph
        self._nouns = get_nouns(paragraph)
        self._present_tense = present_tense
        self._plural = normalize_probability(p_plural)
        self._negative = normalize_probability(p_negative)

    def _create_subject_pool(self):
        pool = {}
        for subj in self._nouns:
            use_plural = False
            countable = is_countable(subj)
            if random.random() < self._plural and countable:
                use_plural = True
            pool[subj] = {'plural': use_plural, 'definite': False, 'countable': countable}
        return pool

    def generate_paragraph(self):
        subj_info = self._create_subject_pool()
        answer = []
        for index, sentence in enumerate(self._raw):
            new_sentence = []
            for element in sentence:
                new_wd = element

                if isinstance(new_wd, Noun):
                    info = subj_info[element]
                    if info['plural']:
                        new_wd = new_wd.plural()

                    if info['definite']:
                        new_wd = new_wd.definite()
                    else:
                        info['definite'] = True
                        if info['countable'] and not isinstance(new_wd, PluralNoun):
                            new_wd = new_wd.indefinite()

                if isinstance(new_wd, BasicVerb):
                    if random.random() < self._negative:
                        new_wd = new_wd.negative()

                new_sentence.append(new_wd)
            answer.append(new_sentence)
        for sentence in answer:
            verb_index = find_subject(sentence) + 1
            if self._present_tense:
                if requires_third_person(sentence):
                    sentence[verb_index] = sentence[verb_index].third_person()
            else:
                sentence[verb_index] = sentence[verb_index].past_tense()
            sentence[0] = sentence[0].capitalize()

        return answer


def normalize_probability(probability: float):
    return min(1.0, max(probability, 0))


def get_nouns(paragraph: Paragraph) -> set:
    answer = set()
    for sentence in paragraph:
        for word in sentence:
            if isinstance(word, Noun):
                answer.add(word)
    return answer

