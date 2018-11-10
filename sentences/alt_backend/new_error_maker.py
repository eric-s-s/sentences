from sentences.backend.investigation_tools import requires_third_person, get_present_be_verb
from sentences.tags.status_tag import StatusTag
from sentences.tags.wordtag import WordTag
from sentences.word_groups.sentence import Sentence
from sentences.words.punctuation import Punctuation

from sentences.word_groups.paragraph import Paragraph
from sentences.words.pronoun import Pronoun, CapitalPronoun, AbstractPronoun
from sentences.words.noun import Noun
from sentences.words.verb import Verb
from sentences.words.be_verb import BeVerb
import random

from sentences.words.wordtools.common_functions import add_s


class NewErrorMaker(object):
    def __init__(self, paragraph: Paragraph, p_error):
        self.p_error = p_error
        self._paragraph = paragraph
        self._error_paragraph = paragraph  # type: Paragraph

    @property
    def paragraph(self):
        return self._paragraph

    @property
    def error_paragraph(self):
        return self._error_paragraph

    @property
    def method_order(self):
        methods = [
            self.create_noun_errors, self.create_pronoun_errors, self.create_verb_errors, self.create_is_do_errors,
            self.create_preposition_transpose_errors, self.create_period_errors
        ]
        return methods

    def reset(self):
        self._error_paragraph = self.paragraph

    def create_noun_errors(self):
        self._set_error_tags()
        for s_index, w_index, word in self._error_paragraph.indexed_all_words():
            if isinstance(word, Noun):
                if random.random() < self.p_error:
                    new_noun = make_noun_error(word)
                    if w_index == 0:
                        new_noun = new_noun.capitalize()
                    self._error_paragraph = self._error_paragraph.set(s_index, w_index, new_noun)
        # for s_index, sentence in enumerate(self._error_paragraph):
        #     for index, word in enumerate(sentence):
        #         if isinstance(word, Noun):
        #             if random.random() < self.p_error:
        #
        #                 new_noun = make_noun_error(word)
        #                 if index == 0:
        #                     new_noun = new_noun.capitalize()
        #                 sentence[index] = new_noun

    def create_pronoun_errors(self):
        self._set_error_tags()
        # excluded = [Pronoun.YOU, Pronoun.IT, CapitalPronoun.YOU, CapitalPronoun.IT]
        # for s_index, sentence in enumerate(self._error_paragraph):
        #     for index, word in enumerate(sentence):
        #         if isinstance(word, AbstractPronoun) and word not in excluded:
        #             if random.random() < self.p_error:
        #                 new_pronoun = word.object()
        #                 if new_pronoun == word:
        #                     new_pronoun = word.subject()
        #                 sentence[index] = new_pronoun

    def create_verb_errors(self):
        self._set_error_tags()
        # for s_index, sentence in enumerate(self._error_paragraph):
        #     for index, word in enumerate(sentence):
        #         if isinstance(word, Verb):
        #             if random.random() < self.p_error:
        #                 is_third_person_noun = requires_third_person(sentence)
        #                 new_verb = make_verb_error(word, is_third_person_noun)
        #                 sentence[index] = new_verb

    def create_is_do_errors(self):
        self._set_error_tags()
        # for s_index, sentence in enumerate(self._error_paragraph):
        #     for index, word in enumerate(sentence):
        #         if isinstance(word, Verb):
        #             if random.random() < self.p_error:
        #                 be_verb = get_present_be_verb(sentence)
        #                 is_do = make_is_do_error(word, be_verb)
        #                 sentence[index] = is_do

    def create_preposition_transpose_errors(self):
        self._set_error_tags()
        # for s_index, sentence in enumerate(self._error_paragraph):  # type: Sentence
        #     for index, word in enumerate(sentence):
        #         if word.has_tags(WordTag.PREPOSITION):
        #             if random.random() < self.p_error:
        #                 obj_index = index + 1
        #                 obj = sentence[obj_index]
        #                 del sentence[index]
        #                 del sentence[index]
        #
        #                 insert_index = sentence.get_subject() + 1
        #                 sentence.insert(insert_index, obj)
        #                 sentence.insert(insert_index, word)

    def create_period_errors(self):
        self._set_error_tags()
        # for s_index, sentence in enumerate(self._error_paragraph):
        #     if random.random() < self.p_error:
        #         sentence[-1] = Punctuation.COMMA
        # self._decapitalize_at_commas()

    def _decapitalize_at_commas(self):
        pass
        # last_index = len(self._error_paragraph) - 1
        # for s_index, sentence in enumerate(self._error_paragraph):
        #     if sentence[-1] == Punctuation.COMMA and s_index < last_index:
        #         target_sentence_index = s_index + 1
        #         target_sentence = self._error_paragraph[target_sentence_index]
        #         to_de_capitalize = target_sentence[0]
        #         new_word = to_de_capitalize.de_capitalize()
        #         target_sentence[0] = new_word

    def create_all_errors(self):
        pass
        # for method in self.method_order:
        #     method()

    def _set_error_tags(self):
        new_tags = self._error_paragraph.tags.add(StatusTag.HAS_ERRORS).remove(StatusTag.GRAMMATICAL)
        self._error_paragraph = self._error_paragraph.set_tags(new_tags)  # type: Paragraph


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


def make_is_do_error(verb, be_verb: BeVerb):
    new_be_verb = be_verb
    if verb.has_tags(WordTag.PAST):
        new_be_verb = new_be_verb.past_tense()
    if verb.has_tags(WordTag.NEGATIVE):
        new_be_verb = new_be_verb.negative()
    return [new_be_verb, verb.to_basic_verb()]
