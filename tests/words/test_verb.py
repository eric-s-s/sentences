import unittest

from sentences.words.verb import (Verb, PastVerb, ThirdPersonVerb,
                                  NegativeVerb, NegativePastVerb, NegativeThirdPersonVerb)


class TestVerb(unittest.TestCase):

    def test_verb_no_irregular_past(self):
        verb = Verb('play')
        self.assertEqual(verb.value, 'play')
        self.assertEqual(verb.infinitive, 'play')
        self.assertEqual(verb.irregular_past, '')

    def test_verb_irregular_past(self):
        verb = Verb('go', '', 'went')
        self.assertEqual(verb.value, 'go')
        self.assertEqual(verb.infinitive, 'go')
        self.assertEqual(verb.irregular_past, 'went')

    def test_verb_repr(self):
        self.assertEqual(repr(Verb('play')), "Verb('play', 'play', '')")
        self.assertEqual(repr(Verb('go', '', 'went')), "Verb('go', 'go', 'went')")
        self.assertEqual(repr(ThirdPersonVerb('goes', 'go', 'went')), "ThirdPersonVerb('goes', 'go', 'went')")
        self.assertEqual(repr(NegativeVerb("don't go", 'go', 'went')), "NegativeVerb(\"don't go\", 'go', 'went')")

    def test_equality_uses_strict_typing(self):
        self.assertIsInstance(PastVerb('go'), Verb)

        self.assertEqual(Verb('go'), Verb('go'))
        self.assertEqual(PastVerb('go'), PastVerb('go'))
        self.assertNotEqual(Verb('go'), PastVerb('go'))

    def test_to_base_verb(self):
        expected = Verb('go', '', 'went')
        third = ThirdPersonVerb('goes', 'go', 'went')
        past = PastVerb('went', 'go', 'went')
        negative = NegativeVerb("don't", 'go', 'went')
        negative_third = NegativeThirdPersonVerb("doesn't go", 'go', 'went')
        negative_past = NegativePastVerb("didn't go", 'go', 'went')

        for verb in (expected, third, past, negative, negative_past, negative_third):
            self.assertEqual(verb.to_base_verb(), expected)

    def test_Verb_past_tense_regular(self):
        regular = Verb('play')
        self.assertEqual(regular.past_tense(), PastVerb('played', 'play', ''))

    def test_Verb_past_tense_irregular(self):
        regular = Verb('go', '', 'went')
        self.assertEqual(regular.past_tense(), PastVerb('went', 'go', 'went'))

    def test_Verb_past_tense_third_person_and_past_tense_verbs(self):
        expected_past = PastVerb('played', 'play')
        self.assertEqual(PastVerb('played', 'play').past_tense(), expected_past)

        self.assertEqual(ThirdPersonVerb('plays', 'play').past_tense(), expected_past)

    def test_NegativeVerb_past_tense(self):
        expected_past = NegativePastVerb("didn't play", 'play')
        self.assertEqual(expected_past, NegativeVerb("don't play", 'play').past_tense())
        self.assertEqual(expected_past, NegativeThirdPersonVerb("doesn't play", 'play').past_tense())
        self.assertEqual(expected_past, NegativePastVerb("didn't play", 'play').past_tense())

    def test_Verb_NegativeVerb_negative(self):
        expected_negative = NegativeVerb("don't play", 'play')
        self.assertEqual(expected_negative, Verb('play').negative())
        self.assertEqual(expected_negative, NegativeVerb("don't play", 'play'))

    def test_ThirdPersonVerb_NegativeThirdPerson_negative(self):
        expected = NegativeThirdPersonVerb("doesn't play", 'play')
        self.assertEqual(expected, ThirdPersonVerb('plays', 'play').negative())
        self.assertEqual(expected, NegativeThirdPersonVerb("doesn't play", 'play').negative())

    def test_PastVerb_NegativePastVerb_negative(self):
        expected = NegativePastVerb("didn't play", 'play')
        self.assertEqual(expected, PastVerb('played', 'play').negative())
        self.assertEqual(expected, NegativePastVerb("didn't play", 'play').negative())

    def test_Verb_PastVerb_ThirdPersonVerb_third_person(self):
        expected = ThirdPersonVerb('plays', 'play')
        self.assertEqual(expected, Verb('play').third_person())
        self.assertEqual(expected, ThirdPersonVerb('plays', 'play').third_person())
        self.assertEqual(expected, PastVerb('played', 'play').third_person())

    def test_Verb_PastVerb_ThirdPersonVerb_third_person_has(self):
        expected = ThirdPersonVerb('has', 'have', 'had')
        self.assertEqual(expected, Verb('have', '', 'had').third_person())
        self.assertEqual(expected, ThirdPersonVerb('has', 'have', 'had').third_person())
        self.assertEqual(expected, PastVerb('had', 'have', 'had').third_person())

    def test_NegativeVerb_all_kinds_third_person(self):
        expected = NegativeThirdPersonVerb("doesn't have", 'have', 'had')
        self.assertEqual(expected, NegativeVerb("don't have", 'have', 'had').third_person())
        self.assertEqual(expected, NegativeThirdPersonVerb("doesn't have", 'have', 'had').third_person())
        self.assertEqual(expected, NegativePastVerb("didn't have", 'have', 'had').third_person())

    def test_capitalize(self):
        basic = Verb('go', '', 'went')
        self.assertEqual(basic.capitalize(), Verb('Go', 'go', 'went'))

        third = ThirdPersonVerb('goes', 'go', 'went')
        self.assertEqual(third.capitalize(), ThirdPersonVerb('Goes', 'go', 'went'))

        past = PastVerb('went', 'go', 'went')
        self.assertEqual(past.capitalize(), PastVerb('Went', 'go', 'went'))

        negative = NegativeVerb("don't go", 'go', 'went')
        self.assertEqual(negative.capitalize(), NegativeVerb("Don't go", 'go', 'went'))

        negative_third = NegativeThirdPersonVerb("doesn't go", 'go', 'went')
        self.assertEqual(negative_third.capitalize(), NegativeThirdPersonVerb("Doesn't go", 'go', 'went'))

        negative_past = NegativePastVerb("didn't go", 'go', 'went')
        self.assertEqual(negative_past.capitalize(), NegativePastVerb("Didn't go", 'go', 'went'))

    def test_repr(self):
        basic = Verb('go', '', 'went')
        self.assertEqual(repr(basic), "Verb('go', 'go', 'went')")

        third = ThirdPersonVerb('goes', 'go', 'went')
        self.assertEqual(repr(third), "ThirdPersonVerb('goes', 'go', 'went')")

        past = PastVerb('went', 'go', 'went')
        self.assertEqual(repr(past), "PastVerb('went', 'go', 'went')")

        negative = NegativeVerb("don't go", 'go', 'went')
        self.assertEqual(repr(negative), "NegativeVerb(\"don't go\", 'go', 'went')")

        negative_third = NegativeThirdPersonVerb("doesn't go", 'go', 'went')
        self.assertEqual(repr(negative_third), "NegativeThirdPersonVerb(\"doesn't go\", 'go', 'went')")

        negative_past = NegativePastVerb("didn't go", 'go', 'went')
        self.assertEqual(repr(negative_past), "NegativePastVerb(\"didn't go\", 'go', 'went')")

    def test_type_checking(self):
        all_types = [Verb, ThirdPersonVerb, PastVerb, NegativeVerb, NegativePastVerb, NegativeThirdPersonVerb]

        for verb_type in all_types:
            verb = Verb('go')
            if verb_type in [Verb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = ThirdPersonVerb('go')
            if verb_type in [Verb, ThirdPersonVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = PastVerb('go')
            if verb_type in [Verb, PastVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = NegativeVerb('go')
            if verb_type in [Verb, NegativeVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = NegativePastVerb('go')
            if verb_type in [Verb, NegativeVerb, PastVerb, NegativePastVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = NegativeThirdPersonVerb('go')
            if verb_type in [Verb, NegativeVerb, ThirdPersonVerb, NegativeThirdPersonVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

    def test_equality_by_all_three_values_and_type(self):
        test = Verb('a', 'b', 'c')
        by_value = Verb('q', 'b', 'c')
        by_infinitive = Verb('a', 'q', 'c')
        by_irregular = Verb('a', 'b', 'q')

        for verb in [by_infinitive, by_value, by_irregular]:
            self.assertNotEqual(test, verb)

        self.assertEqual(test, Verb('a', 'b', 'c'))

    def test_equality_all_types_type_specific(self):
        verb_types = [Verb, PastVerb, ThirdPersonVerb, NegativeVerb, NegativeThirdPersonVerb, NegativePastVerb]
        for verb_type in verb_types:
            for test_against in verb_types:
                first = verb_type('a', 'b', 'c')
                second = test_against('a', 'b', 'c')
                if verb_type == test_against:
                    self.assertEqual(first, second)
                else:
                    self.assertNotEqual(first, second)

    def test_hash_all(self):
        verb_types = [Verb, PastVerb, ThirdPersonVerb, NegativeVerb, NegativeThirdPersonVerb, NegativePastVerb]
        for class_ in verb_types:
            instance = class_('play')
            self.assertEqual(hash(instance), hash('hash of {!r}'.format(instance)))
