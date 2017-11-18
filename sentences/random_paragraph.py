import random
from sentences.random_sentences import RandomSentences

from sentences.investigation_tools import is_word_in_sentence
from sentences.words.pronoun import Pronoun
from sentences.words.noun import Noun


class RandomParagraph(object):
    def __init__(self, p_pronoun=0.2, verb_file='', countable_file='', uncountable_file=''):
        self._p_pronoun = p_pronoun
        self._word_maker = RandomSentences(verb_file, countable_file, uncountable_file)

    def get_subject_pool(self, size):
        pool = []
        safety_count = 0
        safety_limit = 100 + size
        while len(pool) < size:
            new_subj = self._word_maker.subject(self._p_pronoun)
            if not is_word_in_sentence(new_subj, pool):
                pool.append(new_subj)
            else:
                safety_count += 1
                if safety_count > safety_limit:
                    raise OverflowError('pool size is too large for available nouns loaded from file')
        return pool

    def create_pool_paragraph(self, pool_size, num_sentences):
        subjects = self.get_subject_pool(pool_size)
        paragraph = []
        safety_count = 0
        too_many_excepts = 100 + num_sentences
        while len(paragraph) < num_sentences:
            predicate = self._word_maker.predicate(self._p_pronoun)
            try:
                subj = get_subj(subjects, predicate)
                predicate.insert(0, subj)
                paragraph.append(predicate)
            except ValueError:
                safety_count += 1
                if safety_count > too_many_excepts:
                    raise OverflowError('Too many failures to find subj different from predicate.')
        return paragraph

    def create_chain_paragraph(self, num_sentences):
        paragraph = []

        subj = self._word_maker.subject(self._p_pronoun)
        predicate = self._word_maker.predicate(self._p_pronoun)

        safety_count = 0
        while len(paragraph) < num_sentences:
            while is_word_in_sentence(subj, predicate) and safety_count < 100:
                predicate = self._word_maker.predicate(self._p_pronoun)
                safety_count += 1
            safety_count = 0
            predicate.insert(0, subj)
            paragraph.append(predicate)

            subj_candidate = predicate[-2]
            if isinstance(subj_candidate, Pronoun):
                subj = subj_candidate.subject()
            elif isinstance(subj_candidate, Noun):
                subj = subj_candidate
            else:
                subj = self._word_maker.subject(self._p_pronoun)

        return paragraph


def get_subj(pool, predicate):
    to_use = pool[:]
    random.shuffle(to_use)
    while to_use:
        candidate = to_use.pop()
        if not is_word_in_sentence(candidate, predicate):
            return candidate
    raise ValueError('All subjects in predicate')
