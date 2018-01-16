import unittest

from sentences.words.pronoun import Pronoun, Word

I, me, you, he, him, she, her, it, we, us, they, them = Pronoun.lowers()


class TestPronoun(unittest.TestCase):

    def setUp(self):
        self.lower_names = ['I', 'ME', 'YOU', 'HE', 'HIM', 'SHE', 'HER', 'IT', 'WE', 'US', 'THEY', 'THEM']
        self.upper_names = ['CAPITAL_{}'.format(name) for name in self.lower_names]

    def test_values(self):
        lower_values = ['I', 'me', 'you', 'he', 'him', 'she', 'her', 'it', 'we', 'us', 'they', 'them']
        upper_values = [value.capitalize() for value in lower_values]
        for name, value in zip(self.lower_names + self.upper_names, lower_values + upper_values):
            self.assertEqual(getattr(Pronoun, name).value, value)

    def test_lowers(self):
        expected = [getattr(Pronoun, name) for name in self.lower_names]
        self.assertEqual(Pronoun.lowers(), expected)

    def test_uppers(self):
        expected = [getattr(Pronoun, name) for name in self.upper_names]
        self.assertEqual(Pronoun.uppers(), expected)

    def test_is_upper_case_true(self):
        print(Pronoun.uppers())
        self.assertTrue(all(p_noun.is_upper_case() for p_noun in Pronoun.uppers()))

    def test_object(self):
        subjs = [I, you, he, she, it, we, they]
        objs = [me, you, him, her, it, us, them]
        for index, subj in enumerate(subjs):
            self.assertEqual(subj.object(), objs[index])
            self.assertEqual(subj.capitalize().object(), objs[index].capitalize())

        # self.assertEqual(I.object(), me)
        # self.assertEqual(me.object(), me)
        # self.assertEqual(you.object(), you)
        # self.assertEqual(he.object(), him)
        # self.assertEqual(him.object(), him)
        # self.assertEqual(she.object(), her)
        # self.assertEqual(her.object(), her)
        # self.assertEqual(it.object(), it)
        # self.assertEqual(we.object(), us)
        # self.assertEqual(us.object(), us)
        # self.assertEqual(they.object(), them)
        # self.assertEqual(them.object(), them)

    # def test_subject(self):
    #     self.assertEqual(I.subject(), I)
    #     self.assertEqual(me.subject(), I)
    #     self.assertEqual(you.subject(), you)
    #     self.assertEqual(he.subject(), he)
    #     self.assertEqual(him.subject(), he)
    #     self.assertEqual(she.subject(), she)
    #     self.assertEqual(her.subject(), she)
    #     self.assertEqual(it.subject(), it)
    #     self.assertEqual(we.subject(), we)
    #     self.assertEqual(us.subject(), we)
    #     self.assertEqual(they.subject(), they)
    #     self.assertEqual(them.subject(), they)
    #
    def test_capitalize(self):
        self.assertEqual(I.capitalize(), Pronoun.CAPITAL_I)
        self.assertEqual(me.capitalize(), Pronoun.CAPITAL_ME)
        self.assertEqual(you.capitalize(), Pronoun.CAPITAL_YOU)
        self.assertEqual(he.capitalize(), Pronoun.CAPITAL_HE)
        self.assertEqual(him.capitalize(), Pronoun.CAPITAL_HIM)
        self.assertEqual(she.capitalize(), Pronoun.CAPITAL_SHE)
        self.assertEqual(her.capitalize(), Pronoun.CAPITAL_HER)
        self.assertEqual(it.capitalize(), Pronoun.CAPITAL_IT)
        self.assertEqual(we.capitalize(), Pronoun.CAPITAL_WE)
        self.assertEqual(us.capitalize(), Pronoun.CAPITAL_US)
        self.assertEqual(they.capitalize(), Pronoun.CAPITAL_THEY)
        self.assertEqual(them.capitalize(), Pronoun.CAPITAL_THEM)

    # def test_bold(self):
    #     self.assertEqual(I.bold(), Word('<bold>I</bold>'))
    #
    # def test_is_pair_non_pronoun(self):
    #     self.assertFalse(me.is_pair('me'))
    #
    # def test_is_pair_true_on_pairs(self):
    #     self.assertTrue(I.is_pair(me))
    #     self.assertTrue(I.is_pair(I))
    #     self.assertTrue(he.is_pair(him))
    #     self.assertTrue(him.is_pair(he))
    #     self.assertTrue(she.is_pair(her))
    #     self.assertTrue(her.is_pair(she))
    #     self.assertTrue(we.is_pair(us))
    #     self.assertTrue(us.is_pair(we))
    #     self.assertTrue(them.is_pair(they))
    #     self.assertTrue(they.is_pair(them))
    #
    # def test_is_pair_true_on_equal(self):
    #     for pronoun in Pronoun:
    #         self.assertTrue(pronoun.is_pair(pronoun))
    #
    # def test_is_pair_false(self):
    #     pairs = [(I, me), (you, you), (he, him), (she, her), (it, it), (we, us), (they, them)]
    #     for first in pairs:
    #         for second in pairs:
    #             if first != second:
    #                 self.assertFalse(first[0].is_pair(second[0]))
    #                 self.assertFalse(first[1].is_pair(second[0]))
    #                 self.assertFalse(first[0].is_pair(second[1]))
    #                 self.assertFalse(first[1].is_pair(second[1]))
