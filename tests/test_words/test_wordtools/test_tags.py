import unittest

import random

from sentences.words.wordtools.tags import Tags
from sentences.words.wordtools.wordtag import WordTag


class TestTags(unittest.TestCase):
    def test_init_empty(self):
        test = Tags()
        self.assertEqual(test.to_list(), [])

    def test_init_non_empty(self):
        all_tags = sorted(WordTag.__members__.values())
        self.assertEqual(Tags(all_tags).to_list(), all_tags)

    def test_init_no_repeat_values(self):
        one_tag = Tags([WordTag.PAST])
        repeat = Tags([WordTag.PAST, WordTag.PAST])

        self.assertEqual(one_tag.to_list(), [WordTag.PAST])
        self.assertEqual(repeat.to_list(), [WordTag.PAST])

        self.assertEqual(one_tag, repeat)

        self.assertEqual(repr(repeat), 'Tags([WordTag.PAST])')

    def test_init_initial_list_is_not_pointed_to(self):
        tag_list = [WordTag.PAST, WordTag.DEFINITE]
        tags = Tags(tag_list)
        tag_list[0] = 'oops'

        self.assertEqual(tags.to_list(), [WordTag.DEFINITE, WordTag.PAST])

    def test_to_list_is_sorted(self):
        all_tags = sorted(WordTag.__members__.values())
        shuffled = all_tags[:]
        random.shuffle(shuffled)

        test = Tags(shuffled)
        self.assertEqual(test.to_list(), all_tags)

    def test_add_element_not_present(self):
        tags = Tags()
        new_tags = tags.add(WordTag.PAST)

        self.assertEqual(tags.to_list(), [])
        self.assertEqual(new_tags.to_list(), [WordTag.PAST])

        new_tags = new_tags.add(WordTag.DEFINITE)

        self.assertEqual(new_tags.to_list(), [WordTag.DEFINITE, WordTag.PAST])

    def test_add_element_already_present(self):
        tags = Tags([WordTag.PAST])
        new = tags.add(WordTag.PAST)
        self.assertEqual(new.to_list(), [WordTag.PAST])

    def test_remove_element_not_present(self):
        tags = Tags([WordTag.PAST])
        new = tags.remove(WordTag.DEFINITE)
        self.assertEqual(new.to_list(), [WordTag.PAST])

    def test_remove_element_present(self):
        tags = Tags([WordTag.PAST])
        new = tags.remove(WordTag.PAST)
        self.assertEqual(tags.to_list(), [WordTag.PAST])
        self.assertEqual(new.to_list(), [])

    def test_has_true(self):
        tags = Tags(list(WordTag.__members__.values()))
        for tag in WordTag.__members__.values():
            self.assertTrue(tags.has(tag))

    def test_has_false(self):
        tags = Tags([WordTag.PAST, WordTag.DEFINITE])

        for tag in WordTag.__members__.values():
            if tag not in [WordTag.PAST, WordTag.DEFINITE]:
                self.assertFalse(tags.has(tag))

    def has_true_and_false(self):
        tags = Tags([WordTag.PAST, WordTag.DEFINITE])

        self.assertTrue(tags.has(WordTag.DEFINITE))
        self.assertTrue(tags.has(WordTag.PAST))

        self.assertFalse(tags.has(WordTag.THIRD_PERSON))

    def test_copy(self):
        tags = Tags([WordTag.THIRD_PERSON, WordTag.PAST])
        new_tags = tags.copy()
        self.assertIsNot(tags, new_tags)
        self.assertEqual(tags, new_tags)

    def test_equality(self):
        tags = Tags([WordTag.THIRD_PERSON, WordTag.DEFINITE])
        equal_tags = Tags([WordTag.DEFINITE, WordTag.THIRD_PERSON, WordTag.THIRD_PERSON])
        self.assertEqual(tags.to_list(), equal_tags.to_list())
        self.assertEqual(tags, equal_tags)

        self.assertNotEqual(tags, Tags([WordTag.THIRD_PERSON, WordTag.DEFINITE, WordTag.PAST]))

    def test_equality_not_WordTag(self):
        self.assertNotEqual(Tags(), [])

    def test_repr(self):
        tag_list = [WordTag.DEFINITE, WordTag.PAST]
        reverse = [WordTag.PAST, WordTag.DEFINITE]

        expected = 'Tags([WordTag.DEFINITE, WordTag.PAST])'

        self.assertEqual(repr(Tags(tag_list)), expected)
        self.assertEqual(repr(Tags(reverse)), expected)
