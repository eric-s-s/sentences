import random
import unittest

from sentences.backend.random_assignments.plurals_assignement import (PluralsAssignment, get_countable_nouns,
                                                                      is_countable_noun)
from sentences.tags.status_tag import StatusTag
from sentences.tags.tags import Tags
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.noun import Noun


class TestPluralsAssignment(unittest.TestCase):
    def test_init(self):
        sentences = [Sentence([BasicWord('x')])]
        tags = Tags([StatusTag.RAW])
        pa = PluralsAssignment(Paragraph(sentences, tags))
        self.assertEqual(pa.raw.sentence_list(), sentences)
        self.assertEqual(pa.raw.tags, tags)

    def test_init_reverts_nouns_if_has_plural(self):
        original_sentences = [Sentence([Noun('x').plural(), Noun('y'),
                                        Noun.uncountable_noun('z'), Noun.proper_noun('A', plural=True)])]
        original_tags = Tags([StatusTag.HAS_PLURALS, StatusTag.RAW])
        original_paragraph = Paragraph(original_sentences, original_tags)
        pa = PluralsAssignment(original_paragraph)

        self.assertEqual(original_paragraph.sentence_list(), original_sentences)
        self.assertEqual(original_paragraph.tags, original_tags)

        expected = [Sentence([Noun('x'), Noun('y'), Noun.uncountable_noun('z'), Noun.proper_noun('A', plural=True)])]
        self.assertEqual(pa.raw.sentence_list(), expected)
        self.assertEqual(pa.raw.tags, Tags([StatusTag.RAW]))

    def test_assign_plurals(self):
        raw_sentences = [
            Sentence([Noun('x'), Noun('y'), BasicWord('z')]),
            Sentence([Noun('z'), Noun('x'), Noun('y')])
        ]
        raw_paragraph = Paragraph(raw_sentences, Tags([StatusTag.RAW]))

        pa = PluralsAssignment(raw_paragraph)

        plurals = [Noun('x'), Noun('z')]
        new = pa.assign_plural(plurals)

        expected = [
            Sentence([Noun('x').plural(), Noun('y'), BasicWord('z')]),
            Sentence([Noun('z').plural(), Noun('x').plural(), Noun('y')])
        ]
        self.assertEqual(new.sentence_list(), expected)
        self.assertEqual(new.tags, Tags([StatusTag.RAW, StatusTag.HAS_PLURALS]))

    def test_assign_random_plurals_lte_zero(self):
        raw_sentences = [Sentence([Noun('a')]), Sentence([Noun('b'), Noun('c')])]
        paragraph = Paragraph(raw_sentences)
        pa = PluralsAssignment(paragraph)

        new_paragraph = pa.assign_random_plurals(0.0)
        self.assertEqual(new_paragraph.sentence_list(), raw_sentences)
        self.assertEqual(new_paragraph.tags, Tags([StatusTag.HAS_PLURALS]))

        new_paragraph = pa.assign_random_plurals(-0.1)
        self.assertEqual(new_paragraph.sentence_list(), raw_sentences)
        self.assertEqual(new_paragraph.tags, Tags([StatusTag.HAS_PLURALS]))

    def test_assign_random_plurals_gte_one(self):
        raw_sentences = [Sentence([Noun('a')]), Sentence([Noun('b'), Noun('c')])]
        paragraph = Paragraph(raw_sentences)
        pa = PluralsAssignment(paragraph)

        expected = [Sentence([Noun('a').plural()]), Sentence([Noun('b').plural(), Noun('c').plural()])]

        new_paragraph = pa.assign_random_plurals(1.0)
        self.assertEqual(new_paragraph.sentence_list(), expected)
        self.assertEqual(new_paragraph.tags, Tags([StatusTag.HAS_PLURALS]))

        new_paragraph = pa.assign_random_plurals(1.1)
        self.assertEqual(new_paragraph.sentence_list(), expected)
        self.assertEqual(new_paragraph.tags, Tags([StatusTag.HAS_PLURALS]))

    def test_is_countable_noun_true(self):
        base = Noun('dog')
        self.assertTrue(is_countable_noun(base))
        self.assertTrue(is_countable_noun(base.plural()))
        self.assertTrue(is_countable_noun(base.definite()))
        self.assertTrue(is_countable_noun(base.indefinite()))
        self.assertTrue(is_countable_noun(base.capitalize().bold()))

    def test_is_countable_noun_false(self):
        self.assertFalse(is_countable_noun(BasicWord('dog')))
        self.assertFalse(is_countable_noun(Noun.uncountable_noun('water')))
        self.assertFalse(is_countable_noun(Noun.proper_noun('Joe', plural=False)))
        self.assertFalse(is_countable_noun(Noun.proper_noun('the Joes', plural=True)))

    def test_get_countable_nouns(self):
        sentence_list = [Sentence([Noun.uncountable_noun('water'), BasicWord('is'), Noun('pig')]),
                         Sentence([Noun.proper_noun('Joe'), Noun('pig'), Noun('dog')])]
        paragraph = Paragraph(sentence_list)
        self.assertEqual(get_countable_nouns(paragraph), [Noun('pig'), Noun('dog')])

    def test_get_countable_nouns_reverts_to_basic_nouns(self):
        sentence_list = [Sentence([Noun.uncountable_noun('water'), BasicWord('is'),
                                   Noun('pig').plural().definite().capitalize()]),
                         Sentence([Noun.proper_noun('Joe'), Noun('pig').indefinite(),
                                   Noun('dog').plural()])]
        paragraph = Paragraph(sentence_list)
        self.assertEqual(get_countable_nouns(paragraph), [Noun('pig'), Noun('dog')])

    def test_assign_random_plurals_middle(self):
        random.seed(124)
        word_lists = [Sentence([Noun('a'), Noun('b'), Noun('c')])]
        paragraph = Paragraph(word_lists)
        pa = PluralsAssignment(paragraph)

        expected_plurals = [[Noun('c')],
                            [Noun('b')],
                            [Noun('a'), Noun('b')],
                            [Noun('b'), Noun('c')],
                            [Noun('a'), Noun('b'), Noun('c')]]
        for index in range(5):
            new_paragraph = pa.assign_random_plurals(0.5)

            plurals = expected_plurals[index]
            test_paragraph = pa.assign_plural(plurals)
            self.assertEqual(new_paragraph.sentence_list(), test_paragraph.sentence_list())

    def test_assign_random_plurals_add_tag(self):
        paragraph = Paragraph([], Tags([StatusTag.RAW]))
        answer = PluralsAssignment(paragraph).assign_random_plurals(0.5)
        self.assertEqual(answer.tags, Tags([StatusTag.RAW, StatusTag.HAS_PLURALS]))
