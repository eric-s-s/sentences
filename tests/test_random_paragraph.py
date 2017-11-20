import random
import unittest


from sentences.words.word import Word
from sentences.words.verb import BasicVerb
from sentences.words.noun import Noun
from sentences.words.punctuation import Punctuation
from sentences.words.pronoun import Pronoun

from sentences.random_paragraph import RandomParagraph, get_subj


class TestRandomParagraph(unittest.TestCase):
    def test_get_subj_does_not_pick_subj_in_predicate(self):
        predicate = [Word('hi')]
        pool = [Word('hi'), Word('ho')]
        random.seed(5)
        for _ in range(10):
            self.assertEqual(get_subj(pool, predicate), Word('ho'))

    def test_get_subj_raises_value_error(self):
        predicate = [Word('hi')]
        pool = [Word('hi')]
        self.assertRaises(ValueError, get_subj, pool, predicate)

    def test_get_subj_random_selection(self):
        predicate = [Word('oops'), Word('I'), Word('orangutan')]
        pool = [Word('orangutan'), Word('chimpanzee'), Word('monkey'), Word('loser'), Word('baby')]

        random.seed(10)
        self.assertEqual(get_subj(pool, predicate), Word('baby'))
        self.assertEqual(get_subj(pool, predicate), Word('baby'))
        self.assertEqual(get_subj(pool, predicate), Word('loser'))
        self.assertEqual(get_subj(pool, predicate), Word('loser'))
        self.assertEqual(get_subj(pool, predicate), Word('chimpanzee'))
        self.assertEqual(get_subj(pool, predicate), Word('chimpanzee'))
        self.assertEqual(get_subj(pool, predicate), Word('monkey'))

    def test_get_subject_pool_never_repeats(self):
        random.seed(10)
        rp = RandomParagraph()

        answer = rp.get_subject_pool(10)
        self.assertEqual(answer,
                         [Noun('pony'), Noun('ant'), Noun('stinky tofu'), Noun('house'), Noun('cow'), Pronoun.IT,
                          Noun('fire fighter'), Noun('money'), Noun('baby'), Noun('car')])

        answer = rp.get_subject_pool(10)
        self.assertEqual(answer,
                         [Noun('pen'), Noun('stinky tofu'), Noun('shark'), Pronoun.HE, Noun('car'), Noun('water'),
                          Noun('school'), Noun('baby'), Noun('fire fighter'), Noun('poop')])

        answer = rp.get_subject_pool(10)
        self.assertEqual(answer,
                         [Noun('leaf'), Noun('school'), Noun('bicycle'), Noun('cow'), Noun('pineapple'),
                          Noun('baby'), Noun('stinky tofu'), Noun('thunder'), Pronoun.SHE, Noun('orange')])

    def test_get_subject_pool_raises_overflow_error(self):
        random.seed(100)
        three_nouns = 'tests/test_files/three_nouns.csv'
        rp = RandomParagraph(uncountable_file=three_nouns, countable_file=three_nouns, p_pronoun=0.5)
        all_nouns_and_pronouns = rp.get_subject_pool(10)
        self.assertEqual(len(all_nouns_and_pronouns), 10)

        self.assertRaises(OverflowError, rp.get_subject_pool, 11)

    def test_create_pool_paragraph_is_correct_length(self):
        rp = RandomParagraph()
        for length in range(3, 11):
            pool = length - 2
            answer = rp.create_pool_paragraph(pool, length)
            self.assertEqual(len(answer), length)

    def test_create_pool_paragraph_subjects_in_subject_pool_and_not_in_predicate(self):
        random.seed(20)
        rp = RandomParagraph()
        paragraph = rp.create_pool_paragraph(pool_size=3, num_sentences=10)

        subjects = [Noun('cake'), Noun('child', 'children'), Noun('homework')]
        for sentence in paragraph:
            subject = sentence[0]
            predicate = sentence[1:]
            self.assertIn(subject, subjects)
            self.assertNotIn(subject, predicate)

    def test_create_pool_paragraph_raises_overflow_error_very_very_edge_case(self):
        random.seed(20)
        two_nouns = 'tests/test_files/two_nouns.csv'
        bring = 'tests/test_files/bring.csv'
        raise_error = RandomParagraph(uncountable_file=two_nouns, countable_file=two_nouns, verb_file=bring,
                                      p_pronoun=0.0)
        self.assertRaises(OverflowError, raise_error.create_pool_paragraph, 2, 10)
        no_error = RandomParagraph(uncountable_file=two_nouns, countable_file=two_nouns, p_pronoun=0.0)
        no_error.create_pool_paragraph(2, 100)

    def test_create_pool_paragraph_output(self):
        random.seed(100)
        rp = RandomParagraph()
        paragraph = rp.create_pool_paragraph(2, 5)
        expected = [
            [Pronoun.IT, BasicVerb('show'), Noun('octopus'), Noun('sand'), Punctuation.PERIOD],
            [Noun('eagle'), BasicVerb('bring', 'brought'), Noun('fish', 'fish'), Noun('gold'), Punctuation.PERIOD],
            [Pronoun.IT, BasicVerb('excite'), Noun('poop'), Punctuation.PERIOD],
            [Noun('eagle'), BasicVerb('cook'),  Pronoun.HER,  Punctuation.PERIOD],
            [Noun('eagle'), BasicVerb('use'), Noun('shark'),  Punctuation.EXCLAMATION]
        ]
        self.assertEqual(paragraph, expected)

    def test_create_chain_paragraph_is_correct_length(self):
        rp = RandomParagraph()
        for length in range(3, 11):
            answer = rp.create_chain_paragraph(length)
            self.assertEqual(len(answer), length)

    def test_create_chain_paragraph_loop_safety_finally_returns_paragraph_with_repeat_words(self):
        random.seed(20)
        two_nouns = 'tests/test_files/two_nouns.csv'
        bring = 'tests/test_files/bring.csv'
        repeats = RandomParagraph(uncountable_file=two_nouns, countable_file=two_nouns, verb_file=bring, p_pronoun=0.0)
        paragraph = repeats.create_chain_paragraph(3)
        expected = [
            [Noun('joe'), BasicVerb('bring', 'brought'), Noun('bob'), Noun('joe'), Punctuation.PERIOD],
            [Noun('joe'), BasicVerb('bring', 'brought'), Noun('joe'), Noun('bob'), Punctuation.PERIOD],
            [Noun('bob'), BasicVerb('bring', 'brought'), Noun('joe'), Noun('bob'), Punctuation.EXCLAMATION],
        ]
        self.assertEqual(expected, paragraph)

    def test_create_chain_paragraph_pronouns(self):
        rp = RandomParagraph(p_pronoun=1.0, verb_file='tests/test_files/jump_on.csv')
        answer = rp.create_chain_paragraph(10)
        for back_index, sentence in enumerate(answer[1:]):
            previous_obj = answer[back_index][-2]
            current_subj = sentence[0]
            self.assertEqual(previous_obj.subject(), current_subj)

    def test_create_chain_paragraph_nouns(self):
        rp = RandomParagraph(p_pronoun=0.0)
        answer = rp.create_chain_paragraph(10)
        for back_index, sentence in enumerate(answer[1:]):
            previous_obj = answer[back_index][-2]
            current_subj = sentence[0]
            self.assertEqual(previous_obj, current_subj)

    def test_create_chain_paragraph_assigns_random_subj_if_no_obj(self):
        random.seed(11)
        rp = RandomParagraph(verb_file='tests/test_files/intransitive.csv')
        answer = rp.create_chain_paragraph(3)
        expected = [
            [Noun('uncle'), BasicVerb('die'), Punctuation.PERIOD],
            [Noun('wife'), BasicVerb('live'), Punctuation.PERIOD],
            [Noun('sheep', 'sheep'), BasicVerb('jump'), Punctuation.EXCLAMATION]
        ]
        self.assertEqual(expected, answer)

    def test_create_chain_paragraph_output(self):
        random.seed(4)
        rp = RandomParagraph()
        answer = rp.create_chain_paragraph(4)
        expected = [
            [Noun('box'), BasicVerb('sleep', 'slept'), Word('on'), Noun('child', 'children'), Punctuation.PERIOD],
            [Noun('child', 'children'), BasicVerb('break', 'broke'), Pronoun.US, Punctuation.PERIOD],
            [Pronoun.WE, BasicVerb('teach', 'taught'), Noun('banana'), Noun('tree'), Punctuation.PERIOD],
            [Noun('tree'), BasicVerb('fight', 'fought'), Noun('stinky tofu'), Punctuation.PERIOD]
        ]
        self.assertEqual(answer, expected)
