import random
import unittest

from sentences.backend.random_assignments.assign_random_negatives import assign_random_negatives
from sentences.tags.status_tag import StatusTag
from sentences.tags.tags import Tags
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.verb import Verb


class TestAssignRandomNegatives(unittest.TestCase):
    def setUp(self):
        self.sentence_list = [Sentence([BasicWord('a'), Verb('b'), BasicWord('c')]),
                              Sentence([BasicWord('d'), Verb('e')])]
        self.tags = Tags([StatusTag.RAW, StatusTag.HAS_PLURALS])
        self.paragraph = Paragraph(self.sentence_list, self.tags)

    def test_p_negative_lte_zero(self):
        to_test = assign_random_negatives(self.paragraph, p_negative=0.0)
        self.assertEqual(to_test.sentence_list(), self.sentence_list)
        self.assertEqual(to_test.tags, self.tags.add(StatusTag.HAS_NEGATIVES))

        to_test = assign_random_negatives(self.paragraph, p_negative=-0.1)
        self.assertEqual(to_test.sentence_list(), self.sentence_list)

    def test_p_negative_gte_one(self):
        expected_list = [Sentence([BasicWord('a'), Verb('b').past_tense(), BasicWord('c')]),
                         Sentence([BasicWord('d'), Verb('e').past_tense()])]

        to_test = assign_random_negatives(self.paragraph, p_negative=1.0)
        self.assertEqual(to_test.sentence_list(), expected_list)
        self.assertEqual(to_test.tags, self.tags.add(StatusTag.HAS_NEGATIVES))

        to_test = assign_random_negatives(self.paragraph, p_negative=1.1)
        self.assertEqual(to_test.sentence_list(), expected_list)
        self.assertEqual(to_test.tags, self.tags.add(StatusTag.HAS_NEGATIVES))

    def test_p_negative_middle_value(self):
        random.seed(489)
        past_verbs = [[Verb('e')],
                      [Verb('b')],
                      [],
                      [Verb('b')],
                      [Verb('b'), Verb('e')]]
        for index in range(5):
            to_test = assign_random_negatives(self.paragraph, 0.5)
            expected = self.paragraph
            for verb in past_verbs[index]:
                indices = self.paragraph.find(verb)[0]
                expected = expected.set(*indices, verb.past_tense())
            self.assertEqual(to_test.sentence_list(), expected.sentence_list())
