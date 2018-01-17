import unittest

from sentences.words.pronoun import Pronoun, Word, CapitalPronoun, AbstractPronoun

I, me, you, he, him, she, her, it, we, us, they, them = Pronoun


class DummyPronoun(AbstractPronoun):
    I = 'a'
    ME = 'b'

    YOU = 'c'

    HE = 'd'
    HIM = 'e'

    SHE = 'f'
    HER = 'g'

    IT = 'h'

    WE = 'i'
    US = 'j'

    THEY = 'k'
    THEM = 'l'

    def capitalize(self):
        return self

    def de_capitalize(self):
        return self


class TestAbstractPronoun(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pronoun = DummyPronoun
        cls.names = ['I', 'ME', 'YOU', 'HE', 'HIM', 'SHE', 'HER', 'IT', 'WE', 'US', 'THEY', 'THEM']
        cls.values = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

    def test_order(self):
        p_list = list(self.pronoun.__members__.values())
        expected = [getattr(self.pronoun, name) for name in self.names]
        self.assertEqual(p_list, expected)

    def test_pronoun_values(self):
        for name, value in zip(self.names, self.values):
            self.assertEqual(getattr(self.pronoun, name).value, value)
        
    def test_pronoun_object(self):
        self.assertEqual(self.pronoun.I.object(), self.pronoun.ME)
        self.assertEqual(self.pronoun.ME.object(), self.pronoun.ME)
        self.assertEqual(self.pronoun.YOU.object(), self.pronoun.YOU)
        self.assertEqual(self.pronoun.HE.object(), self.pronoun.HIM)
        self.assertEqual(self.pronoun.HIM.object(), self.pronoun.HIM)
        self.assertEqual(self.pronoun.SHE.object(), self.pronoun.HER)
        self.assertEqual(self.pronoun.HER.object(), self.pronoun.HER)
        self.assertEqual(self.pronoun.IT.object(), self.pronoun.IT)
        self.assertEqual(self.pronoun.WE.object(), self.pronoun.US)
        self.assertEqual(self.pronoun.US.object(), self.pronoun.US)
        self.assertEqual(self.pronoun.THEY.object(), self.pronoun.THEM)
        self.assertEqual(self.pronoun.THEM.object(), self.pronoun.THEM)

    def test_pronoun_subject(self):
        self.assertEqual(self.pronoun.I.subject(), self.pronoun.I)
        self.assertEqual(self.pronoun.ME.subject(), self.pronoun.I)
        self.assertEqual(self.pronoun.YOU.subject(), self.pronoun.YOU)
        self.assertEqual(self.pronoun.HE.subject(), self.pronoun.HE)
        self.assertEqual(self.pronoun.HIM.subject(), self.pronoun.HE)
        self.assertEqual(self.pronoun.SHE.subject(), self.pronoun.SHE)
        self.assertEqual(self.pronoun.HER.subject(), self.pronoun.SHE)
        self.assertEqual(self.pronoun.IT.subject(), self.pronoun.IT)
        self.assertEqual(self.pronoun.WE.subject(), self.pronoun.WE)
        self.assertEqual(self.pronoun.US.subject(), self.pronoun.WE)
        self.assertEqual(self.pronoun.THEY.subject(), self.pronoun.THEY)
        self.assertEqual(self.pronoun.THEM.subject(), self.pronoun.THEY)

    # def test_pronoun_capitalize(self):
    #     self.assertEqual(self.pronoun.I.capitalize(), CapitalPronoun.I)
    #     self.assertEqual(self.pronoun.ME.capitalize(), CapitalPronoun.ME)
    #     self.assertEqual(self.pronoun.YOU.capitalize(), CapitalPronoun.YOU)
    #     self.assertEqual(self.pronoun.HE.capitalize(), CapitalPronoun.HE)
    #     self.assertEqual(self.pronoun.HIM.capitalize(), CapitalPronoun.HIM)
    #     self.assertEqual(self.pronoun.SHE.capitalize(), CapitalPronoun.SHE)
    #     self.assertEqual(self.pronoun.HER.capitalize(), CapitalPronoun.HER)
    #     self.assertEqual(self.pronoun.IT.capitalize(), CapitalPronoun.IT)
    #     self.assertEqual(self.pronoun.WE.capitalize(), CapitalPronoun.WE)
    #     self.assertEqual(self.pronoun.US.capitalize(), CapitalPronoun.US)
    #     self.assertEqual(self.pronoun.THEY.capitalize(), CapitalPronoun.THEY)
    #     self.assertEqual(self.pronoun.THEM.capitalize(), CapitalPronoun.THEM)

    def test_bold(self):
        self.assertEqual(self.pronoun.I.bold(), Word('<bold>{}</bold>'.format(self.pronoun.I.value)))

    def test_is_pair_non_pronoun(self):
        self.assertFalse(self.pronoun.ME.is_pair('me'))

    def test_is_pair_different_type_pronoun(self):
        self.assertFalse(self.pronoun.I.is_pair(CapitalPronoun.I))

    def test_is_pair_true_on_pairs(self):
        self.assertTrue(self.pronoun.I.is_pair(self.pronoun.ME))
        self.assertTrue(self.pronoun.I.is_pair(self.pronoun.I))
        self.assertTrue(self.pronoun.HE.is_pair(self.pronoun.HIM))
        self.assertTrue(self.pronoun.HIM.is_pair(self.pronoun.HE))
        self.assertTrue(self.pronoun.SHE.is_pair(self.pronoun.HER))
        self.assertTrue(self.pronoun.HER.is_pair(self.pronoun.SHE))
        self.assertTrue(self.pronoun.WE.is_pair(self.pronoun.US))
        self.assertTrue(self.pronoun.US.is_pair(self.pronoun.WE))
        self.assertTrue(self.pronoun.THEM.is_pair(self.pronoun.THEY))
        self.assertTrue(self.pronoun.THEY.is_pair(self.pronoun.THEM))

    def test_is_pair_true_on_equal(self):
        for pronoun in Pronoun:
            self.assertTrue(pronoun.is_pair(pronoun))

    def test_is_pair_false(self):
        pairs = [(self.pronoun.I, self.pronoun.ME),
                 (self.pronoun.YOU, self.pronoun.YOU),
                 (self.pronoun.HE, self.pronoun.HIM),
                 (self.pronoun.SHE, self.pronoun.HER),
                 (self.pronoun.IT, self.pronoun.IT),
                 (self.pronoun.WE, self.pronoun.US),
                 (self.pronoun.THEY, self.pronoun.THEM)]
        for first in pairs:
            for second in pairs:
                if first != second:
                    self.assertFalse(first[0].is_pair(second[0]))
                    self.assertFalse(first[1].is_pair(second[0]))
                    self.assertFalse(first[0].is_pair(second[1]))
                    self.assertFalse(first[1].is_pair(second[1]))


class TestPronoun(unittest.TestCase):

    def test_pronoun_values(self):
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

    def test_pronoun_object(self):
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

    def test_pronoun_subject(self):
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

    def test_pronoun_capitalize(self):
        self.assertEqual(I.capitalize(), CapitalPronoun.I)
        self.assertEqual(me.capitalize(), CapitalPronoun.ME)
        self.assertEqual(you.capitalize(), CapitalPronoun.YOU)
        self.assertEqual(he.capitalize(), CapitalPronoun.HE)
        self.assertEqual(him.capitalize(), CapitalPronoun.HIM)
        self.assertEqual(she.capitalize(), CapitalPronoun.SHE)
        self.assertEqual(her.capitalize(), CapitalPronoun.HER)
        self.assertEqual(it.capitalize(), CapitalPronoun.IT)
        self.assertEqual(we.capitalize(), CapitalPronoun.WE)
        self.assertEqual(us.capitalize(), CapitalPronoun.US)
        self.assertEqual(they.capitalize(), CapitalPronoun.THEY)
        self.assertEqual(them.capitalize(), CapitalPronoun.THEM)

    def test_bold(self):
        self.assertEqual(I.bold(), Word('<bold>I</bold>'))

    def test_is_pair_non_pronoun(self):
        self.assertFalse(me.is_pair('me'))

    def test_is_pair_different_type_pronoun(self):
        self.assertFalse(I.is_pair(CapitalPronoun.I))

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
