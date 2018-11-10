from itertools import chain
from typing import List

from sentences.tags.tags import Tags
from sentences.word_groups.sentence import Sentence
from sentences.words.wordtools.abstractword import AbstractWord


class Paragraph(object):
    def __init__(self, sentence_list: List[Sentence], tags: Tags = None):
        if tags is None:
            tags = Tags()
        self._tags = tags.copy()
        self._sentences = sentence_list[:]

    @classmethod
    def from_word_lists(cls, word_lists: List[List[AbstractWord]], tags=None):
        return Paragraph([Sentence(lst) for lst in word_lists], tags)

    @property
    def tags(self):
        return self._tags.copy()

    def sentence_list(self):
        return self._sentences[:]

    def __eq__(self, other):
        if not isinstance(other, Paragraph):
            return False
        return (self.tags, self.sentence_list()) == (other.tags, other.sentence_list())

    def __len__(self):
        return len(self._sentences)

    def __iter__(self):
        return iter(self._sentences)

    def __str__(self):
        return ' '.join((str(sentence) for sentence in self._sentences))

    def __repr__(self):
        # TODO for tests!
        return 'Paragraph({!r}, {!r})'.format(self.sentence_list(), self.tags)

    def all_words(self):
        return chain.from_iterable(self._sentences)

    def indexed_all_words(self):
        return ((s_index, w_index, word)
                for s_index, sentence in enumerate(self._sentences)
                for w_index, word in enumerate(sentence))

    def set_tags(self, tags: Tags):
        return Paragraph(self.sentence_list(), tags)

    def set_sentence(self, index, new_sentence):
        sentences = self.sentence_list()
        sentences[index] = new_sentence
        return Paragraph(sentences, self.tags)

    def set(self, sentence_index, word_index, value: AbstractWord):
        sentences = self.sentence_list()
        sentences[sentence_index] = sentences[sentence_index].set(word_index, value)
        return Paragraph(sentences, self.tags)

    def find(self, word: AbstractWord):
        answer = []
        for s_index, w_index, to_test in self.indexed_all_words():
            if word == to_test:
                answer.append((s_index, w_index))
        return answer
