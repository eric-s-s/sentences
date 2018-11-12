import random

from sentences.tags.status_tag import StatusTag
from sentences.tags.wordtag import WordTag
from sentences.word_groups.paragraph import Paragraph
from sentences.words.be_verb import BeVerb
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun, CapitalPronoun, AbstractPronoun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb
from sentences.words.wordtools.common_functions import add_s


class NewErrorMaker(object):
    def __init__(self, paragraph: Paragraph):
        self._paragraph = paragraph
        self._error_paragraph = None  # type: Paragraph

    def get_paragraph(self):
        return self._paragraph

    def noun_errors(self, p_error):
        self._error_paragraph = self._paragraph
        self._set_error_tag(StatusTag.NOUN_ERRORS)

        for s_index, w_index, word in self._error_paragraph.indexed_all_words():
            if isinstance(word, Noun) and random.random() < p_error:
                new_noun = make_noun_error(word)
                self._error_paragraph = self._error_paragraph.set(s_index, w_index, new_noun)
        self._recapitalize_first_word()
        return NewErrorMaker(self._error_paragraph)

    def pronoun_errors(self, p_error):
        self._error_paragraph = self._paragraph
        self._set_error_tag(StatusTag.PRONOUN_ERRORS)

        excluded = [Pronoun.YOU, Pronoun.IT, CapitalPronoun.YOU, CapitalPronoun.IT]
        for s_index, w_index, word in self._error_paragraph.indexed_all_words():
            if isinstance(word, AbstractPronoun) and word not in excluded:
                if random.random() < p_error:
                    new_word = word.subject()
                    if new_word == word:
                        new_word = word.object()
                    self._error_paragraph = self._error_paragraph.set(s_index, w_index, new_word)

        return NewErrorMaker(self._error_paragraph)

    def verb_errors(self, p_error):
        self._error_paragraph = self._paragraph
        self._set_error_tag(StatusTag.VERB_ERRORS)

        for s_index, w_index, word in self._error_paragraph.indexed_all_words():
            if isinstance(word, Verb) and random.random() < p_error:
                new_verb = make_verb_error(word)
                self._error_paragraph = self._error_paragraph.set(s_index, w_index, new_verb)

        self._recapitalize_first_word()
        return NewErrorMaker(self._error_paragraph)

    def is_do_errors(self, p_error):
        self._error_paragraph = self._paragraph
        self._set_error_tag(StatusTag.IS_DO_ERRORS)
        for s_index, sentence in enumerate(self._error_paragraph):
            be_verb = get_be_verb(sentence)
            v_index = sentence.get_verb()
            if v_index != -1 and random.random() < p_error:
                verb = sentence.get(v_index)
                if isinstance(verb, BeVerb):
                    continue

                new_sentence = sentence.set(v_index, verb.to_basic_verb())
                new_sentence = new_sentence.insert(v_index, be_verb)
                self._error_paragraph = self._error_paragraph.set_sentence(s_index, new_sentence)
        return NewErrorMaker(self._error_paragraph)

    def preposition_errors(self, p_error):
        self._error_paragraph = self._paragraph
        self._set_error_tag(StatusTag.PREPOSITION_ERRORS)
        for s_index, w_index, word in self._error_paragraph.indexed_all_words():
            if word.has_tags(WordTag.PREPOSITION) and random.random() < p_error:
                sentence = self._error_paragraph.get_sentence(s_index)
                obj = sentence.get(w_index + 1)
                sentence = sentence.delete(w_index).delete(w_index)
                v_index = sentence.get_verb()
                sentence = sentence.insert(v_index, obj).insert(v_index, word)
                self._error_paragraph = self._error_paragraph.set_sentence(s_index, sentence)

        return NewErrorMaker(self._error_paragraph)

    def punctuation_errors(self, p_error):
        self._error_paragraph = self._paragraph
        self._set_error_tag(StatusTag.PUNCTUATION_ERRORS)
        for s_index, sentence in enumerate(self._error_paragraph):
            if random.random() < p_error:
                new_sentence = sentence.set(-1, Punctuation.COMMA)
                self._error_paragraph = self._error_paragraph.set_sentence(s_index, new_sentence)
        self._decapitalize_at_commas()
        return NewErrorMaker(self._error_paragraph)

    def _decapitalize_at_commas(self):
        for index, sentence in enumerate(self._error_paragraph.sentence_list()[:-1]):
            if sentence.get(-1) == Punctuation.COMMA:
                next_index = index + 1
                next_sentence = self._error_paragraph.get_sentence(next_index)
                first_word = next_sentence.get(0)
                next_sentence = next_sentence.set(0, first_word.de_capitalize())
                self._error_paragraph = self._error_paragraph.set_sentence(next_index, next_sentence)

    def _set_error_tag(self, new_tag):
        new_tags = self._error_paragraph.tags.remove(StatusTag.GRAMMATICAL).add(new_tag)
        self._error_paragraph = self._error_paragraph.set_tags(new_tags)

    def _recapitalize_first_word(self):
        for s_index, sentence in enumerate(self._error_paragraph):
            try:
                test_word = self._paragraph.get_sentence(s_index).get(0)
                new_word = sentence.get(0)
            except IndexError:
                continue

            if test_word.capitalize() == test_word:
                new_word = new_word.capitalize()

            new_sentence = sentence.set(0, new_word)
            self._error_paragraph = self._error_paragraph.set_sentence(s_index, new_sentence)


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


def make_verb_error(verb):
    basic = verb.to_basic_verb()
    if verb.has_tags(WordTag.NEGATIVE):
        basic = basic.negative()

    if verb.has_tags(WordTag.PAST):
        choices = [basic, basic.third_person()]
    elif verb.has_tags(WordTag.THIRD_PERSON):
        choices = [basic] * 3 + [basic.past_tense(), _add_s_to_verb(basic.past_tense())]

    else:
        choices = [basic.third_person()] * 3 + [basic.past_tense()]

    return random.choice(choices)


def _add_s_to_verb(verb: Verb):
    return Verb(add_s(verb.value), verb.irregular_past, verb.infinitive, verb.tags)


def get_be_verb(sentence):
    subj_index = sentence.get_subject()
    verb_index = sentence.get_verb()
    if subj_index == -1 or verb_index == -1:
        return BeVerb.BE
    subj = sentence.get(subj_index)
    verb = sentence.get(verb_index)

    if isinstance(verb, BeVerb):
        return verb

    if subj in (Pronoun.I, Pronoun.ME, CapitalPronoun.I, CapitalPronoun.ME):
        be_verb = BeVerb.AM
    elif not subj.has_tags(WordTag.PLURAL):
        be_verb = BeVerb.IS
    else:
        be_verb = BeVerb.ARE

    if verb.has_tags(WordTag.NEGATIVE):
        be_verb = be_verb.negative()
    if verb.has_tags(WordTag.PAST):
        be_verb = be_verb.past_tense()
    return be_verb
