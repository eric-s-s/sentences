import unittest

from sentences.words.verb import (NewVerb, PastVerb, ThirdPersonVerb,
                                  NegVerb, NegativePastVerb, NegativeThirdPersonVerb)


class TestVerb(unittest.TestCase):

    def test_verb_no_irregular_past(self):
        verb = NewVerb('play')
        self.assertEqual(verb.value, 'play')
        self.assertEqual(verb.infinitive, 'play')
        self.assertEqual(verb.irregular_past, '')

    def test_verb_irregular_past(self):
        verb = NewVerb('go', '', 'went')
        self.assertEqual(verb.value, 'go')
        self.assertEqual(verb.infinitive, 'go')
        self.assertEqual(verb.irregular_past, 'went')

    def test_verb_repr(self):
        self.assertEqual(repr(NewVerb('play')), "NewVerb('play', 'play', '')")
        self.assertEqual(repr(NewVerb('go', '', 'went')), "NewVerb('go', 'go', 'went')")
        self.assertEqual(repr(ThirdPersonVerb('goes', 'go', 'went')), "ThirdPersonVerb('goes', 'go', 'went')")
        self.assertEqual(repr(NegVerb("don't go", 'go', 'went')), "NegVerb(\"don't go\", 'go', 'went')")

    def test_equality_uses_strict_typing(self):
        self.assertIsInstance(PastVerb('go'), NewVerb)

        self.assertEqual(NewVerb('go'), NewVerb('go'))
        self.assertEqual(PastVerb('go'), PastVerb('go'))
        self.assertNotEqual(NewVerb('go'), PastVerb('go'))

    def test_to_base_verb(self):
        expected = NewVerb('go', '', 'went')
        third = ThirdPersonVerb('goes', 'go', 'went')
        past = PastVerb('went', 'go', 'went')
        negative = NegVerb("don't", 'go', 'went')
        negative_third = NegativeThirdPersonVerb("doesn't go", 'go', 'went')
        negative_past = NegativePastVerb("didn't go", 'go', 'went')

        for verb in (expected, third, past, negative, negative_past, negative_third):
            self.assertEqual(verb.to_base_verb(), expected)

    def test_Verb_past_tense_regular(self):
        regular = NewVerb('play')
        self.assertEqual(regular.past_tense(), PastVerb('played', 'play', ''))

    def test_Verb_past_tense_irregular(self):
        regular = NewVerb('go', '', 'went')
        self.assertEqual(regular.past_tense(), PastVerb('went', 'go', 'went'))

    def test_Verb_past_tense_third_person_and_past_tense_verbs(self):
        expected_past = PastVerb('played', 'play')
        self.assertEqual(PastVerb('played', 'play').past_tense(), expected_past)

        self.assertEqual(ThirdPersonVerb('plays', 'play').past_tense(), expected_past)

    def test_NegativeVerb_past_tense(self):
        expected_past = NegativePastVerb("didn't play", 'play')
        self.assertEqual(expected_past, NegVerb("don't play", 'play').past_tense())
        self.assertEqual(expected_past, NegativeThirdPersonVerb("doesn't play", 'play').past_tense())
        self.assertEqual(expected_past, NegativePastVerb("didn't play", 'play').past_tense())

    def test_Verb_NegativeVerb_negative(self):
        expected_negative = NegVerb("don't play", 'play')
        self.assertEqual(expected_negative, NewVerb('play').negative())
        self.assertEqual(expected_negative, NegVerb("don't play", 'play'))

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
        self.assertEqual(expected, NewVerb('play').third_person())
        self.assertEqual(expected, ThirdPersonVerb('plays', 'play').third_person())
        self.assertEqual(expected, PastVerb('played', 'play').third_person())

    def test_Verb_PastVerb_ThirdPersonVerb_third_person_has(self):
        expected = ThirdPersonVerb('has', 'have', 'had')
        self.assertEqual(expected, NewVerb('have', '', 'had').third_person())
        self.assertEqual(expected, ThirdPersonVerb('has', 'have', 'had').third_person())
        self.assertEqual(expected, PastVerb('had', 'have', 'had').third_person())

    def test_NegativeVerb_all_kinds_third_person(self):
        expected = NegativeThirdPersonVerb("doesn't have", 'have', 'had')
        self.assertEqual(expected, NegVerb("don't have", 'have', 'had').third_person())
        self.assertEqual(expected, NegativeThirdPersonVerb("doesn't have", 'have', 'had').third_person())
        self.assertEqual(expected, NegativePastVerb("didn't have", 'have', 'had').third_person())

    def test_capitalize(self):
        basic = NewVerb('go', '', 'went')
        self.assertEqual(basic.capitalize(), NewVerb('Go', 'go', 'went'))

        third = ThirdPersonVerb('goes', 'go', 'went')
        self.assertEqual(third.capitalize(), ThirdPersonVerb('Goes', 'go', 'went'))

        past = PastVerb('went', 'go', 'went')
        self.assertEqual(past.capitalize(), PastVerb('Went', 'go', 'went'))

        negative = NegVerb("don't go", 'go', 'went')
        self.assertEqual(negative.capitalize(), NegVerb("Don't go", 'go', 'went'))

        negative_third = NegativeThirdPersonVerb("doesn't go", 'go', 'went')
        self.assertEqual(negative_third.capitalize(), NegativeThirdPersonVerb("Doesn't go", 'go', 'went'))

        negative_past = NegativePastVerb("didn't go", 'go', 'went')
        self.assertEqual(negative_past.capitalize(), NegativePastVerb("Didn't go", 'go', 'went'))

    def test_repr(self):
        basic = NewVerb('go', '', 'went')
        self.assertEqual(repr(basic), "NewVerb('go', 'go', 'went')")

        third = ThirdPersonVerb('goes', 'go', 'went')
        self.assertEqual(repr(third), "ThirdPersonVerb('goes', 'go', 'went')")

        past = PastVerb('went', 'go', 'went')
        self.assertEqual(repr(past), "PastVerb('went', 'go', 'went')")

        negative = NegVerb("don't go", 'go', 'went')
        self.assertEqual(repr(negative), "NegVerb(\"don't go\", 'go', 'went')")

        negative_third = NegativeThirdPersonVerb("doesn't go", 'go', 'went')
        self.assertEqual(repr(negative_third), "NegativeThirdPersonVerb(\"doesn't go\", 'go', 'went')")

        negative_past = NegativePastVerb("didn't go", 'go', 'went')
        self.assertEqual(repr(negative_past), "NegativePastVerb(\"didn't go\", 'go', 'went')")

    def test_type_checking(self):
        all_types = [NewVerb, ThirdPersonVerb, PastVerb, NegVerb, NegativePastVerb, NegativeThirdPersonVerb]

        for verb_type in all_types:
            verb = NewVerb('go')
            if verb_type in [NewVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = ThirdPersonVerb('go')
            if verb_type in [NewVerb, ThirdPersonVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = PastVerb('go')
            if verb_type in [NewVerb, PastVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = NegVerb('go')
            if verb_type in [NewVerb, NegVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = NegativePastVerb('go')
            if verb_type in [NewVerb, NegVerb, PastVerb, NegativePastVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)

        for verb_type in all_types:
            verb = NegativeThirdPersonVerb('go')
            if verb_type in [NewVerb, NegVerb, ThirdPersonVerb, NegativeThirdPersonVerb]:
                self.assertIsInstance(verb, verb_type)
            else:
                self.assertNotIsInstance(verb, verb_type)


    #
    # # TODO ugh!
    # def test_verb_eq(self):
    #     c_verb = ConjugatedVerb("don't go", 'go')
    #     n_verb = NegativeVerb('don\'t go', 'go')
    #     self.assertEqual(n_verb.value, "don't go")
    #     self.assertEqual(n_verb.infinitive, "go")
    #
    #     self.assertTrue(n_verb.__eq__(c_verb))
    #     self.assertTrue(c_verb.__eq__(n_verb))
    #     self.assertNotEqual(Verb('go'), n_verb)
    #
    #     basic = BasicVerb('go', 'went')
    #     self.assertEqual(basic.value, 'go')
    #     self.assertEqual(basic.infinitive, 'go')
    #     self.assertTrue(basic.__eq__(Verb('go')))
    #     self.assertTrue(Verb('go').__eq__(basic))
    #
    # def test_conjugated_verb(self):
    #     c_verb = ConjugatedVerb('went', 'go')
    #     self.assertEqual(c_verb.value, 'went')
    #     self.assertEqual(c_verb.infinitive, 'go')
    #
    # def test_conjugated_verb_repr(self):
    #     verb = ConjugatedVerb('don\'t do', 'do')
    #     self.assertEqual(repr(verb), 'ConjugatedVerb("don\'t do", \'do\')')
    #
    # def test_basic_verb_repr(self):
    #     verb = BasicVerb('go', 'went')
    #     self.assertEqual(repr(verb), "BasicVerb('go', 'went', 'go')")
    #
    #     verb = BasicVerb('play')
    #     self.assertEqual(repr(verb), "BasicVerb('play', '', 'play')")
    #
    # def test_basic_verb_value_is_infinitive(self):
    #     verb = BasicVerb('go', 'went')
    #     self.assertEqual(verb.infinitive, 'go')
    #     self.assertEqual(verb.value, 'go')
    #
    # def test_basic_verb_past_tense_regular_verb(self):
    #     verb = BasicVerb('play')
    #     answer = verb.past_tense()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb('played', 'play'))
    #
    #     verb = BasicVerb('bat')
    #     answer = verb.past_tense()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb('batted', 'bat'))
    #
    #     verb = BasicVerb('copy')
    #     answer = verb.past_tense()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb('copied', 'copy'))
    #
    #     verb = BasicVerb('like')
    #     answer = verb.past_tense()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb('liked', 'like'))
    #
    # def test_basic_verb_past_tense_with_irregular_verb(self):
    #     verb = BasicVerb('go', 'went')
    #     answer = verb.past_tense()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb('went', 'go'))
    #
    # def test_basic_verb_third_person(self):
    #     verb = BasicVerb('go', 'went')
    #     answer = verb.third_person()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb('goes', 'go'))
    #
    #     verb = BasicVerb('wax')
    #     answer = verb.third_person()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb('waxes', 'wax'))
    #
    #     verb = BasicVerb('copy')
    #     answer = verb.third_person()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb('copies', 'copy'))
    #
    # def test_basic_verb_third_person_have(self):
    #     verb = BasicVerb('have')
    #     self.assertEqual(verb.third_person(), ConjugatedVerb('has', 'have'))
    #
    # def test_basic_verb_negative(self):
    #     verb = BasicVerb('do', 'did')
    #     answer = verb.negative()
    #     self.assertIsInstance(answer, NegativeVerb)
    #     self.assertEqual(answer.value, 'don\'t do')
    #     self.assertEqual(answer.infinitive, 'do')
    #
    # def test_negative_verb_value_and_infinitive(self):
    #     verb = NegativeVerb('don\'t play', 'play')
    #     self.assertEqual(verb.infinitive, 'play')
    #     self.assertEqual(verb.value, 'don\'t play')
    #
    #     verb = NegativeVerb('do not play', 'play')
    #     self.assertEqual(verb.infinitive, 'play')
    #     self.assertEqual(verb.value, 'do not play')
    #
    # def test_negative_verb_repr(self):
    #     verb = NegativeVerb('don\'t play', 'play')
    #     self.assertEqual(repr(verb), "NegativeVerb(\"don't play\", 'play')")
    #
    # def test_negative_verb_past_tense(self):
    #     verb = NegativeVerb('don\'t play', 'play')
    #     answer = verb.past_tense()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb("didn't play", 'play'))
    #
    #     self.assertEqual(NegativeVerb('do not play', 'play').past_tense(), ConjugatedVerb("did not play", 'play'))
    #
    # def test_negative_verb_third_person(self):
    #     verb = NegativeVerb('don\'t play', 'play')
    #     answer = verb.third_person()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb("doesn't play", 'play'))
    #
    #     self.assertEqual(NegativeVerb('do not play', 'play').third_person(), ConjugatedVerb("does not play", 'play'))
    #
    # def test_negative_verb_past_tense_capitalized(self):
    #     verb = NegativeVerb('don\'t play', 'play').capitalize()
    #     answer = verb.past_tense()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb("didn't play", 'play'))
    #
    #     self.assertEqual(NegativeVerb('Do not play', 'play').past_tense(), ConjugatedVerb("did not play", 'play'))
    #
    # def test_negative_verb_third_person_capitalized(self):
    #     verb = NegativeVerb('don\'t play', 'play').capitalize()
    #     answer = verb.third_person()
    #     self.assertIsInstance(answer, ConjugatedVerb)
    #     self.assertEqual(answer, ConjugatedVerb("doesn't play", 'play'))
    #
    #     self.assertEqual(NegativeVerb('Do not play', 'play').third_person(), ConjugatedVerb("does not play", 'play'))
    #
    # def test_to_basic_verb(self):
    #     verb = Verb('play')
    #     basic = verb.to_basic_verb()
    #     self.assertEqual(verb.value, basic.value)
    #     self.assertEqual(verb.infinitive, basic.infinitive)
    #     self.assertNotEqual(verb, basic)
    #     self.assertIsInstance(basic, BasicVerb)
    #
    # def test_to_basic_verb_does_not_retain_special_past_tense(self):
    #     verb = BasicVerb('go', 'went')
    #     past = verb.past_tense()
    #     from_past_tense = past.to_basic_verb()
    #     from_verb = verb.to_basic_verb()
    #
    #     self.assertEqual(verb, from_past_tense)
    #     self.assertEqual(verb, from_verb)
    #
    #     past_from_past_tense = from_past_tense.past_tense()
    #     past_from_verb = from_verb.past_tense()
    #
    #     self.assertEqual(past_from_past_tense, past_from_verb)
    #     self.assertNotEqual(past, past_from_verb)
    #
    #     self.assertEqual(past.value, 'went')
    #     self.assertEqual(past_from_verb.value, 'goed')
    #
    # def test_to_basic_negative_verb(self):
    #     verb = BasicVerb('play').negative()
    #     self.assertEqual(verb.to_basic_verb(), BasicVerb('play'))
    #
    # def test_capitalize(self):
    #     self.assertEqual(Verb('go').capitalize(), Verb('Go', 'go'))
    #     self.assertEqual(ConjugatedVerb('went', 'go').capitalize(), ConjugatedVerb('Went', 'go'))
    #     self.assertEqual(NegativeVerb('do not go', 'go').capitalize(), NegativeVerb('Do not go', 'go'))
    #     basic = BasicVerb('eat', 'ate')
    #     self.assertEqual(basic.capitalize(), BasicVerb('Eat', 'ate', 'eat'))
    #
    # def test_capitalize_limitations(self):
    #     basic = BasicVerb('eat', 'ate')
    #     self.assertEqual(basic.capitalize().past_tense(), ConjugatedVerb('ate', 'eat'))
    #     self.assertEqual(basic.negative().capitalize().past_tense(), ConjugatedVerb('didn\'t eat', 'eat'))
    #
    # def test_hash(self):
    #     self.assertEqual(hash(Verb('eat', 'ate')), hash("hash of Verb('eat', 'ate')"))
