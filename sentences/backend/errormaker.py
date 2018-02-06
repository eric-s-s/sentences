import random

from sentences.backend.grammarizer import normalize_probability
from sentences.backend.investigation_tools import requires_third_person, get_present_be_verb, find_subject

from sentences.words.wordtools.wordtag import WordTag
from sentences.words.wordtools.common_functions import add_s

from sentences.words.noun import Noun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb
from sentences.words.basicword import BasicWord

from sentences.words.pronoun import AbstractPronoun, Pronoun, CapitalPronoun


def copy_paragraph(lst_of_lst):
    return [lst[:] for lst in lst_of_lst]


class ErrorMaker(object):
    def __init__(self, paragraph, p_error):
        self.p_error = normalize_probability(p_error)
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

    @property
    def method_order(self):
        methods = [
            self.create_noun_errors, self.create_pronoun_errors, self.create_verb_errors, self.create_is_do_errors,
            self.create_preposition_transpose_errors, self.create_period_errors
        ]
        return methods

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

    def create_pronoun_errors(self):
        excluded = [Pronoun.YOU, Pronoun.IT, CapitalPronoun.YOU, CapitalPronoun.IT]
        for s_index, sentence in enumerate(self._error_paragraph):
            for index, word in enumerate(sentence):
                if isinstance(word, AbstractPronoun) and word not in excluded:
                    if random.random() < self.p_error:
                        self._error_count += 1
                        new_pronoun = word.object()
                        if new_pronoun == word:
                            new_pronoun = word.subject()
                        sentence[index] = new_pronoun
                        self._answer[s_index][index] = self._answer[s_index][index].bold()

    def create_verb_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            for index, word in enumerate(sentence):
                if isinstance(word, Verb):
                    if random.random() < self.p_error:
                        self._error_count += 1

                        is_third_person_noun = requires_third_person(sentence)
                        new_verb = make_verb_error(word, is_third_person_noun)
                        sentence[index] = new_verb
                        self._answer[s_index][index] = self._answer[s_index][index].bold()

    def create_is_do_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            for index, word in enumerate(sentence):
                if isinstance(word, Verb):
                    if random.random() < self.p_error:
                        if not self.already_has_error(s_index, index):
                            self._error_count += 1

                        be_verb = get_present_be_verb(sentence)
                        is_do = make_is_do_error(word, be_verb)
                        sentence[index] = is_do
                        self._answer[s_index][index] = self._answer[s_index][index].bold()

    def already_has_error(self, sentence_index, word_index):
        return self._answer[sentence_index][word_index].value.startswith('<bold>')

    def create_preposition_transpose_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            for index, word in enumerate(sentence):
                if word.has_tags(WordTag.PREPOSITION):
                    if random.random() < self.p_error:
                        self._error_count += 1

                        obj_index = index + 1
                        obj = sentence[obj_index]
                        del sentence[index]
                        del sentence[index]

                        insert_index = find_subject_special_case(sentence) + 1
                        sentence.insert(insert_index, obj)
                        sentence.insert(insert_index, word)

                        self._answer[s_index][index] = self._answer[s_index][index].bold()
                        self._answer[s_index][obj_index] = self._answer[s_index][obj_index].bold()

    def create_period_errors(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            if random.random() < self.p_error:
                self._error_count += 1

                sentence[-1] = Punctuation.COMMA
                self._answer[s_index][-1] = self._answer[s_index][-1].bold()
        self._decapitalize_at_commas()

    def _decapitalize_at_commas(self):
        last_index = len(self._error_paragraph) - 1
        for s_index, sentence in enumerate(self._error_paragraph):
            if sentence[-1] == Punctuation.COMMA and s_index < last_index:
                target_sentence_index = s_index + 1
                target_sentence = self._error_paragraph[target_sentence_index]
                to_de_capitalize = target_sentence[0]
                new_word = to_de_capitalize.de_capitalize()
                target_sentence[0] = new_word
                if to_de_capitalize != new_word:
                    self._answer[target_sentence_index][0] = self._answer[target_sentence_index][0].bold()

    def create_all_errors(self):
        for method in self.method_order:
            method()


def make_noun_error(noun):
    basic = noun.to_basic_noun()
    if noun.has_tags(WordTag.PROPER):
        choices = [basic.indefinite(), basic.definite()]
    elif noun.has_tags(WordTag.UNCOUNTABLE):
        choices = [basic.indefinite(), basic.plural()]
    elif noun.has_tags(WordTag.INDEFINITE):
        choices = [basic] * 3 + [basic.plural().indefinite(), basic.plural()]
    elif noun.has_tags(WordTag.PLURAL):
        choices = [basic] * 3 + [basic.indefinite(), basic.definite(), basic.plural().indefinite()]
    else:
        choices = [basic] * 3 + [basic.indefinite(), basic.plural(), basic.plural().indefinite()]

    return random.choice(choices)


def make_verb_error(verb, is_third_person_noun):
    basic = verb.to_basic_verb()
    if verb.has_tags(WordTag.NEGATIVE):
        basic = basic.negative()

    if verb.has_tags(WordTag.PAST):
        choices = [basic, basic.third_person()]
    elif is_third_person_noun:
        choices = [basic] * 3 + [basic.past_tense(), _add_s_to_verb(basic.past_tense())]

    else:
        choices = [basic.third_person()] * 3 + [basic.past_tense()]

    return random.choice(choices)


def _add_s_to_verb(verb: Verb):
    return Verb(add_s(verb.value), verb.irregular_past, verb.infinitive, verb.tags)


def make_is_do_error(verb, be_verb):
    be_value = be_verb.value
    if verb.has_tags(WordTag.PAST):
        if be_value == 'are':
            be_value = 'were'
        else:
            be_value = 'was'
    if verb.has_tags(WordTag.NEGATIVE):
        return BasicWord('{} not {}'.format(be_value, verb.infinitive))
    return BasicWord('{} {}'.format(be_value, verb.infinitive))


def find_subject_special_case(sentence):
    answer = find_subject(sentence)
    if answer == -1:
        for index, word in enumerate(sentence):
            value = word.value
            if any(value.startswith(be_verb) for be_verb in ('is', 'am', 'are', 'was', 'were')):
                return index - 1
    return answer
