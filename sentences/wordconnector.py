from itertools import chain

from sentences.words.punctuation import Punctuation


def convert_paragraph(paragraph):
    return connect_words(flatten_paragraph(paragraph))


def flatten_paragraph(paragraph):
    return list(chain.from_iterable(paragraph))


def connect_words(word_list):
    answer = ''
    for word in word_list:
        if isinstance(word, Punctuation):
            answer = answer.rstrip()
        answer += word.value + ' '
    return answer.rstrip()
