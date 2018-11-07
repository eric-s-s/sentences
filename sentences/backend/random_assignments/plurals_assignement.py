import random

from sentences.tags.status_tag import StatusTag
from sentences.tags.wordtag import WordTag
from sentences.word_groups.paragraph import Paragraph
from sentences.words.noun import Noun
from sentences.words.wordtools.abstractword import AbstractWord


class PluralsAssignment(object):
    def __init__(self, raw_paragraph: Paragraph):
        self._raw = raw_paragraph
        if raw_paragraph.tags.has(StatusTag.HAS_PLURALS):
            self._revert_nouns()

    def _revert_nouns(self):
        for s_index, w_index, word in self._raw.indexed_all_words():
            if isinstance(word, Noun):
                self._raw = self._raw.set(s_index, w_index, word.to_basic_noun())  # type: Paragraph
        self._raw = self._raw.set_tags(self._raw.tags.remove(StatusTag.HAS_PLURALS))

    @property
    def raw(self):
        return self._raw

    def assign_plural(self, to_plural) -> Paragraph:
        new_paragraph = self.raw
        for noun in to_plural:
            for s_index, w_index in self.raw.find(noun):
                new_paragraph = new_paragraph.set(s_index, w_index, noun.plural())
        return new_paragraph.set_tags(self.raw.tags.add(StatusTag.HAS_PLURALS))

    def assign_random_plurals(self, p_plural):
        to_plural = [noun for noun in get_countable_nouns(self.raw) if random.random() < p_plural]

        return self.assign_plural(to_plural)


def get_countable_nouns(paragraph):
    out = []  # Sets are untestable with random.seed
    for word in paragraph.all_words():  # type: Noun
        if is_countable_noun(word):
            base_word = word.to_basic_noun()
            if base_word not in out:
                out.append(base_word)

    return out


def is_countable_noun(word: AbstractWord):
    return isinstance(word, Noun) and not (word.has_tags(WordTag.UNCOUNTABLE) or word.has_tags(WordTag.PROPER))
