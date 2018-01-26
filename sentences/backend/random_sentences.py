import random

from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.word import SeparableParticle


# TODO two-part verbs
# TODO improve preposition insertion, it's automatic
# TODO reformat verbs.csv

# TODO verb, irregular past, preposition, obj num, is two-part





class RandomSentences(object):
    def __init__(self, verb_list, noun_list):
        self._pronouns = list(Pronoun.__members__.values())
        self._endings = [Punctuation.PERIOD, Punctuation.PERIOD, Punctuation.EXCLAMATION]

        self._verbs = verb_list[:]
        self._nouns = noun_list[:]
        self._check_empty_lists()

    def _check_empty_lists(self):
        if not self._verbs:
            raise ValueError('There are no verbs in the verb list.')
        if not self._nouns:
            raise ValueError('There are no nouns in any of the nouns lists.')

    def sentence(self, p_pronoun=0.2):
        p_pronoun = min(max(p_pronoun, 0), 1)

        subj = self.subject(p_pronoun)
        predicate = self.predicate(p_pronoun)
        predicate.insert(0, subj)
        return predicate

    def predicate(self, p_pronoun=0.2):
        p_pronoun = min(max(p_pronoun, 0), 1)

        verb_group = random.choice(self._verbs)

        objects = self._get_objects(verb_group['objects'], p_pronoun)

        predicate = assign_objects(verb_group, objects)

        predicate.append(random.choice(self._endings))
        return predicate

    def _get_objects(self, object_count, p_pronoun):
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
        return objects

    def subject(self, p_pronoun):
        if random.random() < p_pronoun:
            return random.choice(self._pronouns).subject()
        else:
            return random.choice(self._nouns)

    def object(self, p_pronoun):
        if random.random() < p_pronoun:
            return random.choice(self._pronouns).object()
        else:
            return random.choice(self._nouns)


def assign_objects2(verb_group, objects):
    preposition = verb_group['preposition']
    separable_particle = verb_group['particle']
    predicate = [verb_group['verb']]

    use_particle = separable_particle is not None
    use_preposition = preposition is not None

    while objects:
        obj = objects.pop(0)
        append_obj = True
        if use_particle and use_preposition and verb_group['objects'] == 1:
            use_preposition = False
            use_particle = False
            predicate.append(separable_particle)
            predicate.append(preposition)
        elif use_particle:
            use_particle = False
            if isinstance(obj, Pronoun):
                predicate.append(obj)
                append_obj = False
            predicate.append(separable_particle)
        elif use_preposition and not objects:
            use_preposition = False
            predicate.append(preposition)

        if append_obj:
            predicate.append(obj)

    if use_particle:
        predicate.append(separable_particle)
    if use_preposition:
        predicate.append(preposition)
    return predicate


def assign_objects(verb_group, objects):
    preposition = [verb_group['preposition']]
    separable_particle = [verb_group['particle']]
    predicate = [verb_group['verb']]

    while objects:
        obj = objects.pop()
        if len(preposition) < 2:
            preposition.append(obj)
        elif isinstance(obj, Pronoun):
            separable_particle.insert(0, obj)
        else:
            separable_particle.append(obj)
    if does_preposition_precede_separable_particle(preposition, separable_particle):
        answer = predicate + preposition + separable_particle
    else:
        answer = predicate + separable_particle + preposition

    return [word for word in answer if word is not None]


def does_preposition_precede_separable_particle(preposition, separable_particle):
    return (
        None in preposition and
        all(isinstance(word, SeparableParticle) for word in separable_particle) and
        any(isinstance(word, Pronoun) for word in preposition)
    )
