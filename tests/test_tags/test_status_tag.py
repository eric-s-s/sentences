import unittest

from sentences.tags.status_tag import StatusTag
from sentences.tags.tags import Tags


class TestStatusTag(unittest.TestCase):
    def test_sorted_members(self):
        expected = [StatusTag.RAW, StatusTag.HAS_PLURALS, StatusTag.HAS_NEGATIVES,
                    StatusTag.SIMPLE_PRESENT, StatusTag.SIMPLE_PAST,
                    StatusTag.NOUN_ERRORS, StatusTag.PRONOUN_ERRORS,
                    StatusTag.VERB_ERRORS, StatusTag.IS_DO_ERRORS,
                    StatusTag.PREPOSITION_ERRORS, StatusTag.PUNCTUATION_ERRORS]

        all_tags = StatusTag.__members__.values()
        self.assertEqual(sorted(all_tags), expected)

    def test_repr(self):
        for name in ('RAW', 'HAS_PLURALS', 'HAS_NEGATIVES',
                     'SIMPLE_PRESENT', 'SIMPLE_PAST',
                     'NOUN_ERRORS', 'PRONOUN_ERRORS', 'VERB_ERRORS', 'IS_DO_ERRORS',
                     'PREPOSITION_ERRORS', 'PUNCTUATION_ERRORS'):
            tag = getattr(StatusTag, name)
            self.assertEqual(repr(tag), 'StatusTag.{}'.format(name))

    def test_with_tag_object(self):
        tags = Tags([StatusTag.RAW, StatusTag.SIMPLE_PAST])
        other_tags = Tags([StatusTag.SIMPLE_PAST, StatusTag.RAW])
        self.assertEqual(tags, other_tags)
        self.assertEqual(repr(tags), repr(other_tags))

        self.assertTrue(tags.has(StatusTag.RAW))
        self.assertFalse(tags.has(StatusTag.NOUN_ERRORS))
