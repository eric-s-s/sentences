import unittest

from sentences.words.pronoun import Pronoun, Word

I, me, you, he, him, she, her, it, we, us, they, them = Pronoun


class TestPronoun(unittest.TestCase):

    def test_values(self):
        self.assertEqual(I.value, 'I')
        self.assertEqual(me.value, 'me')
        self.assertEqual(you.value, 'you')
        self.assertEqual(he.value, 'he')
        self.assertEqual(him.value, 'him')
        self.assertEqual(she.value, 'she')
        self.assertEqual(her.value, 'her')
        self.assertEqual(it.value, 'it')
        self.assertEqual(we.value, 'we')
        self.assertEqual(us.value, 'us')
        self.assertEqual(they.value, 'they')
        self.assertEqual(them.value, 'them')

    def test_object(self):
        self.assertEqual(I.object(), me)
        self.assertEqual(me.object(), me)
        self.assertEqual(you.object(), you)
        self.assertEqual(he.object(), him)
        self.assertEqual(him.object(), him)
        self.assertEqual(she.object(), her)
        self.assertEqual(her.object(), her)
        self.assertEqual(it.object(), it)
        self.assertEqual(we.object(), us)
        self.assertEqual(us.object(), us)
        self.assertEqual(they.object(), them)
        self.assertEqual(them.object(), them)

    def test_subject(self):
        self.assertEqual(I.subject(), I)
        self.assertEqual(me.subject(), I)
        self.assertEqual(you.subject(), you)
        self.assertEqual(he.subject(), he)
        self.assertEqual(him.subject(), he)
        self.assertEqual(she.subject(), she)
        self.assertEqual(her.subject(), she)
        self.assertEqual(it.subject(), it)
        self.assertEqual(we.subject(), we)
        self.assertEqual(us.subject(), we)
        self.assertEqual(they.subject(), they)
        self.assertEqual(them.subject(), they)

    def test_capitalize(self):
        self.assertEqual(I.capitalize(), Word('I'))
        self.assertEqual(me.capitalize(), Word('Me'))
        self.assertEqual(you.capitalize(), Word('You'))
        self.assertEqual(he.capitalize(), Word('He'))
        self.assertEqual(him.capitalize(), Word('Him'))
        self.assertEqual(she.capitalize(), Word('She'))
        self.assertEqual(her.capitalize(), Word('Her'))
        self.assertEqual(it.capitalize(), Word('It'))
        self.assertEqual(we.capitalize(), Word('We'))
        self.assertEqual(us.capitalize(), Word('Us'))
        self.assertEqual(they.capitalize(), Word('They'))
        self.assertEqual(them.capitalize(), Word('Them'))

    def test_de_capitalize(self):
        self.assertEqual(I.de_capitalize(), Word('i'))
        self.assertEqual(me.de_capitalize(), Word('me'))
        self.assertEqual(you.de_capitalize(), Word('you'))
        self.assertEqual(he.de_capitalize(), Word('he'))
        self.assertEqual(him.de_capitalize(), Word('him'))
        self.assertEqual(she.de_capitalize(), Word('she'))
        self.assertEqual(her.de_capitalize(), Word('her'))
        self.assertEqual(it.de_capitalize(), Word('it'))
        self.assertEqual(we.de_capitalize(), Word('we'))
        self.assertEqual(us.de_capitalize(), Word('us'))
        self.assertEqual(they.de_capitalize(), Word('they'))
        self.assertEqual(them.de_capitalize(), Word('them'))

    def test_is_pair_non_pronoun(self):
        self.assertFalse(me.is_pair('me'))

    def test_is_pair_true_on_pairs(self):
        self.assertTrue(I.is_pair(me))
        self.assertTrue(I.is_pair(I))
        self.assertTrue(he.is_pair(him))
        self.assertTrue(him.is_pair(he))
        self.assertTrue(she.is_pair(her))
        self.assertTrue(her.is_pair(she))
        self.assertTrue(we.is_pair(us))
        self.assertTrue(us.is_pair(we))
        self.assertTrue(them.is_pair(they))
        self.assertTrue(they.is_pair(them))

    def test_is_pair_true_on_equal(self):
        for pronoun in Pronoun:
            self.assertTrue(pronoun.is_pair(pronoun))

    def test_is_pair_false(self):
        pairs = [(I, me), (you, you), (he, him), (she, her), (it, it), (we, us), (they, them)]
        for first in pairs:
            for second in pairs:
                if first != second:
                    self.assertFalse(first[0].is_pair(second[0]))
                    self.assertFalse(first[1].is_pair(second[0]))
                    self.assertFalse(first[0].is_pair(second[1]))
                    self.assertFalse(first[1].is_pair(second[1]))
