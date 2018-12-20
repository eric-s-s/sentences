import re
from itertools import zip_longest

from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.noun import Noun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb
from sentences.words.wordtools.abstractword import AbstractWord


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
    new_sentence = []
    error_count = 0
    for word in sentence:

        if isinstance(word, Punctuation):
            new_word = get_punctuation(submission_str)
        else:
            location = find_word_group(word, submission_str)
            substr = submission_str[slice(*location)]
            new_word = BasicWord(substr)

        if new_word is None:
            new_word = BasicWord('MISSING')
        if new_word.value != word.value:
            new_word = new_word.bold()
            error_count += 1
        new_sentence.append(new_word)
    hint = str(Sentence(new_sentence))
    return {
        'error_count': error_count,
        'hint_sentence': hint,
    }


def get_punctuation(submission_str):
    punctuations = {
        '.': Punctuation.PERIOD,
        ',': Punctuation.COMMA,
        '!': Punctuation.EXCLAMATION,
        '?': Punctuation.QUESTION
    }
    last_character = submission_str.strip(' ')[-1]
    try:
        return punctuations[last_character]
    except KeyError:
        return None


def find_word_group(word, submission_str):
    if isinstance(word, Noun):
        return find_noun_group(word, submission_str)
    elif isinstance(word, Verb):
        return find_verb_group(word, submission_str)
    else:
        return find_word(word, submission_str)


def find_noun_group(word: Noun, submission_str):
    prefixes = '(a|A|an|An|the|The)'

    base_word = word.to_basic_noun()

    base_value = base_word.value
    plural_value = base_word.plural().value

    base_regex = _get_dual_case(base_value)
    plural_regex = _get_dual_case(plural_value)

    word_regex = f'({base_regex}|{plural_regex})'

    return _find_from_regex(prefixes, word_regex, submission_str)


def find_verb_group(word: Verb, submission_str):
    prefixes = ["don't", "doesn't", "didn't"]
    all_prefixes = prefixes + [word.capitalize() for word in prefixes]
    prefix_regex = '({})'.format('|'.join(all_prefixes))

    base_word = word.to_basic_verb()

    base_value = base_word.value
    third_person_value = base_word.third_person().value
    past_value = base_word.past_tense().value

    base_regex = _get_dual_case(base_value)
    plural_regex = _get_dual_case(third_person_value)
    past_regex = _get_dual_case(past_value)

    word_regex = f'({base_regex}|{plural_regex}|{past_regex})'

    return _find_from_regex(prefix_regex, word_regex, submission_str)


def find_word(word: AbstractWord, submission_str):
    answer = re.search(r'\b{}\b'.format(word.value), submission_str)
    return answer.span() if answer is not None else answer


def _find_from_regex(prefixes, word_regex, submission_str):
    answer = re.compile(r'({} )?{}\w*'.format(prefixes, word_regex)).search(submission_str)
    return answer.span() if answer is not None else answer


def _get_dual_case(base_str):
    return '[{}{}]{}'.format(base_str[0].upper(), base_str[0], base_str[1:])
