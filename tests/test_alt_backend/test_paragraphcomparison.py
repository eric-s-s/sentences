import unittest

from sentences.alt_backend.new_grammarizer import NewGrammarizer
from sentences.alt_backend.paragraph_comparison import ParagraphComparison, compare_sentences, get_word_list, \
    get_noun_groupings, get_verb_groupings, find_word_group
from sentences.tags.status_tag import StatusTag
from sentences.tags.tags import Tags
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.noun import Noun
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

    def test_find_word_group_noun(self):
        dogs = [Noun('dog'), Noun('dog').plural(), Noun('dog').indefinite(),
                Noun('dog').definite(), Noun('dog').plural().definite()]
        capital_dogs = [word.capitalize() for word in dogs]
        submission_str = 'The dog barks.'
        for word in dogs + capital_dogs:
            answer = find_word_group(word, submission_str)
            expected = (0, 7)
            self.assertEqual(answer, expected)

    def test_find_word_group_noun_submission_str_capitalized(self):
        dogs = [Noun('dog'), Noun('dog').plural(), Noun('dog').indefinite(),
                Noun('dog').definite(), Noun('dog').plural().definite()]
        capital_dogs = [word.capitalize() for word in dogs]
        submission_str = 'Dogs bark.'
        for word in dogs + capital_dogs:
            answer = find_word_group(word, submission_str)
            expected = (0, 4)
            print(word)
            self.assertEqual(answer, expected)


    # def test_function_compare_sentences_strings_are_equal(self):
    #     sentence = Sentence(
    #         [Noun('dog').indefinite().capitalize(), Verb('like').third_person(), Noun('cat').indefinite(),
    #          Punctuation.PERIOD])
    #
    #     self.assertEqual(str(sentence), 'A dog likes a cat.')
    #     submission_str = 'A dog likes a cat.'
    #     hints = compare_sentences(sentence, submission_str)
    #     expected = {
    #         'error_count': 0,
    #         'hint_sentence': "A dog likes a cat.",
    #     }
    #     self.assertEqual(hints, expected)
    #
    # def test_function_compare_sentences_different_noun(self):
    #     sentence = Sentence(
    #         [Noun('dog').indefinite().capitalize(), Verb('like').third_person(), Noun('cat').indefinite(),
    #          Punctuation.PERIOD])
    #
    #     self.assertEqual(str(sentence), 'A dog likes a cat.')
    #     submission_str = 'The dog likes a cat.'
    #     hints = compare_sentences(sentence, submission_str)
    #     expected = {
    #         'error_count': 1,
    #         'hint_sentence': "<bold>The dog<bold> likes a cat.",
    #     }
    #     self.assertEqual(hints, expected)
    #
    #
    #
    #
    #
    # def test_compare_by_word_answer_correct(self):
    #     answer = Paragraph([
    #         Sentence([BasicWord('I'), BasicWord('like'), BasicWord('squirrels'), Punctuation.PERIOD]),
    #         Sentence([BasicWord('a'), BasicWord('b'), BasicWord('c'), Punctuation.PERIOD])
    #     ])
    #     submission_str = "I like squirrels. a b c."
    #     comparitor = ParagraphComparison(answer, submission_str)
    #     hints = comparitor.compare_by_words()
    #     expected = {
    #         'error_count': 0,
    #         'hint_paragraph': submission_str,
    #         'missing_sentences': 0
    #     }
    #     self.assertEqual(hints, expected)

# TODO probably remove this
# def test_function_get_word_list_separates_by_spaces(self):
#     submission_str = "a b c"
#     self.assertEqual(get_word_list(submission_str), ['a', 'b', 'c'])
#
# def test_function_get_word_list_separates_by_punctuation(self):
#     submission_str = "a,b.c?d!e"
#     self.assertEqual(get_word_list(submission_str), ['a', ',', 'b', '.', 'c', '?', 'd', '!', 'e'])
#
# def test_function_get_word_list_deals_with_exra_white_spaces(self):
#     submission_str = "a,  b  c . d"
#     self.assertEqual(get_word_list(submission_str), ["a", ",", "b", "c", ".", "d"])
#
# def test_function_get_noun_groupings_no_articles(self):
#     word_list = ["pigs", "can", "fly", "."]
#     self.assertEqual(get_noun_groupings(word_list), word_list)
#
# def test_function_get_noun_groupings_one_article(self):
#     for article in ("a", "an", "A", "An", "the", "The"):
#         word_list = [article, "thing", "other_thing"]
#         expected = [f"{article} thing", "other_thing"]
#         self.assertEqual(get_noun_groupings(word_list), expected)
#
# def test_function_get_noun_groupings_corner_case_an_a(self):
#     word_list = ['an', 'a', 'the', 'a', 'a', 'b']
#     self.assertEqual(get_noun_groupings(word_list), ['an a', 'the a', 'a b'])
#
# def test_function_get_verb_groupings_no_articles(self):
#     word_list = ["pigs", "fly", "."]
#     self.assertEqual(get_verb_groupings(word_list), word_list)
#
# def test_function_get_verb_groupings_one_article(self):
#     for  in ("a", "an", "A", "An", "the", "The"):
#         word_list = [article, "thing", "other_thing"]
#         expected = [f"{article} thing", "other_thing"]
#         self.assertEqual(get_verb_groupings(word_list), expected)
#
# def test_function_get_verb_groupings_corner_case_an_a(self):
#     word_list = ['an', 'a', 'the', 'a', 'a', 'b']
#     self.assertEqual(get_verb_groupings(word_list), ['an a', 'the a', 'a b'])
