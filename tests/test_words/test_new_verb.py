import unittest

from sentences.words.new_verb import NewVerb
from sentences.words.wordtools.tags import Tags
from sentences.words.wordtools.wordtag import WordTag
from sentences.words.basicword import BasicWord


class TestNewVerb(unittest.TestCase):

    def setUp(self):
        self.past = Tags([WordTag.PAST])
        self.third_person = Tags([WordTag.THIRD_PERSON])
        self.negative = Tags([WordTag.NEGATIVE])

        self.negative_past = Tags([WordTag.NEGATIVE, WordTag.PAST])
        self.negative_third_person = Tags([WordTag.NEGATIVE, WordTag.THIRD_PERSON])

    def test_noun_values(self):
        test = NewVerb('a', 'b', 'c', Tags([WordTag.NEGATIVE]))
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_past, 'b')
        self.assertEqual(test.infinitive, 'c')
        self.assertEqual(test.tags, Tags([WordTag.NEGATIVE]))

    def test_noun_empty_values(self):
        test = NewVerb('a')
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_past, '')
        self.assertEqual(test.infinitive, 'a')
        self.assertEqual(test.tags, Tags([]))

    def test_equality_true_false_by_value(self):
        test = NewVerb('a', 'b', 'c', tags=self.past)
        equal = NewVerb('a', 'b', 'c', tags=self.past)
        not_equal = NewVerb('x', 'b', 'c', tags=self.past)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_equality_true_false_by_irregular_past(self):
        test = NewVerb('a', 'b', 'c', tags=self.past)
        equal = NewVerb('a', 'b', 'c', tags=self.past)
        not_equal = NewVerb('a', 'x', 'c', tags=self.past)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_equality_true_false_by_base_noun(self):
        test = NewVerb('a', 'b', 'c', tags=self.past)
        equal = NewVerb('a', 'b', 'c', tags=self.past)
        not_equal = NewVerb('a', 'b', 'x', tags=self.past)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_equality_true_false_by_tags(self):
        test = NewVerb('a', 'b', 'c', tags=self.past)
        equal = NewVerb('a', 'b', 'c', tags=self.past)
        not_equal = NewVerb('a', 'b', 'c', tags=self.negative_past)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_eq_must_be_noun(self):
        self.assertNotEqual(NewVerb('go'), BasicWord('go'))

    def test_repr(self):
        self.assertEqual(repr(NewVerb('bob')), "NewVerb('bob', '', 'bob', Tags([]))")
        self.assertEqual(repr(NewVerb('go', 'went').past_tense()),
                         "NewVerb('went', 'went', 'go', Tags([WordTag.PAST]))")
        self.assertEqual(repr(NewVerb('play').negative().third_person()),
                         "NewVerb(\"doesn't play\", '', 'play', Tags([WordTag.THIRD_PERSON, WordTag.NEGATIVE]))")

    def test_hash(self):
        self.assertEqual(hash(NewVerb('bob')),
                         hash("hash of NewVerb('bob', '', 'bob', Tags([]))"))

        hash_val = "hash of NewVerb('plays', '', 'play', Tags([WordTag.THIRD_PERSON]))"
        self.assertEqual(hash(NewVerb('play').third_person()), hash(hash_val))

    def test_capitalize(self):
        verb = NewVerb('go', 'went').past_tense().negative().capitalize()
        self.assertEqual(verb, NewVerb("Didn't go", 'went', 'go', tags=self.negative_past))

    def test_de_capitalize(self):
        verb = NewVerb('go', 'went').past_tense().negative()
        self.assertEqual(verb, verb.capitalize().de_capitalize())

    def test_bold(self):
        verb = NewVerb('go', 'went', tags=self.negative)
        self.assertEqual(verb.bold(), NewVerb('<bold>go</bold>', 'went', 'go', tags=self.negative))

    def test_past_tense_regular_verb(self):
        verb = NewVerb('play')
        self.assertEqual(verb.past_tense(), NewVerb('played', '', 'play', tags=self.past))

        verb = NewVerb('baby')
        self.assertEqual(verb.past_tense(), NewVerb('babied', '', 'baby', tags=self.past))

        verb = NewVerb('plan')
        self.assertEqual(verb.past_tense(), NewVerb('planned', '', 'plan', tags=self.past))

    def test_past_tense_irregular_verb(self):
        verb = NewVerb('go', 'went')
        self.assertEqual(verb.past_tense(), NewVerb('went', 'went', 'go', tags=self.past))

    def test_past_tense_third_person(self):
        verb = NewVerb('plays', '', 'play', tags=self.third_person)
        self.assertEqual(verb.past_tense(), NewVerb('played', '', 'play', tags=self.past))

    def test_past_tense_negative_verb(self):
        verb = NewVerb("don't play", '', 'play', tags=self.negative)
        same_result = NewVerb("doesn't play", '', 'play', tags=self.negative_third_person)
        expected = NewVerb("didn't play", '', 'play', tags=self.negative_past)
        self.assertEqual(verb.past_tense(), expected)
        self.assertEqual(same_result.past_tense(), expected)

    def test_past_tense_past_verb(self):
        verb = NewVerb('played', '', 'play', tags=self.past)
        negative = verb.negative()
        self.assertNotEqual(verb, negative)

        self.assertEqual(verb.past_tense(), verb)
        self.assertEqual(verb.past_tense().past_tense(), verb)
        self.assertEqual(negative.past_tense(), negative)
        self.assertEqual(negative.past_tense().past_tense(), negative)

    def test_third_person_basic_verb(self):
        verb = NewVerb('play')
        self.assertEqual(verb.third_person(), NewVerb('plays', '', 'play', tags=self.third_person))

        verb = NewVerb('go', 'went')
        self.assertEqual(verb.third_person(), NewVerb('goes', 'went', 'go', tags=self.third_person))

    def test_third_person_past_verb(self):
        verb = NewVerb('went', 'went', 'go', tags=self.past)
        self.assertEqual(verb.third_person(), NewVerb('goes', 'went', 'go', tags=self.third_person))

    def test_third_person_negative_verb(self):
        verb = NewVerb("don't go", 'went', 'go', tags=self.negative)
        same_result = NewVerb("didn't go", 'went', 'go', tags=self.negative_past)
        expected = NewVerb("doesn't go", 'went', 'go', tags=self.negative_third_person)

        self.assertEqual(verb.third_person(), expected)
        self.assertEqual(same_result.third_person(), expected)

    def test_third_person_third_person_verb(self):
        verb = NewVerb('plays', '', 'play', tags=self.third_person)
        self.assertEqual(verb.third_person(), verb)
        self.assertEqual(verb.third_person().third_person(), verb)

        negative = NewVerb("doesn't play", '', 'play', tags=self.negative_third_person)
        self.assertEqual(negative.third_person(), negative)
        self.assertEqual(negative.third_person().third_person(), negative)

    def test_third_person_special_case(self):
        verb = NewVerb('have', 'had')
        past = verb.past_tense()
        expected = NewVerb('has', 'had', 'have', tags=self.third_person)

        self.assertEqual(verb.third_person(), expected)
        self.assertEqual(past.third_person(), expected)

    def test_negative_basic_verb(self):
        verb = NewVerb('play')
        self.assertEqual(verb.negative(), NewVerb("don't play", '', 'play', tags=self.negative))

        verb = NewVerb('have', 'had')
        self.assertEqual(verb.negative(), NewVerb("don't have", 'had', 'have', tags=self.negative))

    def test_negative_third_person_verb(self):
        verb = NewVerb('plays', '', 'play', tags=self.third_person)
        self.assertEqual(verb.negative(), NewVerb("doesn't play", '', 'play', tags=self.negative_third_person))

    def test_negative_past_verb(self):
        verb = NewVerb('played', '', 'play', tags=self.past)
        self.assertEqual(verb.negative(), NewVerb("didn't play", '', 'play', tags=self.negative_past))

        verb = NewVerb('went', 'went', 'go', tags=self.past)
        self.assertEqual(verb.negative(), NewVerb("didn't go", 'went', 'go', tags=self.negative_past))

    def test_negative_with_negative_verb(self):
        verb = NewVerb("don't play", '', 'play', tags=self.negative)
        self.assertEqual(verb.negative(), verb)
        self.assertEqual(verb.negative().negative(), verb)

        verb = NewVerb("doesn't play", '', 'play', tags=self.negative_third_person)
        self.assertEqual(verb.negative(), verb)

        verb = NewVerb("didn't play", '', 'play', tags=self.negative_past)
        self.assertEqual(verb.negative(), verb)

    def test_to_basic_verb(self):
        verb = NewVerb('go', 'went')

        self.assertEqual(verb.negative().to_basic_verb(), verb)
        self.assertEqual(verb.past_tense().to_basic_verb(), verb)
        self.assertEqual(verb.past_tense().to_basic_verb(), verb)
        self.assertEqual(verb.capitalize().to_basic_verb(), verb)
        self.assertEqual(verb.de_capitalize().to_basic_verb(), verb)
        self.assertEqual(verb.bold().to_basic_verb(), verb)

        self.assertEqual(verb.negative().past_tense().bold().capitalize().to_basic_verb(), verb)
