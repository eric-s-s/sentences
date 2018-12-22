import unittest

from sentences.alt_backend.paragraph_comparison import (
    ParagraphComparison, find_noun_group, find_verb_group, find_word,
    find_word_group, compare_sentences,
    get_word_locations, filter_locations, get_word, get_punctuation)
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb


class TestParagraphComparison(unittest.TestCase):
    def test_init(self):
        answer_paragraph = Paragraph([Sentence([BasicWord('a')])])
        submission_str = 'b'

        comparitor = ParagraphComparison(answer_paragraph, submission_str)
        self.assertEqual(comparitor.answer, answer_paragraph)
        self.assertEqual(comparitor.submission, 'b')

    def test_compare_by_sentence_paragraph_str_eq_submission_str(self):
        answer_paragraph = Paragraph([Sentence([BasicWord('a')])])
        submission_str = str(answer_paragraph)
        comparitor = ParagraphComparison(answer_paragraph, submission_str)
        comparison = comparitor.compare_by_sentences()
        expected = {
            'error_count': 0,
            'hint_paragraph': submission_str,
            'missing_sentences': 0
        }
        self.assertEqual(comparison, expected)

    def test_compare_by_sentence_one_sentence_different_by_internals(self):
        answer = Paragraph([Sentence([BasicWord('Hello'), Punctuation.PERIOD]),
                            Sentence([BasicWord('I'), BasicWord('am'), BasicWord('man'), Punctuation.EXCLAMATION])])
        submission = 'Hello. I am man.'
        hint_paragraph = 'Hello. <bold>I am man.</bold>'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 1,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_commas_are_counted_as_sentences(self):
        answer = Paragraph([Sentence([BasicWord(wd), Punctuation.PERIOD]) for wd in 'ABC'])
        submission = 'A, B. C,'
        hint_paragraph = '<bold>A,</bold> B. <bold>C,</bold>'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 2,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_can_identify_period_comma_exclamation_question(self):
        answer = Paragraph([Sentence([BasicWord('a'), Punctuation.PERIOD]),
                            Sentence([BasicWord('b'), Punctuation.EXCLAMATION]),
                            Sentence([BasicWord('c'), Punctuation.QUESTION]),
                            Sentence([BasicWord('d'), Punctuation.COMMA])])
        submission = 'a, b, c, d,'
        hint_paragraph = '<bold>a,</bold> <bold>b,</bold> <bold>c,</bold> d,'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 3,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_will_find_the_final_sentence_with_missing_punctuation(self):
        answer = Paragraph([Sentence([BasicWord('a'), Punctuation.PERIOD]),
                            Sentence([BasicWord('b'), Punctuation.PERIOD])])
        submission = 'a. b'
        hint_paragraph = 'a. <bold>b</bold>'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 1,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_answer_has_more_sentences(self):
        answer = Paragraph([Sentence([BasicWord('a'), Punctuation.PERIOD]),
                            Sentence([BasicWord('b'), Punctuation.PERIOD])])
        submission = 'a and b.'
        hint_paragraph = '<bold>a and b.</bold> '

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 1,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 1
        }
        self.assertEqual(hints, expected)

    def test_compare_by_sentence_answer_has_less_sentences(self):
        answer = Paragraph([Sentence([BasicWord('a'), Punctuation.PERIOD]),
                            Sentence([BasicWord('b'), Punctuation.PERIOD])])
        submission = 'a. c. b.'
        hint_paragraph = 'a. <bold>c.</bold> <bold>b.</bold>'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_sentences()
        expected = {
            'error_count': 2,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': -1
        }
        self.assertEqual(hints, expected)

    def test_compare_by_words_no_errors(self):
        answer = Paragraph([Sentence([BasicWord('a'), Punctuation.PERIOD]),
                            Sentence([BasicWord('b'), Punctuation.PERIOD])])
        submission = 'a. b.'
        hint_paragraph = 'a. b.'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_words()
        expected = {
            'error_count': 0,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_words_noun_errors(self):
        answer = Paragraph([Sentence([Noun('dog').definite(), Punctuation.PERIOD]),
                            Sentence([Noun('cat').plural(), Punctuation.PERIOD])])
        submission = 'a dog. The cats.'
        hint_paragraph = '<bold>a dog</bold>. <bold>The cats</bold>.'

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_words()
        expected = {
            'error_count': 2,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_words_verb_errors(self):
        answer = Paragraph([Sentence([Verb('go', 'went'), Punctuation.PERIOD]),
                            Sentence([Verb('play'), Punctuation.PERIOD])])
        submission = "went. doesn't plays."
        hint_paragraph = "<bold>went</bold>. <bold>doesn't plays</bold>."

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_words()
        expected = {
            'error_count': 2,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_words_punctuation_errors(self):
        answer = Paragraph([Sentence([Verb('go', 'went'), Punctuation.PERIOD]),
                            Sentence([Verb('play'), Punctuation.PERIOD])])
        submission = "go! play "
        hint_paragraph = "go<bold>!</bold> play <bold>MISSING</bold>"

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_words()
        expected = {
            'error_count': 2,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_words_missing_word_errors(self):
        answer = Paragraph([Sentence([Verb('go', 'went'), Punctuation.PERIOD]),
                            Sentence([Verb('play'), Punctuation.PERIOD])])
        submission = " . ."
        hint_paragraph = "<bold>MISSING</bold>. <bold>MISSING</bold>."

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_words()
        expected = {
            'error_count': 2,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_words_extra_word_errors(self):
        answer = Paragraph([Sentence([Verb('go', 'went'), Punctuation.PERIOD]),
                            Sentence([Verb('play'), Punctuation.PERIOD])])
        submission = "I go. play it."
        hint_paragraph = "<bold>I</bold> go. play <bold>it</bold>."

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_words()
        expected = {
            'error_count': 2,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_words_word_order_errors(self):
        answer = Paragraph([Sentence([Pronoun.I, Verb('go', 'went'), Punctuation.PERIOD]),
                            Sentence([Noun('cat'), Verb('play'), BasicWord('with'), Pronoun.HIM, Punctuation.PERIOD])])
        submission = "go I. cat with him play."
        hint_paragraph = "<bold>go</bold> I. cat <bold>with</bold> <bold>him</bold> play."

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_words()
        expected = {
            'error_count': 3,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 0
        }
        self.assertEqual(hints, expected)

    def test_compare_by_words_missing_sentence(self):
        answer = Paragraph([Sentence([Verb('go', 'went'), Punctuation.PERIOD]),
                            Sentence([Noun('cat'), Verb('play'), Punctuation.PERIOD])])
        submission = "go."
        hint_paragraph = "go. <bold>MISSING</bold> <bold>MISSING</bold> <bold>MISSING</bold>"

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_words()
        expected = {
            'error_count': 3,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': 1
        }
        self.assertEqual(hints, expected)

    def test_compare_by_words_extra_sentence_MINOR_ISSUE_WITH_PUNCTUATION(self):
        answer = Paragraph([Sentence([Verb('go', 'went'), Punctuation.PERIOD])])
        submission = "go. now. please!"
        hint_paragraph = "go. <bold>now</bold> <bold>.</bold> <bold>please</bold> <bold>!</bold>"

        comparitor = ParagraphComparison(answer, submission)
        hints = comparitor.compare_by_words()
        expected = {
            'error_count': 4,
            'hint_paragraph': hint_paragraph,
            'missing_sentences': -2
        }
        self.assertEqual(hints, expected)


class TestParagraphComparisonHelperFunctions(unittest.TestCase):
    def test_get_word_locations(self):
        submission_str = "I can fly, and you can't."
        spans = get_word_locations(submission_str)
        expected = [(0, 1),  # I
                    (2, 5),  # can
                    (6, 9),  # fly
                    (9, 10),  # ,
                    (11, 14),  # and
                    (15, 18),  # you
                    (19, 24),  # can't
                    (24, 25)]  # .
        self.assertEqual(spans, expected)

    def test_filter_locations_to_remove_is_in_list(self):
        locations = [(1, 2), (3, 4), (5, 6)]
        to_remove = (3, 4)
        answer = filter_locations(locations, to_remove)
        expected = [(1, 2), (5, 6)]
        self.assertEqual(answer, expected)

    def test_filter_locations_remove_spans_two_elements(self):
        locations = [(1, 2), (2, 5), (5, 6), (6, 8)]
        to_remove = (2, 6)
        answer = filter_locations(locations, to_remove)
        expected = [(1, 2), (6, 8)]
        self.assertEqual(answer, expected)

    def test_filter_locations_location_is_equal_high_low(self):
        locations = [(1, 2), (2, 4)]
        to_remove = (2, 2)
        answer = filter_locations(locations, to_remove)
        self.assertEqual(answer, locations)

    def test_find_noun_group_word_not_present(self):
        submission_str = ''
        word = Noun('dog')
        self.assertIsNone(find_noun_group(word, submission_str))

    def test_find_noun_group_all_noun_forms_simple_case(self):
        dogs = [Noun('dog'), Noun('dog').plural(), Noun('dog').indefinite(),
                Noun('dog').definite(), Noun('dog').plural().definite()]
        capital_dogs = [word.capitalize() for word in dogs]
        submission_str = 'go dog go.'
        for word in dogs + capital_dogs:
            answer = find_noun_group(word, submission_str)
            expected = (3, 6)
            self.assertEqual(answer, expected)

    def test_find_noun_group_noun_forms_complex_case(self):
        dogs = [Noun('dog'), Noun('dog').plural(), Noun('dog').indefinite(),
                Noun('dog').definite(), Noun('dog').plural().definite()]
        capital_dogs = [word.capitalize() for word in dogs]
        submission_str = 'a the dogs bark.'
        for word in dogs + capital_dogs:
            answer = find_noun_group(word, submission_str)
            start = submission_str.find('the dogs')
            end = start + len('the dogs')
            self.assertEqual(answer, (start, end))

    def test_find_noun_group_all_prefixes(self):
        prefixes = ['a', 'A', 'an', 'An', 'the', 'The']
        word = Noun('cat')
        for prefix in prefixes:
            submission_str = f'x {prefix} cat '
            answer = find_noun_group(word, submission_str)
            start = 2
            end = start + len(f'{prefix} cat')
            self.assertEqual(answer, (start, end))

    def test_find_noun_group_upper_case(self):
        submission_str = 'the Dogs.'
        word = Noun('dog')
        answer = find_noun_group(word, submission_str)
        start = 0
        end = len('the Dogs')
        self.assertEqual(answer, (start, end))

    def test_find_noun_group_lower_case_edge_case(self):
        submission_str = 'The bMWs'
        word = Noun('BMW')
        self.assertIsNone(find_noun_group(word, submission_str))

    def test_find_noun_group_submission_str_special_rule_regular_plural(self):
        submission_str = 'look at the cute babies.'
        word = Noun('baby')
        answer = find_noun_group(word, submission_str)
        start = submission_str.find('babies')
        end = start + len('babies')
        self.assertEqual(answer, (start, end))

    def test_find_noun_group_submission_str_irregular_plural(self):
        submission_str = 'I loves the feets.'
        base_noun = Noun('foot', 'feet')
        answer = find_noun_group(base_noun, submission_str)
        start = submission_str.find('the feets')
        end = start + len('the feets')
        self.assertEqual(answer, (start, end))

    def test_find_verb_group_verb_not_present(self):
        submission_str = ''
        verb = Verb('play')
        self.assertIsNone(find_verb_group(verb, submission_str))

    def test_find_verb_group_all_verb_forms_simple(self):
        submission_str = 'i go home.'
        go = Verb('go', 'went')
        verbs = [go, go.third_person(), go.negative(), go.negative().third_person(), go.past_tense(),
                 go.negative().past_tense()]
        capital_verbs = [verb.capitalize() for verb in verbs]
        for verb in verbs + capital_verbs:
            answer = find_verb_group(verb, submission_str)
            expected = (2, 4)
            self.assertEqual(answer, expected)

    def test_find_verb_group_all_verb_forms_complex(self):
        submission_str = "i didn't went home."
        go = Verb('go', 'went')
        verbs = [go, go.third_person(), go.negative(), go.negative().third_person(), go.past_tense(),
                 go.negative().past_tense()]
        capital_verbs = [verb.capitalize() for verb in verbs]
        for verb in verbs + capital_verbs:
            answer = find_verb_group(verb, submission_str)
            start = submission_str.find("didn't went")
            end = start + len("didn't went")
            self.assertEqual(answer, (start, end))

    def test_find_verb_group_all_prefixes(self):
        prefixes = ["Don't", "don't", "Doesn't", "doesn't", "Didn't", "didn't"]
        verb = Verb('play')
        for prefix in prefixes:
            submission_str = f'the cat {prefix} play here.'
            answer = find_verb_group(verb, submission_str)
            start = len('the cat ')
            end = start + len(f'{prefix} play')
            self.assertEqual(answer, (start, end))

    def test_find_verb_group_upper_case(self):
        submission_str = 'the dogs Play.'
        word = Verb('play')
        answer = find_verb_group(word, submission_str)
        start = len('the Dogs ')
        end = start + len('Play')
        self.assertEqual(answer, (start, end))

    def test_find_verb_group_submission_str_special_rule_regular_third_person(self):
        submission_str = 'He babies me.'
        word = Verb('baby')
        answer = find_verb_group(word, submission_str)
        start = submission_str.find('babies')
        end = start + len('babies')
        self.assertEqual(answer, (start, end))

    def test_find_verb_group_submission_str_special_rule_regular_past_tense(self):
        submission_str = 'He babied me.'
        word = Verb('baby')
        answer = find_verb_group(word, submission_str)
        start = submission_str.find('babied')
        end = start + len('babied')
        self.assertEqual(answer, (start, end))

    def test_find_verb_group_submission_str_irregular_past(self):
        submission_str = 'I went home.'
        base_verb = Verb('go', 'went')
        answer = find_verb_group(base_verb, submission_str)
        start = submission_str.find('went')
        end = start + len('went')
        self.assertEqual(answer, (start, end))

    def test_find_word_word_not_present(self):
        submission_str = ''
        self.assertIsNone(find_word(BasicWord('x'), submission_str))

    def test_find_word_word_breaks(self):
        submission_str = ' x,'
        word = BasicWord('x')
        answer = find_word(word, submission_str)
        expected = (1, 2)
        self.assertEqual(answer, expected)

    def test_find_word_does_not_allow_substring(self):
        word = BasicWord('x')
        prefixed = 'yx'
        postfixed = 'xy'
        self.assertIsNone(find_word(word, prefixed))
        self.assertIsNone(find_word(word, postfixed))

    def test_find_word_group_noun(self):
        word = Noun('dog')
        submission_str = 'The dogs fly.'
        answer = find_word_group(word, submission_str)
        expected = (0, len('the dogs'))
        self.assertEqual(answer, expected)

    def test_find_word_group_verb(self):
        word = Verb('play')
        submission_str = "a didn't play."
        answer = find_word_group(word, submission_str)
        start = 2
        end = start + len("didn't play")
        self.assertEqual(answer, (start, end))

    def test_find_word_group_other(self):
        word = BasicWord('x')
        submission_str = 'I x.'
        answer = find_word_group(word, submission_str)
        expected = (2, 3)
        self.assertEqual(answer, expected)

    def test_find_word_group_not_present(self):
        submission_str = ''
        for word in (Noun('a'), Verb('a'), BasicWord('a')):
            self.assertIsNone(find_word_group(word, submission_str))

    def test_get_word_returns_AbstractWord_and_location(self):
        submission_str = 'the cat is here.'
        answer = get_word(submission_str, Noun('cat'))
        expected = (BasicWord('the cat'), (0, 7))
        self.assertEqual(answer, expected)

    def test_get_word_returns_missing_and_none_when_missing(self):
        submission_str = ''
        answer = get_word(submission_str, Noun('cat'))
        self.assertEqual(answer, (BasicWord('MISSING'), None))

    def test_get_punctuation_empty_str(self):
        submission_str = ''
        answer = get_punctuation(submission_str)
        self.assertEqual(answer, (BasicWord('MISSING'), None))

    def test_get_punctuation_returns_punctuation_at_end_of_sentence(self):
        submission_str = '! hi.'
        answer = get_punctuation(submission_str)
        self.assertEqual(answer, (Punctuation.PERIOD, (4, 5)))

    def test_get_punctuation_returns_punctuation_at_end_of_sentence_controls_for_whitespace(self):
        submission_str = 'hi!     '
        answer = get_punctuation(submission_str)
        self.assertEqual(answer, (Punctuation.EXCLAMATION, (2, 3)))

    def test_get_punctuation_returns_missing_and_none_when_no_punctuation_at_end_of_sentence(self):
        submission_str = 'hi. there'
        answer = get_punctuation(submission_str)
        self.assertEqual(answer, (BasicWord('MISSING'), None))

    def test_compare_sentences(self):
        sentence = Sentence([Noun('dog').definite().capitalize(), Verb('play').third_person(), Punctuation.PERIOD])
        submission_str = 'The dog plays.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': submission_str,
            'error_count': 0
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_with_error_basic(self):
        sentence = Sentence([Noun('dog').definite().capitalize(), Verb('play').third_person(), Punctuation.PERIOD])
        submission_str = 'A dog played.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': "<bold>A dog</bold> <bold>played</bold>.",
            'error_count': 2
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_punctuation_error(self):
        sentence = Sentence([Verb('go').capitalize(), Punctuation.PERIOD])
        submission_str = 'Go!'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': "Go<bold>!</bold>",
            'error_count': 1
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_missing_punctuation(self):
        sentence = Sentence([Verb('go').capitalize(), Punctuation.PERIOD])
        submission_str = 'Go'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'Go <bold>MISSING</bold>',
            'error_count': 1
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_missing_word_start_of_sentence(self):
        sentence = Sentence([Noun('a'), Verb('b'), Pronoun.HE, Punctuation.PERIOD])
        submission_str = 'b he.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': '<bold>MISSING</bold> b he.',
            'error_count': 1
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_missing_word_middle_of_sentence(self):
        sentence = Sentence([Noun('a'), Verb('b'), Pronoun.HE, Punctuation.PERIOD])
        submission_str = 'a he.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'a <bold>MISSING</bold> he.',
            'error_count': 1
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_extra_word_first_word(self):
        sentence = Sentence([Noun('a'), Verb('b'), Pronoun.HE, Punctuation.PERIOD])
        submission_str = 'c a b he.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': '<bold>c</bold> a b he.',
            'error_count': 1
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_extra_word_middle(self):
        sentence = Sentence([Noun('a'), Verb('b'), Pronoun.HE, Punctuation.PERIOD])
        submission_str = 'a b c he.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'a b <bold>c</bold> he.',
            'error_count': 1
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_extra_word_end(self):
        sentence = Sentence([Noun('a'), Verb('b'), Pronoun.HE, Punctuation.PERIOD])
        submission_str = 'a b he c.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'a b he <bold>c</bold>.',
            'error_count': 1
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_two_extra_words_apart(self):
        sentence = Sentence([Noun('a'), Verb('b'), Pronoun.HE, Punctuation.PERIOD])
        submission_str = 'a c b c he.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'a <bold>c</bold> b <bold>c</bold> he.',
            'error_count': 2
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_two_extra_words_together(self):
        sentence = Sentence([Noun('a'), Verb('b'), Pronoun.HE, Punctuation.PERIOD])
        submission_str = 'a b he c c.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'a b he <bold>c</bold> <bold>c</bold>.',
            'error_count': 2
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_repeating_words_no_errors(self):
        sentence = Sentence(
            [Noun('dog').plural().capitalize(), Verb('dog'), Noun('dog').definite(), Punctuation.PERIOD])
        submission_str = 'Dogs dog the dog.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': submission_str,
            'error_count': 0
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_repeating_words_errors(self):
        sentence = Sentence(
            [Noun('dog').plural().capitalize(), Verb('dog'), Noun('dog').definite(), Punctuation.PERIOD])
        submission_str = 'dog dog dog.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': '<bold>dog</bold> dog <bold>dog</bold>.',
            'error_count': 2
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_single_word_in_wrong_place(self):
        sentence = Sentence([Noun('a'), Noun('b'), Noun('c')])
        submission_str = 'a c b'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'a <bold>c</bold> b',
            'error_count': 1
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_two_words_in_wrong_place(self):
        sentence = Sentence([Noun('a'), Noun('b'), Noun('c'), Noun('d')])
        submission_str = 'a c d b'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'a <bold>c</bold> <bold>d</bold> b',
            'error_count': 2
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_LIMITATION_two_separate_words_in_wrong_place_is_handled_incorrectly(self):
        sentence = Sentence([Noun('a'), Noun('b'), Noun('c'), Noun('d')])
        submission_str = 'd a c b'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': '<bold>d</bold> a c <bold>b</bold>',
            'error_count': 2
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_extra_words_and_wrong_order(self):
        sentence = Sentence([
            Noun('dog').definite().capitalize(), Verb('play').third_person(), BasicWord.preposition('with'),
            Noun('cat').indefinite(), Punctuation.PERIOD
        ])
        submission_str = 'extra The dog extra with extra a cat extra plays extra.'
        answer = compare_sentences(sentence, submission_str)
        extra = '<bold>extra</bold>'
        expected_hint = f'{extra} The dog {extra} <bold>with</bold> {extra} <bold>a cat</bold> {extra} plays {extra}.'
        expected = {
            'hint_sentence': expected_hint,
            'error_count': 7
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_missing_words_and_wrong_order(self):
        sentence = Sentence([Noun('a'), Noun('b'), Noun('c'), Noun('d'), Punctuation.PERIOD])
        submission_str = 'a d c.'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': 'a <bold>MISSING</bold> <bold>d</bold> c.',
            'error_count': 2
        }
        self.assertEqual(answer, expected)

    def test_compare_sentences_does_not_double_count_error_for_wrong_word_and_wrong_order(self):
        sentence = Sentence([Noun('dog').indefinite(), Verb('play').third_person()])
        submission_str = 'play dog'
        answer = compare_sentences(sentence, submission_str)
        expected = {
            'hint_sentence': '<bold>play</bold> <bold>dog</bold>',
            'error_count': 2
        }
        self.assertEqual(answer, expected)
