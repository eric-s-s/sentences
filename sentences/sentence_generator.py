import random

from sentences.words.punctuation import Punctuation
from sentences.words.pronoun import Pronoun
from sentences.loader import verbs, uncountable_nouns, countable_nouns


class SentenceGenerator(object):
    def __init__(self):
        self._pronouns = [pronoun for pronoun in Pronoun]
        self._endings = [Punctuation.PERIOD, Punctuation.PERIOD, Punctuation.EXCLAMATION]
        self._countable = countable_nouns()
        self._verbs = verbs()
        self._uncountable = uncountable_nouns()

    def random_sentence(self, p_pronoun=0.2):
        p_pronoun = min(max(p_pronoun, 0), 1)

        sentence = [self.get_subj(p_pronoun)]
        verb_grp = random.choice(self._verbs)
        sentence.append(verb_grp['verb'])
        prep = verb_grp['preposition']
        if prep is not None:
            sentence.append(prep)
        for _ in range(verb_grp['objects']):
            sentence.append(self.get_obj(p_pronoun))
        sentence.append(random.choice(self._endings))
        return sentence

    def get_subj(self, p_pronoun):
        if random.random() < p_pronoun:
            return random.choice(self._pronouns).subject()
        else:
            return random.choice(self._countable + self._uncountable)

    def get_obj(self, p_pronoun):
        if random.random() < p_pronoun:
            return random.choice(self._pronouns).object()
        else:
            return random.choice(self._countable + self._uncountable)


def use_pronoun(probability):
    return random.random() < probability
