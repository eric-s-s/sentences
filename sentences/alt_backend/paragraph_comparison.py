import re
from itertools import zip_longest

from sentences.word_groups.paragraph import Paragraph
from sentences.words.noun import Noun


class ParagraphComparison(object):
    def __init__(self, answer_paragraph: Paragraph, submission_str):
        self.answer = answer_paragraph
        self.submission = submission_str

    def compare_by_sentences(self):
        submission_sentences = self._get_submission_sentences()
        answer_sentences = (str(sentence) for sentence in self.answer)
        error_count = 0
        hint_paragraph = []
        for answer, submission in zip_longest(answer_sentences, submission_sentences, fillvalue=''):
            if answer != submission and submission:
                submission = f'<bold>{submission}</bold>'
                error_count += 1
            hint_paragraph.append(submission)
        missing_sentences = len(self.answer) - len(submission_sentences)

        return {'error_count': error_count,
                'hint_paragraph': ' '.join(hint_paragraph),
                'missing_sentences': missing_sentences}

    def _get_submission_sentences(self):
        sentence_re = re.compile(r"[^.,!?]+[.,!?]?")
        submission_sentences = sentence_re.findall(self.submission)
        return [sentence.strip() for sentence in submission_sentences]

    def compare_by_words(self):
        return {'error_count': 0, 'hint_paragraph': str(self.answer), 'missing_sentences': 0}


def compare_sentences(sentence, submission_str):
    word_list = get_word_list(submission_str)
    # grouped = get_noun_groupings(get_verb_groupings(word_list))
    return {
        'error_count': 0,
        'hint_sentence': submission_str,
    }


def find_word_group(word, submission_str):
    if isinstance(word, Noun):
        base_word = word.to_basic_noun()
        or_statement = '({}|{})'.format(base_word.value, base_word.capitalize().value)
        answer = re.compile(r'.*{}\w*'.format(or_statement)).match(submission_str)
        if answer:
            return answer.span()


def get_noun_groupings(sentence, submission_str):
    breaks = r"[ ,.?!]"
    answer = {}
    for word in sentence:
        if isinstance(word, Noun):
            to_search = Noun.base_noun


def get_word_list(submission_str: str):
    added_spaces = submission_str
    for puncutaion in ",.?!":
        added_spaces = added_spaces.replace(puncutaion, f" {puncutaion} ")
    return [word for word in added_spaces.split(' ') if word]




# def get_noun_groupings(word_list):
#     articles = ['a', 'A', 'an', 'An', 'the', 'The']
#     answer = []
#     index = 0
#     while index < len(word_list):
#         word = word_list[index]
#         if word in articles:
#             word = f"{word} {word_list[index + 1]}"
#             index += 1
#         answer.append(word)
#         index += 1
#     return answer


def get_verb_groupings(word_list):
    return word_list[:]
