import random

from sentences.backend.random_assignments.random_sentences import RandomSentences
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun


class RandomParagraph(object):
    def __init__(self, probability_pronoun, verb_list, noun_list):
        self._p_pronoun = probability_pronoun
        self._word_maker = RandomSentences(verb_list, noun_list)

    def get_subject_pool(self, size):
        pool = []
        safety_count = 0
        safety_limit = 100 + size
        while len(pool) < size:
            new_subj = self._word_maker.subject(self._p_pronoun)
            if new_subj not in pool:
                pool.append(new_subj)
            else:
                safety_count += 1
                if safety_count > safety_limit:
                    raise ValueError('pool size is too large for available nouns loaded from file')
        return pool

    def create_pool_paragraph(self, pool_size, num_sentences):
        subjects = self.get_subject_pool(pool_size)

        paragraph = []
        for _ in range(num_sentences):
            subj = random.choice(subjects)
            paragraph.append(self._word_maker.sentence(subj, self._p_pronoun))
        return paragraph

    def create_chain_paragraph(self, num_sentences):
        paragraph = []

        new_subj = self._word_maker.subject(self._p_pronoun)
        for _ in range(num_sentences):
            sentence = self._word_maker.sentence(new_subj, self._p_pronoun)
            paragraph.append(sentence)
            subj_candidate = sentence.get(-2)
            if isinstance(subj_candidate, Pronoun):
                new_subj = subj_candidate.subject()
            elif isinstance(subj_candidate, Noun):
                new_subj = subj_candidate
            else:
                new_subj = self._word_maker.subject(self._p_pronoun)

        return paragraph
