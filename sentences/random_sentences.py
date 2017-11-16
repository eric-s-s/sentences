import random

from sentences.words.punctuation import Punctuation
from sentences.words.pronoun import Pronoun
from sentences.loader import verbs, uncountable_nouns, countable_nouns


class RandomSentences(object):
    def __init__(self):
        self._pronouns = [pronoun for pronoun in Pronoun]
        self._endings = [Punctuation.PERIOD, Punctuation.PERIOD, Punctuation.EXCLAMATION]
        self._countable = countable_nouns()
        self._verbs = verbs()
        self._uncountable = uncountable_nouns()

    def sentence(self, p_pronoun=0.2):
        p_pronoun = min(max(p_pronoun, 0), 1)

        subj = self.subject(p_pronoun)
        predicate = self.predicate(p_pronoun)
        predicate.insert(0, subj)
        return predicate

    def predicate(self, p_pronoun=0.2):
        p_pronoun = min(max(p_pronoun, 0), 1)

        action, object_count = self._get_verb_list_and_object_count()

        objects = []
        object_position = 0
        while object_position < object_count:
            if object_position == 0:
                new_obj = self.object(p_pronoun)
            else:
                new_obj = self.object(p_pronoun=0)

            if new_obj not in objects:
                objects.append(new_obj)
                object_position += 1

        action = action + objects

        action.append(random.choice(self._endings))
        return action

    def _get_verb_list_and_object_count(self):
        verb_grp = random.choice(self._verbs)
        action = [(verb_grp['verb'])]
        prep = verb_grp['preposition']
        if prep is not None:
            action.append(prep)
        return action, verb_grp['objects']

    def subject(self, p_pronoun):
        if random.random() < p_pronoun:
            return random.choice(self._pronouns).subject()
        else:
            return random.choice(self._countable + self._uncountable)

    def object(self, p_pronoun):
        if random.random() < p_pronoun:
            return random.choice(self._pronouns).object()
        else:
            return random.choice(self._countable + self._uncountable)

