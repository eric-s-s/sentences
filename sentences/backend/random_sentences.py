import random

from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation


class RandomSentences(object):
    def __init__(self, verb_list, countable_list, uncountable_list):
        self._pronouns = list(Pronoun.__members__.values())
        self._endings = [Punctuation.PERIOD, Punctuation.PERIOD, Punctuation.EXCLAMATION]

        self._countable = countable_list[:]
        self._verbs = verb_list[:]
        self._uncountable = uncountable_list[:]
        self._check_empty_lists()

    def _check_empty_lists(self):
        if not self._verbs:
            raise ValueError('There are no verbs in the verb list.')
        if not self._countable and not self._uncountable:
            raise ValueError('There are no countable nouns AND no uncountable nouns.')

    def sentence(self, p_pronoun=0.2):
        p_pronoun = min(max(p_pronoun, 0), 1)

        subj = self.subject(p_pronoun)
        predicate = self.predicate(p_pronoun)
        predicate.insert(0, subj)
        return predicate

    def predicate(self, p_pronoun=0.2):
        p_pronoun = min(max(p_pronoun, 0), 1)

        action, object_count, insert_preposition = self._get_verb_list_and_object_count()

        objects = []
        object_position = 0
        loop_count = 0
        max_loops_until_repeats_allowed = 100
        while object_position < object_count:
            if object_position == 0:
                new_obj = self.object(p_pronoun)
            else:
                new_obj = self.object(p_pronoun=0)

            if new_obj not in objects or loop_count > max_loops_until_repeats_allowed:
                objects.append(new_obj)
                object_position += 1

            loop_count += 1
                            
        if insert_preposition:
            action.insert(-1, objects.pop(0))
        action = action + objects

        action.append(random.choice(self._endings))
        return action

    def _get_verb_list_and_object_count(self):
        verb_grp = random.choice(self._verbs)
        action = [(verb_grp['verb'])]
        prep = verb_grp['preposition']
        if prep is not None:
            action.append(prep)
        return action, verb_grp['objects'], verb_grp['insert_preposition']

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
