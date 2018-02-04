import unittest
from typing import List, Any

from sentences.backend.investigation_tools import (requires_third_person, is_third_person, find_subject,
                                                   is_word_in_sentence, get_present_be_verb)
from sentences.words.new_word import NewNoun
from sentences.words.pronoun import Pronoun, CapitalPronoun
from sentences.words.punctuation import Punctuation
from sentences.words.new_verb import NewVerb
from sentences.words.basicword import BasicWord

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun.__members__.values()
period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION


class TestInvestigationTools(unittest.TestCase):
    def test_find_subject_on_standard_sentence(self):
        sentence = [NewNoun('cow'), NewVerb('give'), NewNoun('frog'), BasicWord.preposition('to'),
                    NewNoun('pig'), period]

        self.assertEqual(find_subject(sentence), 0)

        words = [NewNoun('orangutan'), NewNoun('bunny')]
        self.assertEqual(find_subject(words + sentence), 2)

    def test_find_subject_on_standard_predicate(self):

        predicate = [NewVerb('give'), NewNoun('frog'), BasicWord.preposition('to'), NewNoun('pig'), period]

        self.assertEqual(find_subject(predicate), -1)

    def test_find_subject_limitations(self):
        sentence = [BasicWord('to'), BasicWord('boldly'), NewVerb('save_paragraphs_to_pdf')]
        self.assertEqual(find_subject(sentence), 1)

        sentence = [BasicWord('to'), BasicWord('boldly'), BasicWord('save_paragraphs_to_pdf')]
        self.assertEqual(find_subject(sentence), -1)

    def test_is_third_person_fails_on_word(self):
        self.assertFalse(is_third_person(BasicWord('dog')))

    def test_is_third_person_pronouns_true(self):
        names = ['HE', 'SHE', 'IT', 'HIM', 'HER']
        lower = [getattr(Pronoun, name) for name in names]
        upper = [getattr(CapitalPronoun, name) for name in names]
        for third_person in lower + upper:
            self.assertTrue(is_third_person(third_person))

    def test_is_third_person_pronouns_false(self):
        names = ['I', 'ME', 'YOU', 'WE', 'US', 'THEY', 'THEM']
        lower = [getattr(Pronoun, name) for name in names]
        upper = [getattr(CapitalPronoun, name) for name in names]
        for not_it in lower + upper:
            self.assertFalse(is_third_person(not_it))

    def test_is_third_person_all_non_plural_nouns(self):
        noun = NewNoun('dog')
        self.assertTrue(is_third_person(noun))
        self.assertTrue(is_third_person(noun.definite()))
        self.assertTrue(is_third_person(noun.indefinite()))
        self.assertTrue(is_third_person(NewNoun('Bob')))

    def test_is_third_person_plural_nouns(self):
        noun = NewNoun('dog')
        self.assertFalse(is_third_person(noun.plural()))
        self.assertFalse(is_third_person(noun.definite().plural()))
        self.assertFalse(is_third_person(noun.plural().definite()))
        self.assertFalse(is_third_person(NewNoun.proper_noun('The Bobs', plural=True)))

    def test_requires_third_person(self):
        answer = [it, NewVerb('steal', 'stole'), her, exclamation]
        self.assertTrue(requires_third_person(answer))

        answer = [NewNoun('teacher', ''), NewVerb('take', 'took'), me, period]
        self.assertTrue(requires_third_person(answer))

        answer[0] = answer[0].plural()
        self.assertFalse(requires_third_person(answer))

        answer[0] = you
        self.assertFalse(requires_third_person(answer))

    def test_requires_third_person_no_subject(self):
        answer = [NewVerb('STOP'), BasicWord('in'), NewNoun('name').definite(), BasicWord('of'), NewNoun('love'),
                  period, period, period]
        self.assertFalse(requires_third_person(answer))

    def test_is_word_in_sentence_pronoun(self):
        sentence = [i, NewVerb('do').negative().past_tense(), it]
        self.assertTrue(is_word_in_sentence(me, sentence))
        self.assertTrue(is_word_in_sentence(i, sentence))
        self.assertFalse(is_word_in_sentence(they, sentence))
        self.assertTrue(is_word_in_sentence(it, sentence))

    def test_is_word_in_sentence_other(self):
        sentence = [BasicWord('tom'), NewVerb('dick'), NewNoun('harry')]
        self.assertTrue(is_word_in_sentence(BasicWord('tom'), sentence))
        self.assertTrue(is_word_in_sentence(NewVerb('dick'), sentence))
        self.assertTrue(is_word_in_sentence(NewNoun('harry'), sentence))

        self.assertFalse(is_word_in_sentence(NewNoun('tom'), sentence))
        self.assertFalse(is_word_in_sentence(BasicWord('dick'), sentence))
        self.assertFalse(is_word_in_sentence(NewVerb('harry'), sentence))

    def test_get_present_be_verb_no_subj(self):
        sentence = [NewVerb('Give'), Pronoun.ME, NewNoun('break').indefinite(), period]
        self.assertEqual(get_present_be_verb(sentence), BasicWord('be'))

    def test_get_present_be_verb_are(self):
        predicate = [NewVerb('play'), period]
        subjs = [you, them, they, we, us, BasicWord('You'), BasicWord('They'), BasicWord('We'),
                 NewNoun.proper_noun('The Guys', plural=True),
                 NewNoun('dog').plural(), NewNoun('dog').definite().plural(), NewNoun('dog').plural().capitalize()]
        for subj in subjs:
            self.assertEqual(get_present_be_verb([subj] + predicate), BasicWord('are'))

    def test_get_present_be_verb_is(self):
        predicate = [NewVerb('play').third_person(), period]
        p_nouns = [he, him, she, her, it]
        capital_p_nouns = [p_noun.capitalize() for p_noun in p_nouns]
        subjs = [NewNoun('water'), NewNoun('dog').definite(), NewNoun('dog').capitalize(), NewNoun('dog').indefinite(),
                 NewNoun('Joe')]
        for subj in p_nouns + capital_p_nouns + subjs:
            self.assertEqual(get_present_be_verb([subj] + predicate), BasicWord('is'))

    def test_get_present_be_verb_am(self):
        predicate = [NewVerb('play'), period]  # type: List[Any]
        subjs = [Pronoun.I, Pronoun.ME, CapitalPronoun.I, CapitalPronoun.ME]
        for subj in subjs:
            self.assertEqual(get_present_be_verb([subj] + predicate), BasicWord('am'))
