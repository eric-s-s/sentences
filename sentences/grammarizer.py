import random
from typing import List, Union

from sentences.investigation_tools import requires_third_person, is_word_in_sentence, is_countable, find_subject

from sentences.words.word import Word
from sentences.words.verb import BasicVerb
from sentences.words.noun import Noun, IndefiniteNoun, DefiniteNoun, PluralNoun, DefinitePluralNoun
from sentences.words.punctuation import Punctuation
from sentences.words.pronoun import Pronoun


Paragraph = List[List[Union[Word, Pronoun, Punctuation]]]


class Grammarizer(object):
    def __init__(self, paragraph: Paragraph, present_tense: bool = True, p_plural: float = 0.3, p_negative: float = 0.2):
        self._raw = paragraph
        self._raw_subjects = get_subjects(paragraph)
        self._present_tense = present_tense
        self._plural = normalize_probability(p_plural)
        self._negative = normalize_probability(p_negative)

    def _create_subject_pool(self):
        pool = {}
        for subj in self._raw_subjects:
            use_plural = False
            countable = is_countable(subj)
            if random.random() < self._plural and countable:
                use_plural = True
            pool[subj] = {'plural': use_plural, 'definite': False, 'countable': countable}
        return pool

    def generate_paragraph(self):
        print(self._raw_subjects)
        subj_infos = self._create_subject_pool()
        answer = []
        for index, sentence in enumerate(self._raw):
            new_sentence = []
            raw_subj = self._raw_subjects[index]
            subj_info = subj_infos[raw_subj]
            for element in sentence:
                new_wd = element

                if element == raw_subj and isinstance(element, Noun):
                    if subj_info['plural']:
                        new_wd = new_wd.plural()

                    if subj_info['definite']:
                        new_wd = new_wd.definite()
                    else:
                        subj_info['definite'] = True
                        if subj_info['countable'] and not isinstance(new_wd, PluralNoun):
                            new_wd = new_wd.indefinite()

                if isinstance(new_wd, BasicVerb):
                    if random.random() < self._negative:
                        new_wd = new_wd.negative()

                new_sentence.append(new_wd)
            answer.append(new_sentence)
        for sentence in answer:
            sentence[0] = sentence[0].capitalize()
            if requires_third_person(sentence):
                verb_index = find_subject(sentence) + 1
                sentence[verb_index] = sentence[verb_index].third_person()
        return answer



def normalize_probability(probability: float):
    return min(1.0, max(probability, 0))



def get_subjects(paragraph: Paragraph) -> List[Union[Word, Pronoun]]:
    answer = []
    for sentence in paragraph:
        index = find_subject(sentence)
        subj = None
        if index != -1:
            subj = sentence[index]
        answer.append(subj)
    return answer

