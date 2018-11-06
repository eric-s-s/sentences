import random
import unittest

from sentences.tags.wordtag import WordTag


class TestWordTag(unittest.TestCase):
    def test_all_members(self):
        member_list = list(WordTag.__members__.values())
        self.assertEqual(member_list,
                         [
                             WordTag.UNCOUNTABLE,
                             WordTag.PLURAL,
                             WordTag.DEFINITE,
                             WordTag.INDEFINITE,
                             WordTag.PROPER,
                             WordTag.THIRD_PERSON,
                             WordTag.NEGATIVE,
                             WordTag.PAST,
                             WordTag.PREPOSITION,
                             WordTag.SEPARABLE_PARTICLE
                         ])

    def test_all_reprs(self):
        self.assertEqual(repr(WordTag.PAST), 'WordTag.PAST')
        for wt in WordTag.__members__.values():
            self.assertEqual(repr(wt), 'WordTag.' + wt.name)

    def test_is_sortable(self):
        list_1 = list(WordTag.__members__.values())
        list_2 = list(WordTag.__members__.values())
        random.shuffle(list_1)
        random.shuffle(list_2)
        self.assertEqual(sorted(list_1), sorted(list_2))
