import random

from sentences.backend.grammarizer import normalize_probability
from sentences.backend.investigation_tools import requires_third_person
from sentences.words.noun import Noun, IndefiniteNoun, PluralNoun, UncountableNoun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb
from sentences.words.word import Word


def copy_paragraph(lst_of_lst):
    return [lst[:] for lst in lst_of_lst]


class ErrorMaker(object):
    def __init__(self, paragraph, p_error, present_tense=True):
        self.p_error = normalize_probability(p_error)
        self.present_tense = present_tense
        self._paragraph = copy_paragraph(paragraph)
        self._error_paragraph = copy_paragraph(paragraph)
        self._answer = copy_paragraph(paragraph)
        self._error_count = 0

    @property
    def paragraph(self):
        return copy_paragraph(self._paragraph)

    @property
    def error_paragraph(self):
        return copy_paragraph(self._error_paragraph)

    @property
    def answer_paragraph(self):
        answer = copy_paragraph(self._answer)
        return answer

    @property
    def error_count(self):
        return self._error_count

    def reset(self):
        self._error_paragraph = self.paragraph
        self._error_count = 0

    def create_noun_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            for index, word in enumerate(sentence):
                if isinstance(word, Noun):
                    if random.random() < self.p_error:
                        self._error_count += 1

                        new_noun = make_noun_error(word)
                        if index == 0:
                            new_noun = new_noun.capitalize()
                        sentence[index] = new_noun
                        self._answer[s_index][index] = self._answer[s_index][index].bold()

    def create_verb_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            for index, word in enumerate(sentence):
                if isinstance(word, Verb):
                    if random.random() < self.p_error:
                        self._error_count += 1

                        third_person = requires_third_person(sentence)
                        new_verb = make_verb_error(word, self.present_tense, third_person)
                        sentence[index] = new_verb
                        self._answer[s_index][index] = self._answer[s_index][index].bold()

    def create_period_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            if random.random() < self.p_error:
                self._error_count += 1

                sentence[-1] = Punctuation.COMMA
                self._answer[s_index][-1] = self._answer[s_index][-1].bold()
        self._decapitalize_at_commas()

    def _decapitalize_at_commas(self):
        last_index = len(self._error_paragraph) - 1
        for index, sentence in enumerate(self._error_paragraph):
            if sentence[-1] == Punctuation.COMMA and index < last_index:
                to_alter_index = index + 1
                to_alter = self._error_paragraph[to_alter_index]
                to_decapitalize = to_alter[0]
                old_value = to_decapitalize.value
                new_word = Word(old_value[0].lower() + old_value[1:])
                to_alter[0] = new_word
                self._answer[to_alter_index][0] = self._answer[to_alter_index][0].bold()

    def create_all_errors(self):
        self.create_noun_errors()
        self.create_verb_errors()
        self.create_period_errors()


def make_noun_error(noun):
    basic = noun.to_base_noun()
    if isinstance(noun, UncountableNoun):
        choices = [basic.indefinite(), basic.plural()]
    elif isinstance(noun, IndefiniteNoun):
        choices = [basic] * 3 + [basic.plural().indefinite(), basic.plural()]
    elif isinstance(noun, PluralNoun):
        choices = [basic] * 3 + [basic.indefinite(), basic.definite(), basic.plural().indefinite()]
    else:
        choices = [basic] * 3 + [basic.indefinite(), basic.plural(), basic.plural().indefinite()]

    return random.choice(choices)


def make_verb_error(verb, present_tense, third_person):
    basic = verb.to_basic_verb()
    if is_negative_verb(verb):
        basic = basic.negative()

    if present_tense and third_person:
        choices = [basic] * 3 + [basic.past_tense(), basic.past_tense().add_s()]
    elif present_tense and not third_person:
        choices = [basic.third_person()] * 3 + [basic.past_tense()]
    else:
        choices = [basic, basic.third_person()]

    return random.choice(choices)


def is_negative_verb(verb):
    negatives = ["don't ", "doesn't ", "didn't ", "do not ", "does not ", "did not "]
    value = verb.value
    return any(value.startswith(negative) for negative in negatives)