import unittest

from sentences.tags.tags import Tags
from sentences.tags.wordtag import WordTag
from sentences.words.basicword import BasicWord
from sentences.words.be_verb import BeVerb
from sentences.words.wordtools.abstractword import AbstractWord


class TestBeVerb(unittest.TestCase):

    def test_registered_subclass(self):
        self.assertTrue(isinstance(BeVerb.IS, AbstractWord))

    def test_values(self):
        expected_pairs = [
            (BeVerb.AM, 'am'), (BeVerb.IS, 'is'), (BeVerb.ARE, 'are'),
            (BeVerb.AM_NOT, 'am not'), (BeVerb.IS_NOT, 'is not'), (BeVerb.ARE_NOT, 'are not'),
            (BeVerb.WAS, 'was'), (BeVerb.WERE, 'were'),
            (BeVerb.WAS_NOT, 'was not'), (BeVerb.WERE_NOT, 'were not')
        ]
        for word, value in expected_pairs:
            self.assertEqual(word.value, value)

    def test_tags(self):
        self.assertEqual(BeVerb.AM.tags, Tags())
        self.assertEqual(BeVerb.IS.tags, Tags([WordTag.THIRD_PERSON]))
        self.assertEqual(BeVerb.ARE.tags, Tags())

        self.assertEqual(BeVerb.AM_NOT.tags, Tags([WordTag.NEGATIVE]))
        self.assertEqual(BeVerb.IS_NOT.tags, Tags([WordTag.NEGATIVE, WordTag.THIRD_PERSON]))
        self.assertEqual(BeVerb.ARE_NOT.tags, Tags([WordTag.NEGATIVE]))

        self.assertEqual(BeVerb.WAS.tags, Tags([WordTag.PAST]))
        self.assertEqual(BeVerb.WERE.tags, Tags([WordTag.PAST]))

        self.assertEqual(BeVerb.WAS_NOT.tags, Tags([WordTag.PAST, WordTag.NEGATIVE]))
        self.assertEqual(BeVerb.WERE_NOT.tags, Tags([WordTag.PAST, WordTag.NEGATIVE]))

    def test_has_tags_true(self):
        self.assertTrue(BeVerb.IS_NOT.has_tags())
        self.assertTrue(BeVerb.IS_NOT.has_tags(WordTag.THIRD_PERSON))
        self.assertTrue(BeVerb.IS_NOT.has_tags(WordTag.NEGATIVE))
        self.assertTrue(BeVerb.IS_NOT.has_tags(WordTag.THIRD_PERSON, WordTag.NEGATIVE))

    def test_has_tags_false(self):
        self.assertFalse(BeVerb.IS_NOT.has_tags(WordTag.PAST))
        self.assertFalse(BeVerb.IS_NOT.has_tags(WordTag.THIRD_PERSON, WordTag.PAST))

    def test_capitalize(self):
        expected = BasicWord('Is not')
        self.assertEqual(BeVerb.IS_NOT.capitalize(), expected)

    def test_de_capitalize(self):
        for member in BeVerb.__members__.values():
            self.assertEqual(member.de_capitalize(), member)

    def test_bold(self):
        expected = BasicWord("<bold>is not</bold>")
        self.assertEqual(BeVerb.IS_NOT.bold(), expected)

    def test_negative_already_negative(self):
        self.assertEqual(BeVerb.AM_NOT.negative(), BeVerb.AM_NOT)
        self.assertEqual(BeVerb.IS_NOT.negative(), BeVerb.IS_NOT)
        self.assertEqual(BeVerb.ARE_NOT.negative(), BeVerb.ARE_NOT)

        self.assertEqual(BeVerb.WAS_NOT.negative(), BeVerb.WAS_NOT)
        self.assertEqual(BeVerb.WERE_NOT.negative(), BeVerb.WERE_NOT)

    def test_negative(self):
        self.assertEqual(BeVerb.AM.negative(), BeVerb.AM_NOT)
        self.assertEqual(BeVerb.IS.negative(), BeVerb.IS_NOT)
        self.assertEqual(BeVerb.ARE.negative(), BeVerb.ARE_NOT)

        self.assertEqual(BeVerb.WAS.negative(), BeVerb.WAS_NOT)
        self.assertEqual(BeVerb.WERE.negative(), BeVerb.WERE_NOT)

    def test_past_tense_already_past_tense(self):
        self.assertEqual(BeVerb.WAS.past_tense(), BeVerb.WAS)
        self.assertEqual(BeVerb.WAS_NOT.past_tense(), BeVerb.WAS_NOT)
        self.assertEqual(BeVerb.WERE.past_tense(), BeVerb.WERE)
        self.assertEqual(BeVerb.WERE_NOT.past_tense(), BeVerb.WERE_NOT)

    def test_past_tense(self):
        self.assertEqual(BeVerb.AM.past_tense(), BeVerb.WAS)
        self.assertEqual(BeVerb.AM_NOT.past_tense(), BeVerb.WAS_NOT)

        self.assertEqual(BeVerb.IS.past_tense(), BeVerb.WAS)
        self.assertEqual(BeVerb.IS_NOT.past_tense(), BeVerb.WAS_NOT)

        self.assertEqual(BeVerb.ARE.past_tense(), BeVerb.WERE)
        self.assertEqual(BeVerb.ARE_NOT.past_tense(), BeVerb.WERE_NOT)
