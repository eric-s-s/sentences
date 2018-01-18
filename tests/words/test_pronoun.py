import unittest

from sentences.words.pronoun import Pronoun, Word, CapitalPronoun, AbstractPronoun


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

    def test_bold(self):
        for pronoun in self.pronoun.__members__.values():
            self.assertEqual(pronoun.bold(), Word('<bold>{}</bold>'.format(pronoun.value)))

    def test_is_pair_non_pronoun(self):
        self.assertFalse(self.pronoun.ME.is_pair('me'))

    def test_is_pair_different_type_pronoun(self):
        other_type = Pronoun
        if self.pronoun == Pronoun:
            other_type = CapitalPronoun
        self.assertFalse(self.pronoun.I.is_pair(other_type.I))

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


class TestPronoun(TestAbstractPronoun):

    @classmethod
    def setUpClass(cls):
        super(TestPronoun, cls).setUpClass()
        cls.pronoun = Pronoun
        cls.values = ['I', 'me', 'you', 'he', 'him', 'she', 'her', 'it', 'we', 'us', 'they', 'them']

    def test_pronoun_capitalize(self):
        for name in self.names:
            current = getattr(self.pronoun, name)
            capital = getattr(CapitalPronoun, name)
            self.assertEqual(current.capitalize(), capital)

    def test_pronoun_de_capitalize(self):
        for pronoun in self.pronoun.__members__.values():
            self.assertEqual(pronoun.de_capitalize(), pronoun)


class TestCapitalPronoun(TestAbstractPronoun):

    @classmethod
    def setUpClass(cls):
        super(TestCapitalPronoun, cls).setUpClass()
        cls.pronoun = CapitalPronoun
        cls.values = ['I', 'Me', 'You', 'He', 'Him', 'She', 'Her', 'It', 'We', 'Us', 'They', 'Them']

    def test_pronoun_de_capitalize(self):
        for name in self.names:
            current = getattr(self.pronoun, name)
            lower = getattr(Pronoun, name)
            self.assertEqual(current.de_capitalize(), lower)

    def test_pronoun_capitalize(self):
        for pronoun in self.pronoun.__members__.values():
            self.assertEqual(pronoun.capitalize(), pronoun)
