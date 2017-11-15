import random

from sentences.words.verb import Verb
from sentences.words.noun import Noun, DefiniteNoun, IndefiniteNoun, PluralNoun
from sentences.words.punctuation import Punctuation
from sentences.grammarizer import normalize_probability
from sentences.investigation_tools import is_countable, is_word_in_sentence, is_third_person, requires_third_person


def super_copy(lst_of_lst):
    return [lst[:] for lst in lst_of_lst]


class ErrorMaker(object):
    def __init__(self, paragraph, p_error, present_tense=True):
        self.p_error = normalize_probability(p_error)
        self.present_tense = present_tense
        self._paragraph = super_copy(paragraph)
        self._error_paragraph = super_copy(paragraph)
        self._answer = super_copy(paragraph)

    @property
    def paragraph(self):
        return super_copy(self._paragraph)

    @property
    def error_paragraph(self):
        return super_copy(self._error_paragraph)

    @property
    def answer_paragraph(self):
        return super_copy(self._answer)

    def reset(self):
        self._error_paragraph = self.paragraph

    def create_noun_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            for index, word in enumerate(sentence):
                if isinstance(word, Noun):
                    if random.random() < self.p_error:
                        new_noun = fuck_with_noun(word)
                        if index == 0:
                            new_noun = new_noun.capitalize()
                        sentence[index] = new_noun
                        self._answer[s_index][index] = self._answer[s_index][index].bold()

    def create_verb_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            for index, word in enumerate(sentence):
                if isinstance(word, Verb):
                    if random.random() < self.p_error:
                        third_person = requires_third_person(sentence)
                        new_verb = fuck_with_verb(word, self.present_tense, third_person)
                        sentence[index] = new_verb
                        self._answer[s_index][index] = self._answer[s_index][index].bold()

    def create_period_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            if random.random() < self.p_error:
                sentence[-1] = Punctuation.COMMA
                self._answer[s_index][-1] = self._answer[s_index][-1].bold()

    def create_all_errors(self):
        self.create_noun_errors()
        self.create_verb_errors()
        self.create_period_errors()


def fuck_with_noun(noun):
    basic = noun.to_base_noun()
    uncountable = not is_countable(basic)
    if uncountable:
        choices = [basic.indefinite(), basic.plural()]
    elif isinstance(noun, IndefiniteNoun):
        choices = [basic] * 3 + [basic.plural().indefinite(), basic.plural()]
    elif isinstance(noun, PluralNoun):
        choices = [basic] * 3 + [basic.indefinite(), basic.definite(), basic.plural().indefinite()]
    else:
        choices = [basic] * 3 + [basic.indefinite(), basic.plural(), basic.plural().indefinite()]

    return random.choice(choices)


def fuck_with_verb(verb, present_tense, third_person):
    basic = verb.to_basic_verb()
    if is_negative_verb(verb):
        basic = basic.negative()

    if present_tense and third_person:
        choices = [basic] * 3 + [basic.past_tense()]
    elif present_tense and not third_person:
        choices = [basic.third_person()] * 3 + [basic.past_tense()]
    else:
        choices = [basic, basic.third_person()]

    return random.choice(choices)


def is_negative_verb(verb):
    negatives = ["don't ", "doesn't ", "didn't ", "do not ", "does not ", "did not "]
    value = verb.value
    return any(value.startswith(negative) for negative in negatives)
