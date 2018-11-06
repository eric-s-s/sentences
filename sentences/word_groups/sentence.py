from typing import List, Optional

from sentences.words.wordtools.abstractword import AbstractWord
from sentences.words.verb import Verb
from sentences.words.be_verb import BeVerb
from sentences.words.punctuation import Punctuation

WordList = List[AbstractWord]


class Sentence(object):
    def __init__(self, word_list: WordList=None):
        if word_list is None:
            word_list = []
        self._word_list = word_list.copy()

    def word_list(self):
        return self._word_list[:]

    def get_verb(self):
        for index, word in enumerate(self.word_list()):
            if isinstance(word, (Verb, BeVerb)):
                return index
        return -1

    def get_subject(self):
        return max(self.get_verb() - 1, -1)

    def __eq__(self, other):
        if not isinstance(other, Sentence):
            return False
        return self.word_list() == other.word_list()

    def __iter__(self):
        return iter(self.word_list())

    def __len__(self):
        return len(self._word_list)

    def get(self, index):
        return self._word_list[index]

    def set(self, index, value):
        new_list = self.word_list()
        new_list[index] = value
        return Sentence(new_list)

    def delete(self, index):
        new_list = self.word_list()
        del new_list[index]
        return Sentence(new_list)

    def insert(self, index, new_word):
        new_list = self.word_list()
        new_list.insert(index, new_word)
        return Sentence(new_list)

    def insert_list(self, index, word_list):
        old_list = self.word_list()
        new_list = old_list[:index] + word_list[:] + old_list[index:]
        return Sentence(new_list)

    def __str__(self):
        answer = ''
        for word in self.word_list():
            if not answer or isinstance(word, Punctuation):
                answer += word.value
            else:
                answer += ' {}'.format(word.value)
        return answer






