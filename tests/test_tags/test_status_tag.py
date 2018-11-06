import unittest

from sentences.tags.status_tag import StatusTag
from sentences.tags.tags import Tags


class TestStatusTag(unittest.TestCase):
    def test_sorted_members(self):
        expected = [StatusTag.RAW, StatusTag.HAS_PLURALS, StatusTag.HAS_NEGATIVES,
                    StatusTag.GRAMMATICAL, StatusTag.HAS_ERRORS]
        all_tags = StatusTag.__members__.values()
        self.assertEqual(sorted(all_tags), expected)

    def test_repr(self):
        for name in ('RAW', 'HAS_PLURALS', 'HAS_NEGATIVES', 'GRAMMATICAL', 'HAS_ERRORS'):
            tag = getattr(StatusTag, name)
            self.assertEqual(repr(tag), 'StatusTag.{}'.format(name))

    def test_with_tag_object(self):
        tags = Tags([StatusTag.RAW, StatusTag.GRAMMATICAL])
        other_tags = Tags([StatusTag.GRAMMATICAL, StatusTag.RAW])
        self.assertEqual(tags, other_tags)
        self.assertEqual(repr(tags), repr(other_tags))

        self.assertTrue(tags.has(StatusTag.RAW))
        self.assertFalse(tags.has(StatusTag.HAS_ERRORS))
