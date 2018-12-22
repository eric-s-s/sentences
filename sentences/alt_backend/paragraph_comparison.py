import re
from collections import namedtuple
from itertools import zip_longest
from typing import List

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
        submission_sentences = self._get_submission_sentences()
        missing_sentences = len(self.answer) - len(submission_sentences)
        if missing_sentences > 0:
            submission_sentences += [''] * missing_sentences

        error_count = 0
        hint_sentences = []
        for sentence, submission_str in zip_longest(self.answer, submission_sentences, fillvalue=Sentence()):
            answer = compare_sentences(sentence, submission_str)
            error_count += answer['error_count']
            hint_sentences.append(answer['hint_sentence'])

        return {'error_count': error_count,
                'hint_paragraph': ' '.join(hint_sentences),
                'missing_sentences': missing_sentences}


WordObj = namedtuple('WordObj', ['index', 'location', 'word'])


def compare_sentences(sentence, submission_str):
    new_sentence = []
    error_count = 0
    extra_locations = get_word_locations(submission_str)

    current_search_str = submission_str

    for index, word in enumerate(sentence):
        if isinstance(word, Punctuation):
            new_word, location = get_punctuation(current_search_str)
        else:
            new_word, location = get_word(current_search_str, word)

        if location is None:
            location = _get_missing_location(new_sentence)
        extra_locations = filter_locations(extra_locations, location)

        until, after = location
        replace_found_word = '_' * (after - until)
        current_search_str = current_search_str[:until] + replace_found_word + current_search_str[after:]

        if new_word.value != word.value:
            new_word = new_word.bold()
            error_count += 1
        word_obj = WordObj(index=index, location=location, word=new_word)
        new_sentence.append(word_obj)

    for location in extra_locations:
        word = BasicWord(submission_str[slice(*location)]).bold()
        word_obj = WordObj(index=None, location=location, word=word)
        new_sentence.append(word_obj)
        error_count += 1

    ordered_like_submission_str = sorted(new_sentence, key=lambda el: el.location)
    final_word_list, extra_errors = _check_for_out_of_order_words(ordered_like_submission_str)
    hint = str(Sentence(final_word_list))
    error_count += extra_errors
    return {
        'error_count': error_count,
        'hint_sentence': hint,
    }


def _get_missing_location(current_sentence):
    if not current_sentence:
        location = (0, 0)
    else:
        last_location = current_sentence[-1].location
        end_index = last_location[1]
        location = (end_index, end_index)
    return location


def get_word_locations(submission_str):
    return [match.span() for match in re.compile(r"([a-zA-Z']+|[.,?!])").finditer(submission_str)]


def filter_locations(all_locations, to_remove):
    low, high = to_remove
    return [location for location in all_locations if location[0] >= high or location[1] <= low]


def _check_for_out_of_order_words(obj_list: List[WordObj]):
    word_list = []
    expected_index = 0
    extra_errors = 0
    skipped_indices = 0
    for word_obj in obj_list:

        if word_obj.index is None:
            word_list.append(word_obj.word)
            continue

        if word_obj.index != expected_index:
            new_word = word_obj.word.bold()
            skipped_indices += 1
            if new_word != word_obj.word:
                extra_errors += 1
        else:
            new_word = word_obj.word
            expected_index += 1 + skipped_indices
            skipped_indices = 0
        word_list.append(new_word)
    return word_list, extra_errors


def get_word(submission_str, word):
    location = find_word_group(word, submission_str)
    if location is None:
        return BasicWord('MISSING'), None
    substr = submission_str[slice(*location)]
    new_word = BasicWord(substr)
    return new_word, location


def get_punctuation(submission_str):
    punctuations = {
        '.': Punctuation.PERIOD,
        ',': Punctuation.COMMA,
        '!': Punctuation.EXCLAMATION,
        '?': Punctuation.QUESTION
    }
    last_index = len(submission_str.strip(' ')) - 1
    last_character = submission_str.strip(' ')[last_index:]
    try:
        return punctuations[last_character], (last_index, last_index + 1)
    except KeyError:
        return BasicWord("MISSING"), None


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
